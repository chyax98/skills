---
theme: black
---

# React 基础入门

从零开始掌握 React 核心概念

---

## 目录

1. React 简介与核心理念
2. 开发环境搭建
3. JSX 语法基础
4. 组件化开发
5. State 与 Props
6. 事件处理
7. 条件渲染与列表
8. Hooks 核心概念
9. 实战练习

---

## React 是什么？

**React** 是一个用于构建用户界面的 JavaScript 库

<!-- .element: class="fragment" -->

由 Facebook 于 2013 年开源

<!-- .element: class="fragment" -->

专注于 UI 层（MVC 中的 V）

<!-- .element: class="fragment" -->

---

## React 核心理念

**声明式编程**
- 描述"想要什么"，而非"怎么做"
- React 负责高效更新 DOM

<!-- .element: class="fragment" -->

**组件化**
- 将 UI 拆分为独立、可复用的组件
- 每个组件管理自己的状态

<!-- .element: class="fragment" -->

**一次学习，随处编写**
- Web、移动端、桌面应用通用

<!-- .element: class="fragment" -->

---

## React 三大核心特性

**虚拟 DOM（Virtual DOM）**
- 内存中的 JavaScript 对象
- 最小化真实 DOM 操作

<!-- .element: class="fragment" -->

**单向数据流**
- 数据从父组件流向子组件
- 便于追踪和调试

<!-- .element: class="fragment" -->

**组件复用**
- 提高开发效率
- 降低维护成本

<!-- .element: class="fragment" -->

---

## 快速搭建开发环境

使用官方脚手架 **Create React App**

```bash
# 使用 npx（推荐）
npx create-react-app my-app

# 进入项目目录
cd my-app

# 启动开发服务器
npm start
```

<!-- .element: class="fragment" -->

浏览器自动打开 `http://localhost:3000`

<!-- .element: class="fragment" -->

---

## 项目目录结构

```text
my-app/
├── node_modules/      # 依赖包
├── public/            # 静态资源
│   └── index.html     # HTML 模板
├── src/               # 源代码
│   ├── App.js         # 根组件
│   ├── index.js       # 入口文件
│   └── index.css      # 全局样式
└── package.json       # 项目配置
```

<!-- .element: class="fragment" -->

**核心文件**: `src/index.js` 和 `src/App.js`

<!-- .element: class="fragment" -->

---

## JSX 是什么？

**JSX = JavaScript + XML**

<!-- .element: class="fragment" -->

在 JavaScript 中编写类似 HTML 的语法

<!-- .element: class="fragment" -->

```javascript
const element = <h1>Hello, React!</h1>;
```

<!-- .element: class="fragment" -->

JSX 会被编译为 `React.createElement()` 调用

<!-- .element: class="fragment" -->

---

## JSX 语法规则

**必须有一个根元素**

```javascript
// ✅ 正确
return (
  <div>
    <h1>标题</h1>
    <p>段落</p>
  </div>
);

// ❌ 错误：多个根元素
return (
  <h1>标题</h1>
  <p>段落</p>
);
```

<!-- .element: class="fragment" -->

---

## JSX 中嵌入表达式

使用 `{}` 嵌入 JavaScript 表达式

```javascript
const name = 'React';
const element = <h1>Hello, {name}!</h1>;

// 表达式运算
const count = 5;
const result = <p>2 + 3 = {2 + 3}</p>;

// 函数调用
function formatName(user) {
  return user.firstName + ' ' + user.lastName;
}
const greeting = <h1>Hello, {formatName(user)}!</h1>;
```

<!-- .element: class="fragment" -->

---

## JSX 属性与样式

**使用驼峰命名**

```javascript
// HTML: class, onclick
// JSX: className, onClick

<div className="container" onClick={handleClick}>
  <button disabled={isDisabled}>点击</button>
</div>
```

<!-- .element: class="fragment" -->

**内联样式使用对象**

```javascript
const style = { color: 'red', fontSize: '20px' };
<h1 style={style}>标题</h1>
```

<!-- .element: class="fragment" -->

---

## 组件的两种定义方式

**函数组件（推荐）**

```javascript
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}
```

<!-- .element: class="fragment" -->

**类组件**

```javascript
class Welcome extends React.Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
}
```

<!-- .element: class="fragment" -->

现代 React 推荐使用**函数组件 + Hooks**

<!-- .element: class="fragment" -->

---

## 组件的使用

**组件名必须大写字母开头**

```javascript
// 定义组件
function Greeting() {
  return <h1>欢迎使用 React</h1>;
}

// 使用组件（像 HTML 标签一样）
function App() {
  return (
    <div>
      <Greeting />
      <Greeting />
    </div>
  );
}
```

<!-- .element: class="fragment" -->

---

## Props：组件间的数据传递

**Props = Properties（属性）**

<!-- .element: class="fragment" -->

父组件向子组件传递数据

<!-- .element: class="fragment" -->

```javascript
// 父组件
function App() {
  return <Welcome name="张三" age={25} />;
}

// 子组件
function Welcome(props) {
  return (
    <div>
      <h1>Hello, {props.name}</h1>
      <p>年龄: {props.age}</p>
    </div>
  );
}
```

<!-- .element: class="fragment" -->

---

## Props 的特点

**只读性（Read-Only）**
- 组件不能修改自己的 props
- 所有 React 组件都必须像纯函数一样保护它们的 props

<!-- .element: class="fragment" -->

```javascript
// ❌ 错误：不要修改 props
function Welcome(props) {
  props.name = '李四';  // 错误！
  return <h1>Hello, {props.name}</h1>;
}
```

<!-- .element: class="fragment" -->

---

## State：组件的内部状态

**State** 是组件的私有数据

<!-- .element: class="fragment" -->

使用 `useState` Hook 创建状态

<!-- .element: class="fragment" -->

```javascript
import { useState } from 'react';

function Counter() {
  // count: 状态变量
  // setCount: 更新状态的函数
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>当前计数: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        +1
      </button>
    </div>
  );
}
```

<!-- .element: class="fragment" -->

---

## State vs Props

| 特性 | State | Props |
|------|-------|-------|
| 数据来源 | 组件内部 | 父组件传递 |
| 可修改性 | 可修改 | 只读 |
| 使用场景 | 动态数据 | 配置数据 |

<!-- .element: class="fragment" -->

**核心原则**: Props 是组件的配置，State 是组件的记忆

<!-- .element: class="fragment" -->

---

## 事件处理

**使用驼峰命名 + 函数引用**

```javascript
function Button() {
  function handleClick() {
    alert('按钮被点击了！');
  }

  return (
    <button onClick={handleClick}>
      点击我
    </button>
  );
}
```

<!-- .element: class="fragment" -->

**传递参数**

```javascript
<button onClick={() => handleClick(id)}>删除</button>
```

<!-- .element: class="fragment" -->

---

## 阻止默认行为

**使用 `event.preventDefault()`**

```javascript
function Form() {
  function handleSubmit(e) {
    e.preventDefault();  // 阻止表单提交
    console.log('表单数据已处理');
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" />
      <button type="submit">提交</button>
    </form>
  );
}
```

<!-- .element: class="fragment" -->

---

## 条件渲染

**使用 `if` 语句**

```javascript
function Greeting({ isLoggedIn }) {
  if (isLoggedIn) {
    return <h1>欢迎回来！</h1>;
  }
  return <h1>请先登录</h1>;
}
```

<!-- .element: class="fragment" -->

**使用三元运算符**

```javascript
<div>
  {isLoggedIn ? <LogoutButton /> : <LoginButton />}
</div>
```

<!-- .element: class="fragment" -->

---

## 列表渲染

**使用 `map()` 方法**

```javascript
function TodoList() {
  const todos = ['学习 React', '编写代码', '发布项目'];

  return (
    <ul>
      {todos.map((todo, index) => (
        <li key={index}>{todo}</li>
      ))}
    </ul>
  );
}
```

<!-- .element: class="fragment" -->

**必须添加 `key` 属性**
- 帮助 React 识别哪些元素改变了
- 使用唯一且稳定的 ID

<!-- .element: class="fragment" -->

---

## Hooks 是什么？

**Hooks** 让函数组件拥有状态和生命周期

<!-- .element: class="fragment" -->

React 16.8 引入的新特性

<!-- .element: class="fragment" -->

**核心 Hooks**:
- `useState` - 状态管理
- `useEffect` - 副作用处理
- `useContext` - 共享数据

<!-- .element: class="fragment" -->

---

## useState Hook

**管理组件状态**

```javascript
import { useState } from 'react';

function Example() {
  // 声明状态变量
  const [count, setCount] = useState(0);
  const [name, setName] = useState('React');

  return (
    <div>
      <p>计数: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        增加
      </button>
    </div>
  );
}
```

<!-- .element: class="fragment" -->

---

## useEffect Hook

**处理副作用操作**

```javascript
import { useState, useEffect } from 'react';

function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    // 副作用：设置定时器
    const timer = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);

    // 清理函数
    return () => clearInterval(timer);
  }, []); // 空数组：仅在挂载时运行

  return <h1>运行时间: {count}秒</h1>;
}
```

<!-- .element: class="fragment" -->

---

## 实战：待办事项列表

```javascript
import { useState } from 'react';

function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  const addTodo = () => {
    setTodos([...todos, input]);
    setInput('');
  };

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={addTodo}>添加</button>
      <ul>
        {todos.map((todo, i) => <li key={i}>{todo}</li>)}
      </ul>
    </div>
  );
}
```

<!-- .element: class="fragment" -->

---

## 组件间数据共享

**通过提升状态（Lifting State Up）**

```javascript
function App() {
  const [data, setData] = useState('');

  return (
    <div>
      <Input value={data} onChange={setData} />
      <Display value={data} />
    </div>
  );
}

function Input({ value, onChange }) {
  return <input value={value} onChange={e => onChange(e.target.value)} />;
}

function Display({ value }) {
  return <p>输入内容: {value}</p>;
}
```

<!-- .element: class="fragment" -->

---

## React 开发最佳实践

**组件设计原则**
- 单一职责：一个组件只做一件事
- 可复用性：抽取通用组件
- Props 验证：使用 PropTypes 或 TypeScript

<!-- .element: class="fragment" -->

**性能优化**
- 避免不必要的渲染
- 使用 React.memo 缓存组件
- 合理使用 useCallback 和 useMemo

<!-- .element: class="fragment" -->

---

## 学习资源推荐

**官方文档**
- [React 中文文档](https://zh-hans.react.dev/)
- [React 英文文档](https://react.dev/)

<!-- .element: class="fragment" -->

**开发工具**
- React DevTools（浏览器扩展）
- Create React App 脚手架
- Vite（更快的构建工具）

<!-- .element: class="fragment" -->

**实践项目**
- 井字棋游戏（官方教程）
- 个人博客
- 电商购物车

<!-- .element: class="fragment" -->

---

## 下一步学习方向

**进阶主题**
- React Router（路由管理）
- Redux/Zustand（状态管理）
- React Query（数据获取）

<!-- .element: class="fragment" -->

**生态系统**
- Next.js（全栈框架）
- React Native（移动开发）
- TypeScript（类型安全）

<!-- .element: class="fragment" -->

---

## 总结

**核心概念回顾**
1. React 是声明式、组件化的 UI 库
2. JSX 让我们在 JavaScript 中编写 UI
3. Props 用于组件通信，State 用于状态管理
4. Hooks 让函数组件更强大
5. 虚拟 DOM 保证高性能

<!-- .element: class="fragment" -->

**记住**: 多练习、多实践、多查文档！

<!-- .element: class="fragment" -->

---

# 感谢观看！

开始你的 React 之旅吧 🚀

**问题交流时间**
