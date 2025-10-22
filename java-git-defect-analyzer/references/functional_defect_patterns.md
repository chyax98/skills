# 功能缺陷识别模式

本文档定义了常见的功能缺陷模式,用于对比需求文档与代码实现。

## 1. 功能完全缺失 (CRITICAL)

### 定义
需求文档明确要求的功能在代码中完全找不到相关实现。

### 识别方法
- 提取需求中的关键操作动词 (记录、发送、验证、生成等)
- 在代码变更中搜索对应的方法名、类名、注释
- 未找到任何匹配项 → 功能缺失

### 示例

**需求**:
```
用户登录成功后,系统需要记录登录日志,包含:
- 登录时间
- IP 地址
- 设备信息
```

**缺陷代码**:
```java
@PostMapping("/login")
public ResponseEntity<UserVO> login(@RequestBody LoginRequest request) {
    User user = authService.authenticate(request);
    return ResponseEntity.ok(userMapper.toVO(user));
}
// ❌ 完全缺失日志记录逻辑
```

**修复建议**:
```java
@PostMapping("/login")
public ResponseEntity<UserVO> login(@RequestBody LoginRequest request) {
    User user = authService.authenticate(request);

    // ✅ 添加日志记录
    LoginLog log = new LoginLog();
    log.setUserId(user.getId());
    log.setLoginTime(LocalDateTime.now());
    log.setIpAddress(request.getRemoteAddr());
    log.setDeviceInfo(request.getHeader("User-Agent"));
    loginLogService.save(log);

    return ResponseEntity.ok(userMapper.toVO(user));
}
```

---

## 2. 功能实现不完整 (HIGH)

### 定义
功能部分实现,但缺少关键逻辑分支或边界条件处理。

### 识别方法
- 需求描述了多个场景或条件分支
- 代码只处理了部分场景
- 缺少异常情况、边界值、特殊状态的处理

### 示例 1: 缺少逻辑分支

**需求**:
```
支持两种登录方式:
1. 手机号 + 验证码
2. 邮箱 + 密码
```

**缺陷代码**:
```java
public User login(String username, String credential) {
    // ⚠️ 只实现了手机号登录
    if (isPhoneNumber(username)) {
        return phoneLoginService.verify(username, credential);
    }
    // ❌ 缺少邮箱登录分支
    throw new UnsupportedOperationException("Unsupported login method");
}
```

**修复建议**:
```java
public User login(String username, String credential) {
    if (isPhoneNumber(username)) {
        return phoneLoginService.verify(username, credential);
    } else if (isEmail(username)) {
        // ✅ 添加邮箱登录分支
        return emailLoginService.authenticate(username, credential);
    } else {
        throw new IllegalArgumentException("Invalid username format");
    }
}
```

### 示例 2: 缺少异常处理

**需求**:
```
订单提交失败时,需要回滚库存并通知用户
```

**缺陷代码**:
```java
public Order submitOrder(OrderRequest request) {
    inventoryService.deduct(request.getItems()); // 扣减库存
    Order order = orderService.create(request);  // 创建订单
    // ❌ 未处理订单创建失败的回滚逻辑
    return order;
}
```

**修复建议**:
```java
@Transactional
public Order submitOrder(OrderRequest request) {
    try {
        inventoryService.deduct(request.getItems());
        Order order = orderService.create(request);
        return order;
    } catch (Exception e) {
        // ✅ 事务自动回滚库存
        // ✅ 通知用户
        notificationService.sendOrderFailure(request.getUserId(), e.getMessage());
        throw new OrderSubmitException("订单提交失败", e);
    }
}
```

---

## 3. 业务逻辑错误 (CRITICAL)

### 定义
代码实现与需求描述的业务流程矛盾或顺序错误。

### 识别方法
- 对比需求的业务流程图/时序描述
- 检查代码执行顺序是否与需求一致
- 验证业务规则是否正确实现

### 示例 1: 流程顺序错误

**需求**:
```
支付流程:
1. 验证账户余额
2. 扣减余额
3. 创建支付记录
```

**缺陷代码**:
```java
public Payment pay(Long userId, BigDecimal amount) {
    // ❌ 先扣款再验证
    accountService.deduct(userId, amount);

    if (accountService.getBalance(userId).compareTo(amount) < 0) {
        throw new InsufficientBalanceException();
    }

    return paymentService.create(userId, amount);
}
```

**修复建议**:
```java
public Payment pay(Long userId, BigDecimal amount) {
    // ✅ 先验证再扣款
    if (accountService.getBalance(userId).compareTo(amount) < 0) {
        throw new InsufficientBalanceException();
    }

    accountService.deduct(userId, amount);
    return paymentService.create(userId, amount);
}
```

### 示例 2: 业务规则错误

**需求**:
```
VIP 用户享受 8 折优惠,普通用户 9 折
```

**缺陷代码**:
```java
public BigDecimal calculatePrice(User user, BigDecimal originalPrice) {
    if (user.isVip()) {
        return originalPrice.multiply(new BigDecimal("0.9")); // ❌ VIP 是 0.8 折
    }
    return originalPrice.multiply(new BigDecimal("0.8"));     // ❌ 普通用户是 0.9 折
}
```

**修复建议**:
```java
public BigDecimal calculatePrice(User user, BigDecimal originalPrice) {
    BigDecimal discount = user.isVip()
        ? new BigDecimal("0.8")  // ✅ VIP 8 折
        : new BigDecimal("0.9"); // ✅ 普通 9 折
    return originalPrice.multiply(discount);
}
```

---

## 4. 数据一致性问题 (HIGH)

### 定义
操作不符合 ACID 原则,可能导致数据不一致。

### 识别方法
- 需求涉及多表操作或分布式事务
- 检查是否有事务边界
- 验证失败时是否正确回滚

### 示例

**需求**:
```
转账操作需要保证原子性:
- A 账户扣款
- B 账户加款
```

**缺陷代码**:
```java
// ❌ 无事务保护
public void transfer(Long fromId, Long toId, BigDecimal amount) {
    accountService.deduct(fromId, amount);  // 可能成功
    accountService.add(toId, amount);       // 可能失败 → 数据不一致
}
```

**修复建议**:
```java
@Transactional  // ✅ 事务保护
public void transfer(Long fromId, Long toId, BigDecimal amount) {
    accountService.deduct(fromId, amount);
    accountService.add(toId, amount);
    // 任一失败都会回滚
}
```

---

## 5. 参数验证缺失 (MEDIUM)

### 定义
需求指定的数据验证规则未实现。

### 识别方法
- 提取需求中的验证要求 (格式、范围、必填)
- 检查代码是否有对应的验证逻辑

### 示例

**需求**:
```
用户注册时:
- 手机号必须是 11 位数字
- 密码长度 6-20 位
- 邮箱必须符合格式
```

**缺陷代码**:
```java
public User register(RegisterRequest request) {
    // ❌ 无任何验证
    User user = new User();
    user.setPhone(request.getPhone());
    user.setPassword(request.getPassword());
    user.setEmail(request.getEmail());
    return userRepository.save(user);
}
```

**修复建议**:
```java
public User register(RegisterRequest request) {
    // ✅ 添加验证
    if (!request.getPhone().matches("\\d{11}")) {
        throw new ValidationException("手机号格式错误");
    }

    if (request.getPassword().length() < 6 || request.getPassword().length() > 20) {
        throw new ValidationException("密码长度必须为 6-20 位");
    }

    if (!isValidEmail(request.getEmail())) {
        throw new ValidationException("邮箱格式错误");
    }

    User user = new User();
    user.setPhone(request.getPhone());
    user.setPassword(passwordEncoder.encode(request.getPassword()));
    user.setEmail(request.getEmail());
    return userRepository.save(user);
}
```

---

## 6. 边界条件未处理 (MEDIUM)

### 定义
需求隐含或明确的边界情况未处理。

### 识别方法
- 检查空值、空集合、边界值的处理
- 验证并发、重复请求的处理

### 常见边界条件

**空值处理**:
```java
// ❌ 未检查 null
public String getFullName(User user) {
    return user.getFirstName() + " " + user.getLastName();
}

// ✅ 检查 null
public String getFullName(User user) {
    if (user == null) {
        return "";
    }
    String firstName = user.getFirstName() != null ? user.getFirstName() : "";
    String lastName = user.getLastName() != null ? user.getLastName() : "";
    return (firstName + " " + lastName).trim();
}
```

**空集合处理**:
```java
// ❌ 未检查空集合
public BigDecimal calculateTotal(List<OrderItem> items) {
    return items.stream()
        .map(OrderItem::getPrice)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
}

// ✅ 检查空集合
public BigDecimal calculateTotal(List<OrderItem> items) {
    if (items == null || items.isEmpty()) {
        return BigDecimal.ZERO;
    }
    return items.stream()
        .map(OrderItem::getPrice)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
}
```

---

## 检测优先级

| 缺陷类型 | 严重程度 | 检测关键词 |
|---------|---------|-----------|
| 功能完全缺失 | CRITICAL | 需求动词未在代码中出现 |
| 业务逻辑错误 | CRITICAL | 流程顺序、规则与需求矛盾 |
| 数据一致性问题 | HIGH | 多表操作无事务保护 |
| 功能实现不完整 | HIGH | 分支不全、异常未处理 |
| 参数验证缺失 | MEDIUM | 需求验证规则未实现 |
| 边界条件未处理 | MEDIUM | 空值、边界值未检查 |

---

## 自动检测策略

### 关键词匹配法
1. 提取需求中的操作动词: 记录、发送、验证、生成、计算、更新
2. 在代码中搜索相关方法名、类名、变量名
3. 未匹配 → 功能缺失

### 流程比对法
1. 识别需求中的顺序关键词: 先...后...、首先...然后...
2. 提取代码执行顺序
3. 比对是否一致

### 规则提取法
1. 识别需求中的条件���: 如果...则...、当...时...
2. 检查代码是否有对应的 if/switch 分支
3. 验证条件表达式是否正确

---

## 参考资料

- [Java 代码审查清单](https://github.com/code-review-checklists/java-checklist)
- [需求验证最佳实践](https://www.baeldung.com/java-validation)
