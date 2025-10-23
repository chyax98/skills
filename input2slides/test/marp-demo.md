---
marp: true
theme: default
paginate: true
header: 'Marp 测试演示'
footer: 'Claude @ 2025-10-23'
---

# Marp 测试演示
## 验证导出功能 ✅

---

## 为什么选择 Marp?

- ✅ **轻量级** - 纯 Markdown + CSS
- ✅ **CLI 工具** - 简单易用
- ✅ **多格式导出** - HTML/PDF/PPTX
- ✅ **无复杂依赖** - 开箱即用

---

## 代码示例

TypeScript 类型注解:

```typescript
interface User {
  id: number
  name: string
  email: string
}

function getUser(id: number): User {
  return {
    id,
    name: "Alice",
    email: "alice@example.com"
  }
}
```

---

## Python 示例

```python
def fibonacci(n: int) -> int:
    """计算斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 测试
for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")
```

---

# 导出测试成功! 🎉

### 支持的格式
- **HTML** - 自包含单文件
- **PDF** - 可打印分享
- **PPTX** - PowerPoint 兼容

---
