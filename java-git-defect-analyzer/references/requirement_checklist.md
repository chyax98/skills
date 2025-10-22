# 需求验证清单

系统化的需求验证步骤,确保代码实现完全符合需求文档。

## 1. 核心功能验证

### 1.1 功能完整性检查

**验证步骤**:
1. 列出需求文档中的所有功能点
2. 逐一检查代码中是否有对应实现
3. 标记缺失/不完整的功能

**检查清单**:
- [ ] 需求中的所有操作动词是否都有对应方法?
- [ ] 需求中的所有数据实体是否都有对应类?
- [ ] 需求中的所有业务规则是否都有实现?
- [ ] 需求中的所有用户交互是否都有接口?

**示例**:

**需求**:
```
用户管理功能:
1. 注册用户
2. 登录验证
3. 修改个人信息
4. 找回密码
```

**验证**:
```
✅ registerUser() - 已实现
✅ login() - 已实现
✅ updateProfile() - 已实现
❌ resetPassword() - 缺失
```

---

### 1.2 业务流程验证

**验证步骤**:
1. 提取需求中的业务流程图/时序描述
2. 对比代码执行流程
3. 验证顺序、条件、分支是否一致

**检查清单**:
- [ ] 流程步骤顺序是否与需求一致?
- [ ] 条件分支是否完整?
- [ ] 异常流程是否处理?
- [ ] 业务规则是否正确应用?

**示例**:

**需求流程**:
```
订单提交流程:
1. 验证库存充足
2. 锁定库存
3. 创建订单
4. 扣减库存
5. 发送确认通知
```

**代码验证**:
```java
public Order submitOrder(OrderRequest request) {
    // ✅ 1. 验证库存
    if (!inventoryService.checkStock(request.getItems())) {
        throw new InsufficientStockException();
    }

    // ✅ 2. 锁定库存
    inventoryService.lock(request.getItems());

    // ✅ 3. 创建订单
    Order order = orderService.create(request);

    // ✅ 4. 扣减库存
    inventoryService.deduct(request.getItems());

    // ✅ 5. 发送通知
    notificationService.sendOrderConfirmation(order);

    return order;
}
```

---

### 1.3 边界条件验证

**验证步骤**:
1. 识别需求中的边界值/极限情况
2. 检查代码是否处理这些情况

**检查清单**:
- [ ] 空值 (null) 是否处理?
- [ ] 空集合/字符串是否处理?
- [ ] 数值边界 (0, 负数, 最大值) 是否验证?
- [ ] 并发/重复请求是否处理?
- [ ] 超时情况是否处理?

**边界条件类型**:

| 边界类型 | 检查项 | 处理方式 |
|---------|-------|---------|
| **空值** | null 参数/返回值 | 抛出异常或返回默认值 |
| **空集合** | 空 List/Set/Map | 返回空结果或默认值 |
| **空字符串** | "" 或空格字符串 | 验证后拒绝或清理 |
| **数值边界** | 0, 负数, Integer.MAX_VALUE | 范围验证 |
| **并发** | 同时多个请求 | 锁机制或幂等性设计 |
| **超时** | 外部调用超时 | 超时配置 + 异常处理 |

**示例**:

```java
// ✅ 完善的边界条件处理
public BigDecimal calculateTotal(List<OrderItem> items, BigDecimal discount) {
    // 空集合处理
    if (items == null || items.isEmpty()) {
        return BigDecimal.ZERO;
    }

    // 空值处理
    if (discount == null) {
        discount = BigDecimal.ZERO;
    }

    // 数值边界验证
    if (discount.compareTo(BigDecimal.ZERO) < 0 || discount.compareTo(BigDecimal.ONE) > 0) {
        throw new IllegalArgumentException("折扣必须在 0-1 之间");
    }

    BigDecimal total = items.stream()
        .map(OrderItem::getPrice)
        .reduce(BigDecimal.ZERO, BigDecimal::add);

    return total.multiply(BigDecimal.ONE.subtract(discount));
}
```

---

## 2. 数据一致性验证

### 2.1 事务完整性检查

**验证步骤**:
1. 识别需求中涉及多步数据操作的场景
2. 检查代码是否使用事务保护
3. 验证事务边界是否正确

**检查清单**:
- [ ] 多表操作是否在同一事务中?
- [ ] 事务边界是否合理? (不要过大或过小)
- [ ] 是否有正确的事务传播级别?
- [ ] 异常是否会触发回滚?

**示例**:

```java
// ✅ 正确的事务使用
@Transactional
public void transferMoney(Long fromId, Long toId, BigDecimal amount) {
    // 所有数据库操作在同一事务中
    Account from = accountRepository.findById(fromId)
        .orElseThrow(() -> new AccountNotFoundException(fromId));

    Account to = accountRepository.findById(toId)
        .orElseThrow(() -> new AccountNotFoundException(toId));

    from.deduct(amount);
    to.add(amount);

    accountRepository.save(from);
    accountRepository.save(to);

    // 记录转账日志
    transactionLogRepository.save(new TransactionLog(fromId, toId, amount));

    // 任一失败都会回滚所有操作
}
```

---

### 2.2 数据验证完整性

**验证步骤**:
1. 提取需求中的数据验证规则
2. 检查代码是否实现所有验证

**检查清单**:
- [ ] 必填字段是否验证?
- [ ] 数据格式是否验证? (邮箱、手机号、日期)
- [ ] 数据范围是否验证? (年龄、金额、长度)
- [ ] 业务规则是否验证? (库存充足、余额充足)
- [ ] 唯一性是否验证? (用户名、邮箱不重复)

**验证规则类型**:

| 验证类型 | 示例规则 | 实现方式 |
|---------|---------|---------|
| **必填** | 用户名不能为空 | `@NotNull`, `@NotBlank` |
| **格式** | 邮箱格式 | `@Email`, 正则表达式 |
| **范围** | 年龄 18-100 | `@Min`, `@Max`, `@Range` |
| **长度** | 密码 6-20 位 | `@Size(min=6, max=20)` |
| **唯一性** | 用户名不重复 | 数据库查询验证 |
| **业务规则** | 库存充足 | 业务逻辑验证 |

**示例**:

```java
// ✅ 使用 Bean Validation
public class RegisterRequest {
    @NotBlank(message = "用户名不能为空")
    @Size(min = 3, max = 20, message = "用户名长度 3-20 位")
    private String username;

    @NotBlank(message = "密码不能为空")
    @Size(min = 6, max = 20, message = "密码长度 6-20 位")
    private String password;

    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式错误")
    private String email;

    @NotBlank(message = "手机号不能为空")
    @Pattern(regexp = "\\d{11}", message = "手机号必须是 11 位数字")
    private String phone;
}

@PostMapping("/register")
public ResponseEntity<User> register(@Valid @RequestBody RegisterRequest request) {
    // @Valid 自动触发验证

    // ✅ 业务规则验证
    if (userRepository.existsByUsername(request.getUsername())) {
        throw new DuplicateUsernameException();
    }

    User user = userService.register(request);
    return ResponseEntity.ok(user);
}
```

---

## 3. 异常处理验证

### 3.1 异常场景覆盖

**验证步骤**:
1. 识别需求中的异常场景
2. 检查代码是否处理所有异常
3. 验证异常处理方式是否合理

**检查清单**:
- [ ] 网络/IO 异常是否处理?
- [ ] 外部服务调用失败是否处理?
- [ ] 数据库异常是否处理?
- [ ] 业务异常是否定义明确?
- [ ] 异常信息是否友好?

**异常处理模式**:

| 异常类型 | 处理方式 | 示例 |
|---------|---------|------|
| **业务异常** | 自定义异常 + 明确信息 | `throw new InsufficientBalanceException()` |
| **系统异常** | 捕获 + 日志 + 友好提示 | `catch (SQLException e) { log.error(...); throw new SystemException(); }` |
| **第三方异常** | 捕获 + 降级/重试 | `try { api.call(); } catch (TimeoutException e) { return fallback(); }` |

**示例**:

```java
// ✅ 完善的异常处理
public PaymentResult pay(PaymentRequest request) {
    try {
        // 业务验证
        if (accountService.getBalance(request.getUserId()).compareTo(request.getAmount()) < 0) {
            throw new InsufficientBalanceException("余额不足");
        }

        // 调用第三方支付
        PaymentResponse response = paymentGateway.charge(request);

        if (response.isSuccess()) {
            return PaymentResult.success(response.getTransactionId());
        } else {
            return PaymentResult.failure(response.getErrorMessage());
        }

    } catch (InsufficientBalanceException e) {
        // 业务异常: 直接返回给用户
        log.warn("支付失败: {}", e.getMessage());
        return PaymentResult.failure(e.getMessage());

    } catch (TimeoutException e) {
        // 超时异常: 记录日志 + 友好提示
        log.error("支付网关超时", e);
        return PaymentResult.failure("支付系统繁忙,请稍后重试");

    } catch (Exception e) {
        // 未知异常: 记录详细日志 + 通用提示
        log.error("支付异常", e);
        return PaymentResult.failure("支付失败,请联系客服");
    }
}
```

---

## 4. 性能要求验证

### 4.1 响应时间验证

**验证步骤**:
1. 识别需求中的性能要求 (如 "接口响应时间 < 1 秒")
2. 检查代码是否有性能优化措施

**检查清单**:
- [ ] 是否有数据库查询优化? (索引、分页、懒加载)
- [ ] 是否有缓存机制?
- [ ] 是否有异步处理?
- [ ] 是否避免了 N+1 查询问题?

**示例**:

```java
// ❌ 性能问题: N+1 查询
public List<OrderVO> getOrders() {
    List<Order> orders = orderRepository.findAll();
    return orders.stream()
        .map(order -> {
            // 每个 order 都查询一次数据库
            User user = userRepository.findById(order.getUserId()).get();
            return new OrderVO(order, user);
        })
        .collect(Collectors.toList());
}

// ✅ 优化: 批量查询
public List<OrderVO> getOrders() {
    List<Order> orders = orderRepository.findAll();

    // 批量查询用户
    Set<Long> userIds = orders.stream()
        .map(Order::getUserId)
        .collect(Collectors.toSet());
    Map<Long, User> userMap = userRepository.findAllById(userIds).stream()
        .collect(Collectors.toMap(User::getId, u -> u));

    return orders.stream()
        .map(order -> new OrderVO(order, userMap.get(order.getUserId())))
        .collect(Collectors.toList());
}

// ✅ 更好: 使用缓存
@Cacheable("orders")
public List<OrderVO> getOrders() {
    // 结果会被缓存
    return orderService.getOrdersWithUsers();
}
```

---

## 5. 安全要求验证

### 5.1 权限控制验证

**验证步骤**:
1. 识别需求中的权限要求
2. 检查代码是否实现权限控制

**检查清单**:
- [ ] 是否有认证机制? (登录验证)
- [ ] 是否有授权机制? (权限验证)
- [ ] 敏感操作是否需要二次验证?
- [ ] 是否防止越权访问?

**示例**:

```java
// ✅ 权限控制
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/users/{id}")
public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
    userService.delete(id);
    return ResponseEntity.noContent().build();
}

// ✅ 防止越权: 只能操作自己的数据
@GetMapping("/orders/{id}")
public ResponseEntity<Order> getOrder(@PathVariable Long id, @AuthenticationPrincipal User currentUser) {
    Order order = orderRepository.findById(id)
        .orElseThrow(() -> new OrderNotFoundException(id));

    // 验证订单所有权
    if (!order.getUserId().equals(currentUser.getId())) {
        throw new AccessDeniedException("无权访问此订单");
    }

    return ResponseEntity.ok(order);
}
```

---

## 验证清单总结

### 完整验证流程

```
1. 功能完整性验证
   ├─ 所有功能点是否实现?
   ├─ 业务流程是否正确?
   └─ 边界条件是否处理?

2. 数据一致性验证
   ├─ 事务是否完整?
   └─ 数据验证是否完整?

3. 异常处理验证
   ├─ 异常场景是否覆盖?
   └─ 异常处理是否合理?

4. 性能要求验证
   ├─ 响应时间是否满足?
   └─ 是否有优化措施?

5. 安全要求验证
   ├─ 权限控制是否完善?
   └─ 是否防止常见攻击?
```

---

## 参考资料

- [Spring Boot 验证指南](https://spring.io/guides/gs/validating-form-input/)
- [数据库事务最佳实践](https://www.baeldung.com/transaction-configuration-with-jpa-and-spring)
- [异常处理最佳实践](https://www.baeldung.com/exception-handling-for-rest-with-spring)
