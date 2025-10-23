---
theme: default
title: Slidev 测试演示
author: Claude
layout: cover
---

# Slidev 测试演示
## 验证导出功能

---
layout: default
---

# 为什么选择 Slidev?

Slidev 是为开发者设计的演示工具:

- ✅ **Markdown 驱动** - 专注内容创作
- ✅ **主题系统** - 丰富的视觉定制
- ✅ **代码高亮** - Shiki 语法高亮
- ✅ **多格式导出** - HTML/PDF/PPTX

---
layout: two-cols
---

# 代码示例

::left::

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

::right::

Python 示例:

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
layout: center
class: text-center
---

# 导出测试成功! 🎉

## 支持的格式
- HTML (单页应用)
- PDF (可打印)
- PPTX (PowerPoint)

---
