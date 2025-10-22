# 低优先级问题参考

本文档定义了对功能影响较小的代码质量问题,这些问题不影响功能正确性,但会影响代码可维护性。

## 1. 命名规范

### 1.1 类命名

**规范**:
- 使用大写驼峰 (PascalCase)
- 名词或名词短语
- 清晰描述类的职责

**示例**:

```java
// ✅ 好的命名
public class UserService { }
public class OrderRepository { }
public class PaymentGatewayClient { }

// ❌ 不好的命名
public class userservice { }       // 全小写
public class Usr { }                // 缩写不清晰
public class DoSomething { }        // 使用动词
public class Data { }               // 太泛化
```

---

### 1.2 方法命名

**规范**:
- 使用小写驼峰 (camelCase)
- 动词或动词短语
- 清晰表达操作意图

**示例**:

```java
// ✅ 好的命名
public User getUserById(Long id) { }
public boolean isActive() { }
public void sendEmail(String to, String subject) { }
public List<Order> findOrdersByStatus(OrderStatus status) { }

// ❌ 不好的命名
public User get(Long id) { }               // 太简略
public boolean active() { }                // 缺少 is/has
public void email(String to, String s) { } // 动词不明确,参数名不清晰
public List<Order> process() { }           // 不知道处理什么
```

**命名前缀约定**:

| 前缀 | 用途 | 示例 |
|------|------|------|
| `get` | 获取属性/查询单个对象 | `getUserName()`, `getBalance()` |
| `set` | 设置属性 | `setUserName()`, `setBalance()` |
| `is/has` | 布尔判断 | `isActive()`, `hasPermission()` |
| `find` | 查询(可能为空) | `findById()`, `findByEmail()` |
| `list/get` | 查询列表 | `listUsers()`, `getOrders()` |
| `create` | 创建新对象 | `createOrder()`, `createUser()` |
| `update` | 更新对象 | `updateProfile()`, `updateStatus()` |
| `delete/remove` | 删除对象 | `deleteUser()`, `removeItem()` |
| `calculate/compute` | 计算 | `calculateTotal()`, `computeDiscount()` |
| `validate/check` | 验证 | `validateInput()`, `checkPermission()` |

---

### 1.3 变量命名

**规范**:
- 使用小写驼峰 (camelCase)
- 描述性名称,避免缩写
- 常量使用全大写下划线分隔

**示例**:

```java
// ✅ 好的命名
String userName = "John";
List<Order> activeOrders = new ArrayList<>();
BigDecimal totalAmount = BigDecimal.ZERO;
final int MAX_RETRY_COUNT = 3;

// ❌ 不好的命名
String un = "John";           // 过度缩写
List<Order> list = new ArrayList<>();  // 太泛化
BigDecimal amt = BigDecimal.ZERO;      // 缩写不清晰
final int max = 3;            // 常量未使用全大写
```

---

## 2. 代码格式

### 2.1 缩进和空格

**规范**:
- 使用 4 空格缩进 (或 2 空格,团队统一即可)
- 不使用 Tab
- 运算符前后加空格
- 逗号后加空格

**示例**:

```java
// ✅ 好的格式
public BigDecimal calculateTotal(List<Item> items) {
    BigDecimal total = BigDecimal.ZERO;
    for (Item item : items) {
        total = total.add(item.getPrice());
    }
    return total;
}

// ❌ 不好的格式
public BigDecimal calculateTotal(List<Item> items){
BigDecimal total=BigDecimal.ZERO;
for(Item item:items){
total=total.add(item.getPrice());
}
return total;
}
```

---

### 2.2 括号风格

**规范** (K&R 风格):
- 左括号不换行
- 右括号换行
- else/catch/finally 与右括号在同一行

**示例**:

```java
// ✅ 好的格式
if (condition) {
    doSomething();
} else {
    doOther();
}

try {
    riskyOperation();
} catch (Exception e) {
    handleException(e);
} finally {
    cleanup();
}

// ❌ 不好的格式 (Allman 风格,不推荐 Java)
if (condition)
{
    doSomething();
}
else
{
    doOther();
}
```

---

### 2.3 行长度

**规范**:
- 每行不超过 120 字符
- 长语句适当换行

**示例**:

```java
// ✅ 适当换行
String message = String.format(
    "User %s (ID: %d) performed action %s at %s",
    user.getName(),
    user.getId(),
    action,
    timestamp
);

// ❌ 单行过长 (>120 字符)
String message = String.format("User %s (ID: %d) performed action %s at %s", user.getName(), user.getId(), action, timestamp);
```

---

## 3. 注释规范

### 3.1 Javadoc 注释

**规范**:
- 公共 API 必须有 Javadoc
- 描述类/方法的功能和用途
- 说明参数、返回值、异常

**示例**:

```java
/**
 * 用户服务类,提供用户相关的业务逻辑
 *
 * @author John Doe
 * @since 1.0
 */
public class UserService {

    /**
     * 根据用户 ID 查询用户信息
     *
     * @param id 用户 ID,不能为 null
     * @return 用户对象,如果不存在则返回 null
     * @throws IllegalArgumentException 如果 id 为 null
     */
    public User findById(Long id) {
        if (id == null) {
            throw new IllegalArgumentException("User ID cannot be null");
        }
        return userRepository.findById(id).orElse(null);
    }
}
```

---

### 3.2 行内注释

**规范**:
- 解释复杂逻辑的"为什么",而非"是什么"
- 避免显而易见的注释
- 标记 TODO/FIXME/HACK 时说明原因

**示例**:

```java
// ✅ 好的注释 - 解释为什么
// 使用双重检查锁定以提高性能,避免每次都进入 synchronized 块
if (instance == null) {
    synchronized (Singleton.class) {
        if (instance == null) {
            instance = new Singleton();
        }
    }
}

// TODO: 重构为观察者模式以支持多个监听器 (计划 v2.0)
notifyListener();

// ❌ 不好的注释 - 重复代码
// 获取用户名
String userName = user.getName();

// ❌ 无意义的 TODO
// TODO: fix this
```

---

### 3.3 注释过多/过少

**问题**:
- 过多注释: 代码自解释性差
- 过少注释: 复杂逻辑难以理解

**示例**:

```java
// ❌ 注释过多 - 代码应该自解释
// 创建用户对象
User user = new User();
// 设置用户名
user.setName(name);
// 设置邮箱
user.setEmail(email);
// 保存用户
userRepository.save(user);

// ✅ 清晰的代码,无需过多注释
User user = new User(name, email);
userRepository.save(user);

// ✅ 复杂逻辑需要注释
// 计算复合折扣: VIP 8折 + 满减 20 元 + 优惠券
BigDecimal finalPrice = originalPrice
    .multiply(vipDiscount)
    .subtract(fullReductionAmount)
    .subtract(couponAmount);
```

---

## 4. 代码重复

### 4.1 重复代码块

**问题**: 相同或相似代码在多处出现

**示例**:

```java
// ❌ 重复代码
public void processOrder(Order order) {
    if (order == null) {
        log.error("Order is null");
        throw new IllegalArgumentException("Order cannot be null");
    }
    // ...
}

public void cancelOrder(Order order) {
    if (order == null) {
        log.error("Order is null");
        throw new IllegalArgumentException("Order cannot be null");
    }
    // ...
}

// ✅ 提取公共方法
private void validateOrder(Order order) {
    if (order == null) {
        log.error("Order is null");
        throw new IllegalArgumentException("Order cannot be null");
    }
}

public void processOrder(Order order) {
    validateOrder(order);
    // ...
}

public void cancelOrder(Order order) {
    validateOrder(order);
    // ...
}
```

---

### 4.2 Magic Number

**问题**: 硬编码的数字常量

**示例**:

```java
// ❌ Magic Number
if (user.getAge() < 18) {
    return "未成年";
}
if (order.getStatus() == 2) {
    return "已完成";
}

// ✅ 使用常量
private static final int ADULT_AGE = 18;
private static final int ORDER_STATUS_COMPLETED = 2;

if (user.getAge() < ADULT_AGE) {
    return "未成年";
}
if (order.getStatus() == ORDER_STATUS_COMPLETED) {
    return "已完成";
}

// ✅ 更好: 使用枚举
enum OrderStatus {
    PENDING(1), COMPLETED(2), CANCELLED(3);
    private final int code;
}

if (order.getStatus() == OrderStatus.COMPLETED) {
    return "已完成";
}
```

---

## 5. 性能轻微问题

### 5.1 不必要的对象创建

**问题**: 创建无用对象,增加 GC 压力

**示例**:

```java
// ❌ 不必要的 String 对象
String str = new String("hello");  // 应该直接用 "hello"

// ❌ 自动装箱/拆箱
Integer count = 0;
for (int i = 0; i < 1000; i++) {
    count += i;  // 每次循环都装箱/拆箱
}

// ✅ 使用基本类型
int count = 0;
for (int i = 0; i < 1000; i++) {
    count += i;
}
```

---

### 5.2 循环中的低效操作

**问题**: 循环中执行不必要的重复计算

**示例**:

```java
// ❌ 循环中重复计算
for (int i = 0; i < list.size(); i++) {  // size() 每次都调用
    process(list.get(i));
}

// ✅ 提取到循环外
int size = list.size();
for (int i = 0; i < size; i++) {
    process(list.get(i));
}

// ✅ 使用增强 for 循环
for (Item item : list) {
    process(item);
}
```

---

## 6. 日志问题

### 6.1 日志级别不当

**问题**: 日志级别使用不恰当

**规范**:

| 级别 | 用途 | 示例 |
|------|------|------|
| `ERROR` | 系统错误,需要立即处理 | `log.error("Database connection failed", e)` |
| `WARN` | 警告,可能有问题但不影响运行 | `log.warn("Deprecated API called")` |
| `INFO` | 重要业务流程节点 | `log.info("User {} logged in", userId)` |
| `DEBUG` | 调试信息,开发时用 | `log.debug("Query result: {}", result)` |
| `TRACE` | 详细追踪信息 | `log.trace("Method entry: {}", params)` |

**示例**:

```java
// ❌ 日志级别不当
log.error("User login successful");  // 成功不应该用 ERROR
log.info("Detailed query params: {}", params);  // 详细信息应该用 DEBUG

// ✅ 正确的日志级别
log.info("User {} login successful", userId);
log.debug("Query params: {}", params);
```

---

### 6.2 日志过多/过少

**问题**:
- 过多日志: 影响性能,难以查找关键信息
- 过少日志: 问题难以追踪

**示例**:

```java
// ❌ 日志过多
log.debug("Entering method processOrder");
log.debug("Order ID: {}", order.getId());
log.debug("Order status: {}", order.getStatus());
log.debug("Validating order...");
log.debug("Order validated");
log.debug("Processing order...");
log.debug("Order processed");
log.debug("Exiting method processOrder");

// ✅ 关键节点日志
log.info("Processing order {}", order.getId());
// 处理逻辑
log.info("Order {} processed successfully", order.getId());

// ❌ 日志过少 (异常未记录)
try {
    riskyOperation();
} catch (Exception e) {
    // 吞掉异常,没有日志
}

// ✅ 异常记录日志
try {
    riskyOperation();
} catch (Exception e) {
    log.error("Failed to perform risky operation", e);
    throw e;
}
```

---

## 检测优先级

| 问题类型 | 严重程度 | 检测关键词 |
|---------|---------|-----------|
| 命名不规范 | LOW | 不符合驼峰、使用缩写 |
| 格式问题 | LOW | 缩进不一致、缺少空格 |
| 注释缺失 | LOW | 公共 API 无 Javadoc |
| 代码重复 | LOW | 相同代码块 >3 次 |
| Magic Number | LOW | 硬编码数字 |
| 轻微性能 | LOW | 不必要对象创建 |
| 日志不当 | LOW | 日志级别错误 |

---

## 自动检测工具

推荐使用以下工具自动检测低优先级问题:

- **Checkstyle**: 代码风格检查
- **PMD**: 代码质量检查
- **SpotBugs**: Bug 检测
- **SonarLint**: IDE 集成的实时检测

---

## 参考资料

- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [阿里巴巴 Java 开发手册](https://github.com/alibaba/p3c)
- [Effective Java (3rd Edition)](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/)
