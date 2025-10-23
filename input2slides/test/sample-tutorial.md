# TypeScript 泛型完全指南

泛型是 TypeScript 最强大的特性之一，它允许我们编写可重用的组件，同时保持类型安全。

## 为什么需要泛型？

在没有泛型的情况下，我们必须为每种类型编写重复的代码，或者使用 `any` 类型而失去类型检查。

### 问题示例

```typescript
function identity(arg: any): any {
  return arg;
}

// 失去了类型信息
const result = identity("hello"); // result 是 any 类型
```

## 泛型基础

### 基本语法

泛型使用尖括号 `<T>` 来定义类型参数。

```typescript
function identity<T>(arg: T): T {
  return arg;
}

// 使用时可以显式指定类型
const result1 = identity<string>("hello"); // result1: string

// 或让 TypeScript 自动推断
const result2 = identity(42); // result2: number
```

### 泛型接口

```typescript
interface GenericIdentityFn<T> {
  (arg: T): T;
}

const myIdentity: GenericIdentityFn<number> = identity;
```

## 泛型约束

有时我们需要限制泛型的类型范围。

### extends 关键字

```typescript
interface Lengthwise {
  length: number;
}

function loggingIdentity<T extends Lengthwise>(arg: T): T {
  console.log(arg.length); // 现在可以安全访问 .length
  return arg;
}

loggingIdentity("hello"); // ✅ string 有 length
loggingIdentity([1, 2, 3]); // ✅ array 有 length
loggingIdentity(42); // ❌ number 没有 length
```

## 泛型类

类也可以使用泛型。

```typescript
class GenericNumber<T> {
  zeroValue: T;
  add: (x: T, y: T) => T;
}

const myGenericNumber = new GenericNumber<number>();
myGenericNumber.zeroValue = 0;
myGenericNumber.add = (x, y) => x + y;
```

## 实战应用

### 类型安全的数组操作

```typescript
function firstElement<T>(arr: T[]): T | undefined {
  return arr[0];
}

const numbers = [1, 2, 3];
const first = firstElement(numbers); // first: number | undefined

const strings = ["a", "b", "c"];
const firstStr = firstElement(strings); // firstStr: string | undefined
```

### 多个类型参数

```typescript
function pair<T, U>(first: T, second: U): [T, U] {
  return [first, second];
}

const result = pair("hello", 42); // result: [string, number]
```

## 常见模式

### 工厂函数

```typescript
function create<T>(constructor: new () => T): T {
  return new constructor();
}

class MyClass {
  constructor() {
    console.log("Created!");
  }
}

const instance = create(MyClass); // instance: MyClass
```

### 映射类型

```typescript
type Partial<T> = {
  [P in keyof T]?: T[P];
};

interface Todo {
  title: string;
  description: string;
}

type PartialTodo = Partial<Todo>;
// {
//   title?: string;
//   description?: string;
// }
```

## 最佳实践

1. **使用有意义的类型参数名**: `T` 适合单一类型，多个时用 `T`, `U`, `V` 或语义化名称如 `TKey`, `TValue`

2. **避免过度使用泛型**: 只在需要类型参数化时使用

3. **优先推断**: 让 TypeScript 自动推断类型，避免不必要的显式类型注解

4. **使用约束**: 当需要访问类型的特定属性时，使用 `extends` 约束

## 总结

泛型让 TypeScript 既灵活又类型安全：

- ✅ 代码重用
- ✅ 类型安全
- ✅ 自动推断
- ✅ 编译时检查

掌握泛型是成为 TypeScript 高手的必经之路！
