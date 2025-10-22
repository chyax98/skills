# 高影响缺陷检测模式

本文档定义了可能导致运行时故障、安全漏洞或严重性能问题的高影响缺陷模式。

## 1. NPE (NullPointerException) 风险

### 模式 1.1: 方法调用前未检查 null

**风险**: 运行时抛出 NPE,导致服务中断

**检测规则**:
```java
// ❌ 高风险模式
Object obj = repository.findById(id);  // 可能返回 null
obj.method();                           // 直接调用 → NPE
```

**常见场景**:
- `Repository.findById()` → 未检查直接使用
- `Map.get()` → 未检查直接调用方法
- `request.getParameter()` → 未检查直接使用
- 方法参数未验证 null

**修复建议**:
```java
// ✅ 安全做法
Object obj = repository.findById(id);
if (obj == null) {
    throw new NotFoundException("对象不存在");
}
obj.method();

// ✅ 或使用 Optional
repository.findById(id)
    .map(obj -> obj.method())
    .orElseThrow(() -> new NotFoundException("对象不存在"));
```

### 模式 1.2: Optional 未检查直接 get()

**风险**: 抛出 NoSuchElementException

**检测规则**:
```java
// ❌ 高风险模式
User user = userRepository.findById(id).get();  // 未检查 isPresent()
```

**修复建议**:
```java
// ✅ 方式 1: 检查后取值
Optional<User> userOpt = userRepository.findById(id);
if (userOpt.isPresent()) {
    User user = userOpt.get();
    // ...
}

// ✅ 方式 2: 使用 orElseThrow
User user = userRepository.findById(id)
    .orElseThrow(() -> new UserNotFoundException(id));

// ✅ 方式 3: 使用 map/flatMap
return userRepository.findById(id)
    .map(this::processUser)
    .orElse(defaultValue);
```

### 模式 1.3: 集合操作未检查空

**风险**: 空集合上执行操作导致 NPE

**检测规则**:
```java
// ❌ 高风险模式
List<String> list = getList();
String first = list.get(0);  // list 可能为 null 或空
```

**修复建议**:
```java
// ✅ 安全做法
List<String> list = getList();
if (list != null && !list.isEmpty()) {
    String first = list.get(0);
}

// ✅ 使用 Optional
Optional.ofNullable(list)
    .filter(l -> !l.isEmpty())
    .map(l -> l.get(0))
    .ifPresent(this::process);
```

---

## 2. 资源泄漏

### 模式 2.1: 数据库连接未关闭

**风险**: 连接池耗尽,服务不可用

**检测规则**:
```java
// ❌ 高风险模式
Connection conn = dataSource.getConnection();
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(sql);
// 未关闭资源
```

**修复建议**:
```java
// ✅ 使用 try-with-resources (Java 7+)
try (Connection conn = dataSource.getConnection();
     Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery(sql)) {

    while (rs.next()) {
        // 处理数据
    }
} // 自动关闭资源

// ✅ 或手动关闭 (不推荐)
Connection conn = null;
try {
    conn = dataSource.getConnection();
    // ...
} finally {
    if (conn != null) {
        conn.close();
    }
}
```

### 模式 2.2: 文件流未关闭

**风险**: 文件句柄泄漏,无法删除/移动文件

**检测规则**:
```java
// ❌ 高风险模式
FileInputStream fis = new FileInputStream("file.txt");
// 未关闭
```

**修复建议**:
```java
// ✅ 使用 try-with-resources
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // 读取文件
}

// ✅ 使用 NIO Files (推荐)
List<String> lines = Files.readAllLines(Paths.get("file.txt"));
```

### 模式 2.3: HTTP 客户端未关闭

**风险**: 线程/连接泄漏

**检测规则**:
```java
// ❌ 高风险模式
CloseableHttpClient client = HttpClients.createDefault();
HttpResponse response = client.execute(request);
// 未关闭 client
```

**修复建议**:
```java
// ✅ 使用 try-with-resources
try (CloseableHttpClient client = HttpClients.createDefault()) {
    HttpResponse response = client.execute(request);
    // 处理响应
}
```

---

## 3. SQL 注入

### 模式 3.1: 字符串拼接构造 SQL

**风险**: SQL 注入攻击,数据泄露/篡改

**检测规则**:
```java
// ❌ 严重安全漏洞
String sql = "SELECT * FROM users WHERE username = '" + username + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(sql);
```

**攻击示例**:
```java
username = "admin' OR '1'='1"; // 绕过验证
// 实际执行: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
```

**修复建议**:
```java
// ✅ 使用 PreparedStatement
String sql = "SELECT * FROM users WHERE username = ?";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setString(1, username);  // 参数绑定,自动转义
ResultSet rs = pstmt.executeQuery();

// ✅ 使用 ORM (JPA/MyBatis)
@Query("SELECT u FROM User u WHERE u.username = :username")
User findByUsername(@Param("username") String username);
```

### 模式 3.2: 动态 SQL 拼接

**风险**: 复杂查询的 SQL 注入

**检测规则**:
```java
// ❌ 高风险模式
String orderBy = request.getParameter("orderBy");
String sql = "SELECT * FROM products ORDER BY " + orderBy;
```

**攻击示例**:
```java
orderBy = "1; DROP TABLE products--"; // 删除表
```

**修复建议**:
```java
// ✅ 白名单验证
Set<String> allowedColumns = Set.of("name", "price", "created_at");
if (!allowedColumns.contains(orderBy)) {
    throw new IllegalArgumentException("Invalid order by column");
}
String sql = "SELECT * FROM products ORDER BY " + orderBy;

// ✅ 使用 ORM 动态查询
CriteriaBuilder cb = em.getCriteriaBuilder();
CriteriaQuery<Product> query = cb.createQuery(Product.class);
Root<Product> root = query.from(Product.class);
query.orderBy(cb.asc(root.get(orderBy)));
```

---

## 4. 硬编码密钥

### 模式 4.1: 硬编码数据库密码

**风险**: 密码泄露,数据库被入侵

**检测规则**:
```java
// ❌ 严重安全问题
String dbUrl = "jdbc:mysql://localhost:3306/db";
String dbUser = "root";
String dbPassword = "admin123";  // 硬编码密码

Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
```

**修复建议**:
```java
// ✅ 使用环境变量
String dbPassword = System.getenv("DB_PASSWORD");

// ✅ 使用配置文件 (application.properties)
spring.datasource.password=${DB_PASSWORD}

// ✅ 使用密钥管理服务
String dbPassword = vaultClient.getSecret("db-password");
```

### 模式 4.2: 硬编码 API 密钥

**风险**: API 密钥泄露,滥用

**检测规则**:
```java
// ❌ 严重安全问题
String apiKey = "sk_live_abc123def456";
HttpRequest request = HttpRequest.newBuilder()
    .header("Authorization", "Bearer " + apiKey)
    .build();
```

**修复建议**:
```java
// ✅ 环境变量
String apiKey = System.getenv("API_KEY");

// ✅ 配置文件 (不提交到 Git)
@Value("${api.key}")
private String apiKey;
```

### 模式 4.3: 硬编码加密密钥

**风险**: 加密失效,数据泄露

**检测规则**:
```java
// ❌ 严重安全问题
String secretKey = "mySecretKey123";
Cipher cipher = Cipher.getInstance("AES");
cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(secretKey.getBytes(), "AES"));
```

**修复建议**:
```java
// ✅ 从密钥管理服务获取
KeyStore keyStore = KeyStore.getInstance("JCEKS");
keyStore.load(keyStoreStream, keyStorePassword);
Key key = keyStore.getKey("aesKey", keyPassword);
```

---

## 5. 并发问题

### 模式 5.1: 双重检查锁定未使用 volatile

**风险**: 多线程环境下对象初始化不完整

**检测规则**:
```java
// ❌ 高风险模式 (Java 5 之前会失败)
class Singleton {
    private static Singleton instance;  // 未使用 volatile

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

**修复建议**:
```java
// ✅ 添加 volatile
class Singleton {
    private static volatile Singleton instance;  // volatile 确保可见性

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}

// ✅ 更好的方式: 使用静态内部类
class Singleton {
    private static class Holder {
        private static final Singleton INSTANCE = new Singleton();
    }

    public static Singleton getInstance() {
        return Holder.INSTANCE;
    }
}
```

### 模式 5.2: 竞态条件

**风险**: 并发访问导致数据不一致

**检测规则**:
```java
// ❌ 高风险模式
class Counter {
    private int count = 0;

    public void increment() {
        count++;  // 非原子操作
    }
}
```

**修复建议**:
```java
// ✅ 使用 AtomicInteger
class Counter {
    private AtomicInteger count = new AtomicInteger(0);

    public void increment() {
        count.incrementAndGet();
    }
}

// ✅ 使用 synchronized
class Counter {
    private int count = 0;

    public synchronized void increment() {
        count++;
    }
}
```

### 模式 5.3: 非线程安全的集合

**风险**: 并发修改异常或数据丢失

**检测规则**:
```java
// ❌ 高风险模式 (多线程环境)
class Cache {
    private Map<String, Object> cache = new HashMap<>();  // 非线程安全

    public void put(String key, Object value) {
        cache.put(key, value);
    }
}
```

**修复建议**:
```java
// ✅ 使用 ConcurrentHashMap
class Cache {
    private Map<String, Object> cache = new ConcurrentHashMap<>();

    public void put(String key, Object value) {
        cache.put(key, value);
    }
}

// ✅ 使用 synchronized
class Cache {
    private Map<String, Object> cache = new HashMap<>();

    public synchronized void put(String key, Object value) {
        cache.put(key, value);
    }
}
```

---

## 检测优先级表

| 缺陷类型 | 严重程度 | 运行时影响 | 检测关键词 |
|---------|---------|-----------|-----------|
| SQL 注入 | CRITICAL | 数据泄露/篡改 | String concatenation in SQL |
| 硬编码密钥 | CRITICAL | 安全凭证泄露 | password/apiKey/secret = "..." |
| NPE 风险 | HIGH | 服务中断 | null without check |
| 资源泄漏 | HIGH | 资源耗尽 | Connection/Stream without close |
| 竞态条件 | MEDIUM | 数据不一致 | Non-atomic operations |

---

## 自动检测工具集成

推荐集成以下工具增强检测能力:

- **SpotBugs**: NPE、资源泄漏检测
- **SonarQube**: 全面代码质量分析
- **FindSecBugs**: 安全漏洞检测
- **ErrorProne**: 编译时静态分析

---

## 参考资料

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Java Concurrency in Practice](https://jcip.net/)
- [Effective Java (3rd Edition)](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/)
