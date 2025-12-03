# Python 缺陷检测规则

## 规则概览

支持检测 8 类常见缺陷,按严重度分级:

- 🔴 **Blocker**(阻断级): SQL注入、命令注入、敏感信息泄露
- 🟠 **Critical**(严重级): 资源泄漏、不安全的反序列化
- 🟡 **Major**(重要级): 异常处理不当、类型错误、并发问题
- 🟢 **Minor**(次要级): N+1查询、性能问题

---

## 🔴 Blocker - 阻断级

### 1. SQL 注入

**风险等级**: 🔴 Blocker (10分)

**描述**: 使用字符串拼接或格式化构造 SQL 语句,存在 SQL 注入风险。

**危险模式**:

```python
# 模式 1: 使用 f-string 或 % 格式化
user_id = request.args.get("id")
query = f"SELECT * FROM users WHERE id = {user_id}"  # ❌ SQL注入
cursor.execute(query)

# 模式 2: 使用 + 拼接
name = request.json.get("name")
query = "SELECT * FROM users WHERE name = '" + name + "'"  # ❌
cursor.execute(query)

# 模式 3: 使用 .format()
order_by = request.args.get("sort")
query = "SELECT * FROM products ORDER BY {}".format(order_by)  # ❌
cursor.execute(query)

# 模式 4: Django ORM raw query
User.objects.raw(f"SELECT * FROM user WHERE name = '{name}'")  # ❌
```

**攻击示例**:

```python
# 输入: id = "1 OR 1=1"
# 执行: SELECT * FROM users WHERE id = 1 OR 1=1
# 结果: 返回所有用户

# 输入: name = "'; DROP TABLE users--"
# 执行: SELECT * FROM users WHERE name = ''; DROP TABLE users--'
# 结果: 删除表
```

**检测方法**:

Level 1 - 文本匹配:

```bash
git diff HEAD~3..HEAD | grep -E '(execute|raw).*f"|\.format\(|"\s*\+\s*'
```

Level 2 - Serena MCP:

```
查询: "查找所有使用 f-string 或字符串拼接构造 SQL 的代码"
查询: "查找包含 cursor.execute 且参数包含变量拼接的代码"
```

**安全示例**:

```python
# ✅ 使用参数化查询 (pymysql, psycopg2)
user_id = request.args.get("id")
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))

# ✅ SQLAlchemy 参数绑定
from sqlalchemy import text
query = text("SELECT * FROM users WHERE name = :name")
result = session.execute(query, {"name": name})

# ✅ Django ORM 查询
User.objects.filter(name=name)

# ✅ 动态 ORDER BY 白名单
ALLOWED_SORT = {"name", "price", "created_at"}
order_by = request.args.get("sort", "id")
if order_by not in ALLOWED_SORT:
    raise ValueError("Invalid sort field")
query = f"SELECT * FROM products ORDER BY {order_by}"  # 白名单验证后安全
```

**修复建议**:

1. 使用参数化查询 (`%s`, `?`, `:name`)
2. 使用 ORM (Django ORM, SQLAlchemy)
3. 动态字段使用白名单验证

**参考**: OWASP A03:2021 - Injection

---

### 2. 命令注入

**风险等级**: 🔴 Blocker (10分)

**描述**: 使用用户输入构造系统命令,存在命令注入风险。

**危险模式**:

```python
# 模式 1: os.system 直接拼接
filename = request.args.get("file")
os.system(f"cat {filename}")  # ❌ 命令注入

# 模式 2: subprocess.run shell=True
import subprocess
user_input = request.json.get("command")
subprocess.run(f"echo {user_input}", shell=True)  # ❌

# 模式 3: eval/exec 执行用户输入
code = request.json.get("code")
eval(code)  # ❌ 代码注入
exec(code)  # ❌
```

**攻击示例**:

```python
# 输入: filename = "test.txt; rm -rf /"
# 执行: cat test.txt; rm -rf /
# 结果: 删除系统文件

# 输入: code = "__import__('os').system('rm -rf /')"
# 执行: eval 执行任意代码
# 结果: 系统破坏
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -E '(os\.system|subprocess.*shell=True|eval|exec)\s*\('
```

Serena MCP:

```
查询: "查找所有调用 os.system, subprocess 且 shell=True, eval, exec 的代码"
```

**安全示例**:

```python
# ✅ subprocess 不使用 shell, 参数列表
filename = request.args.get("file")
subprocess.run(["cat", filename])  # 参数分离,无法注入

# ✅ 使用安全的 API
import pathlib
file_path = pathlib.Path(filename)
if file_path.exists():
    content = file_path.read_text()

# ✅ 白名单验证
ALLOWED_COMMANDS = {"ls", "pwd", "date"}
command = request.args.get("cmd")
if command not in ALLOWED_COMMANDS:
    raise ValueError("Invalid command")

# ❌ 永远不要用 eval/exec 处理用户输入
# 使用 ast.literal_eval 安全解析
import ast
data = request.json.get("data")
parsed = ast.literal_eval(data)  # 只能解析字面量
```

**修复建议**:

1. 使用 `subprocess` 参数列表形式 (不用 `shell=True`)
2. 禁止 `eval`/`exec` 处理用户输入
3. 使用白名单验证命令
4. 使用安全的 Python API 替代系统命令

**参考**: OWASP A03:2021 - Injection

---

### 3. 敏感信息泄露

**风险等级**: 🔴 Blocker (10分)

**描述**: 硬编码密码、密钥、Token 等敏感信息。

**危险模式**:

```python
# 模式 1: 硬编码数据库密码
DATABASE_URL = "postgresql://user:password123@localhost/db"  # ❌

# 模式 2: 硬编码 API 密钥
API_KEY = "sk_live_abc123def456"  # ❌
headers = {"Authorization": f"Bearer {API_KEY}"}

# 模式 3: 硬编码加密密钥
from cryptography.fernet import Fernet
SECRET_KEY = b"my_secret_key_12345678901234567890"  # ❌
cipher = Fernet(SECRET_KEY)

# 模式 4: JWT 密钥硬编码
JWT_SECRET = "super_secret_key"  # ❌
token = jwt.encode(payload, JWT_SECRET)
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -iE '(password|api_key|secret|token)\s*=\s*["\']'
```

Serena MCP:

```
查询: "查找所有包含 password/api_key/secret/token 赋值为字符串字面量的代码"
```

**安全示例**:

```python
# ✅ 使用环境变量
import os
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")

# ✅ 使用配置文件 (.env) + python-dotenv
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ✅ 使用密钥管理服务
import boto3
secrets = boto3.client("secretsmanager")
db_password = secrets.get_secret_value(SecretId="db-password")["SecretString"]

# ✅ .gitignore 排除配置文件
# .gitignore:
# .env
# config.ini
# secrets.yaml
```

**修复建议**:

1. 使用环境变量或 `.env` 文件 (不提交到 Git)
2. 使用密钥管理服务 (AWS Secrets Manager, HashiCorp Vault)
3. 在 `.gitignore` 中排除配置文件

**参考**: OWASP A02:2021 - Cryptographic Failures

---

## 🟠 Critical - 严重级

### 4. 资源泄漏

**风险等级**: 🟠 Critical (5分)

**描述**: 文件、数据库连接、网络连接等资源未正确关闭。

**危险模式**:

```python
# 模式 1: 文件未关闭
file = open("data.txt", "r")
content = file.read()
# ❌ 未关闭文件

# 模式 2: 数据库连接未关闭
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
cursor.execute(query)
# ❌ 未关闭连接

# 模式 3: HTTP 连接未关闭
import requests
response = requests.get(url)
# ❌ 未关闭会话
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -E 'open\(|connect\(' | grep -v 'with\s'
```

Serena MCP:

```
查询: "查找所有调用 open, connect 但未使用 with 语句的代码"
```

**安全示例**:

```python
# ✅ 使用 with 语句 (context manager)
with open("data.txt", "r") as file:
    content = file.read()
# 自动关闭

# ✅ 数据库连接
with psycopg2.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

# ✅ HTTP 会话管理
with requests.Session() as session:
    response = session.get(url)
    data = response.json()

# ✅ 使用 pathlib (推荐)
from pathlib import Path
content = Path("data.txt").read_text()
```

**修复建议**:

1. 使用 `with` 语句自动管理资源
2. 使用 `pathlib` 等高级 API
3. 实现自定义 context manager (`__enter__`, `__exit__`)

---

### 5. 不安全的反序列化

**风险等级**: 🟠 Critical (5分)

**描述**: 使用 `pickle.loads` 反序列化不可信数据,可执行任意代码。

**危险模式**:

```python
# 模式 1: pickle 反序列化用户输入
import pickle
data = request.get_data()
obj = pickle.loads(data)  # ❌ 可执行任意代码

# 模式 2: yaml.load 不安全模式
import yaml
config = yaml.load(file)  # ❌ 使用 FullLoader

# 模式 3: marshal 反序列化
import marshal
code = request.get_data()
marshal.loads(code)  # ❌
```

**攻击示例**:

```python
# 攻击者构造恶意 pickle 数据
import pickle
import os

class Exploit:
    def __reduce__(self):
        return (os.system, ('rm -rf /',))

malicious_data = pickle.dumps(Exploit())
# 受害者反序列化时执行 rm -rf /
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -E '(pickle\.loads|yaml\.load|marshal\.loads)'
```

Serena MCP:

```
查询: "查找所有调用 pickle.loads, yaml.load, marshal.loads 的代码"
```

**安全示例**:

```python
# ✅ 使用 JSON (安全但功能有限)
import json
data = json.loads(request.get_data())

# ✅ 使用 yaml.safe_load
import yaml
config = yaml.safe_load(file)  # 只加载基本类型

# ✅ 限制 pickle (如果必须使用)
import pickle
import io

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # 白名单允许的类
        if module == "myapp.models" and name in {"User", "Order"}:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"Forbidden class: {module}.{name}")

data = RestrictedUnpickler(io.BytesIO(request.get_data())).load()
```

**修复建议**:

1. 优先使用 JSON、MessagePack 等安全格式
2. YAML 使用 `safe_load` 而非 `load`
3. 必须使用 pickle 时实现白名单限制

**参考**: OWASP A08:2021 - Software and Data Integrity Failures

---

## 🟡 Major - 重要级

### 6. 异常处理不当

**风险等级**: 🟡 Major (2分)

**描述**: 捕获异常后吞没或暴露敏感信息。

**危险模式**:

```python
# 模式 1: 空 except 块
try:
    process_order(order)
except Exception:
    pass  # ❌ 完全吞没异常

# 模式 2: 裸 except
try:
    data = json.loads(content)
except:  # ❌ 捕获所有异常包括 KeyboardInterrupt
    pass

# 模式 3: 暴露敏感信息
try:
    conn = psycopg2.connect(db_url)
except Exception as e:
    return jsonify({"error": str(e)}), 500  # ❌ 可能暴露数据库连接串

# 模式 4: 捕获但不处理
try:
    result = api_call()
except RequestException as e:
    print(e)  # ❌ 仅打印,未处理
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -A2 "except" | grep -E "(pass|print)"
```

Serena MCP:

```
查询: "查找所有 except 块只包含 pass 或 print 的代码"
查询: "查找所有裸 except (不指定异常类型) 的代码"
```

**安全示例**:

```python
# ✅ 重新抛出
try:
    process_order(order)
except OrderException as e:
    logger.error(f"Order processing failed: {order.id}", exc_info=True)
    raise

# ✅ 指定异常类型
try:
    data = json.loads(content)
except json.JSONDecodeError as e:
    logger.error("Invalid JSON", exc_info=True)
    raise ValidationError("Invalid JSON format")

# ✅ 错误信息脱敏
try:
    conn = psycopg2.connect(db_url)
except psycopg2.OperationalError:
    logger.error("Database connection failed", exc_info=True)
    return jsonify({"error": "Database unavailable"}), 500  # 不暴露细节

# ✅ 合理处理
try:
    result = api_call()
except RequestException as e:
    logger.error("API call failed", exc_info=True)
    # 回退方案
    return get_cached_result()
```

**修复建议**:

1. 指定具体的异常类型,避免裸 `except`
2. 记录日志后重新抛出或提供回退方案
3. 对外错误信息脱敏,避免暴露实现细节
4. 使用 `logger.exception()` 或 `exc_info=True` 记录堆栈

---

### 7. 类型错误

**风险等级**: 🟡 Major (2分)

**描述**: 类型注解缺失或不正确,导致运行时类型错误。

**危险模式**:

```python
# 模式 1: 缺少类型注解
def calculate_total(items):  # ❌ 参数类型不明确
    return sum(item["price"] for item in items)

# 模式 2: 返回值类型不明确
def get_user(user_id):  # ❌ 返回 User? None? 不清楚
    return db.query(User).filter_by(id=user_id).first()

# 模式 3: Any 滥用
from typing import Any
def process(data: Any) -> Any:  # ❌ 失去类型检查
    return data.process()

# 模式 4: 类型不一致
def add_numbers(a: int, b: int) -> int:
    return str(a + b)  # ❌ 返回 str 而非 int
```

**检测方法**:

```bash
# 使用 mypy 静态类型检查
mypy --strict .
```

Serena MCP:

```
查询: "查找所有函数定义但缺少类型注解的代码"
查询: "查找所有使用 Any 类型的代码"
```

**安全示例**:

```python
# ✅ 完整类型注解
from typing import List, Dict, Optional

def calculate_total(items: List[Dict[str, float]]) -> float:
    return sum(item["price"] for item in items)

# ✅ Optional 表示可空
def get_user(user_id: int) -> Optional[User]:
    return db.query(User).filter_by(id=user_id).first()

# ✅ 使用具体类型
from pydantic import BaseModel

class RequestData(BaseModel):
    name: str
    age: int

def process(data: RequestData) -> Dict[str, str]:
    return {"message": f"Hello {data.name}"}

# ✅ 使用 TypeGuard
from typing import TypeGuard

def is_user_dict(data: dict) -> TypeGuard[Dict[str, Any]]:
    return "id" in data and "name" in data
```

**修复建议**:

1. 为所有公共函数添加类型注解
2. 使用 `mypy` 或 `pyright` 静态类型检查
3. 使用 `Pydantic` 进行运行时类型验证
4. 避免使用 `Any`,使用具体类型或 `TypeVar`

---

### 8. 并发问题

**风险等级**: 🟡 Major (2分)

**描述**: 多线程/异步环境下的竞态条件、共享状态问题。

**危险模式**:

```python
# 模式 1: 共享状态竞态条件
counter = 0

def increment():
    global counter
    counter += 1  # ❌ 非原子操作

# 模式 2: 非线程安全的数据结构
cache = {}  # ❌ dict 非线程安全

def get_cached(key):
    if key not in cache:
        cache[key] = fetch_data(key)
    return cache[key]

# 模式 3: asyncio 中使用阻塞调用
import asyncio
import time

async def process():
    time.sleep(10)  # ❌ 阻塞事件循环
    return "done"

# 模式 4: 共享资源无锁保护
class Database:
    def __init__(self):
        self.connection = None

    def query(self, sql):
        if not self.connection:
            self.connection = create_connection()  # ❌ 竞态条件
        return self.connection.execute(sql)
```

**检测方法**:

Serena MCP:

```
查询: "查找所有使用 global 关键字的代码"
查询: "查找所有在 async 函数中调用阻塞函数的代码"
```

**安全示例**:

```python
# ✅ 使用线程安全的原子操作
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    with lock:
        counter += 1

# ✅ 使用线程安全的数据结构
from threading import Lock
from typing import Dict

class ThreadSafeCache:
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._lock = Lock()

    def get(self, key: str):
        with self._lock:
            if key not in self._cache:
                self._cache[key] = fetch_data(key)
            return self._cache[key]

# ✅ asyncio 使用非阻塞调用
import asyncio

async def process():
    await asyncio.sleep(10)  # 非阻塞
    return "done"

# ✅ 异步 HTTP 客户端
import httpx

async def fetch(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# ✅ 使用锁保护共享资源
import asyncio

class Database:
    def __init__(self):
        self.connection = None
        self._lock = asyncio.Lock()

    async def query(self, sql):
        async with self._lock:
            if not self.connection:
                self.connection = await create_connection()
            return await self.connection.execute(sql)
```

**修复建议**:

1. 使用 `threading.Lock` 或 `asyncio.Lock` 保护共享状态
2. 使用线程安全的数据结构 (Queue, ThreadSafeCache)
3. asyncio 中使用 `await` 和非阻塞 API
4. 避免全局可变状态,使用依赖注入

---

## 🟢 Minor - 次要级

### 9. N+1 查询问题

**风险等级**: 🟢 Minor (1分)

**描述**: 循环中执行数据库查询,导致性能问题。

**危险模式**:

```python
# 模式 1: 循环查询
orders = Order.query.all()
for order in orders:
    user = User.query.get(order.user_id)  # ❌ N+1
    order.user_name = user.name

# 模式 2: SQLAlchemy 懒加载
class Order(Base):
    user = relationship("User", lazy="select")

orders = session.query(Order).all()
for order in orders:
    print(order.user.name)  # ❌ 触发 N 次查询

# 模式 3: Django ORM
orders = Order.objects.all()
for order in orders:
    print(order.user.name)  # ❌ N+1
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -E 'for.*in' -A5 | grep -E '\.query\.|\.get\('
```

Serena MCP:

```
查询: "查找所有在循环内调用数据库查询方法的代码"
```

**安全示例**:

```python
# ✅ SQLAlchemy joinedload
from sqlalchemy.orm import joinedload

orders = session.query(Order).options(joinedload(Order.user)).all()
for order in orders:
    print(order.user.name)  # 无额外查询

# ✅ Django select_related (ForeignKey)
orders = Order.objects.select_related("user").all()
for order in orders:
    print(order.user.name)

# ✅ Django prefetch_related (ManyToMany)
orders = Order.objects.prefetch_related("items").all()
for order in orders:
    print([item.name for item in order.items.all()])

# ✅ 批量查询
orders = Order.query.all()
user_ids = [order.user_id for order in orders]
users = {u.id: u for u in User.query.filter(User.id.in_(user_ids)).all()}
for order in orders:
    order.user_name = users[order.user_id].name
```

**修复建议**:

1. 使用 `joinedload` (SQLAlchemy) 或 `select_related` (Django)
2. 使用 `prefetch_related` (Django) 处理多对多
3. 批量查询 + 字典缓存

---

## 功能缺陷检测

与 Java 相同,需要验证需求实现情况:

### 功能完全缺失 (CRITICAL)

需求明确要求的功能在代码中完全找不到。

**示例**:

需求: "用户注册成功后,发送欢迎邮件"

```python
# ❌ 缺失发送邮件功能
@app.post("/register")
async def register(user: UserCreate):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    return {"message": "注册成功"}
```

### 功能实现不完整 (HIGH)

功能部分实现,但缺少关键逻辑分支或边界条件处理。

**示例**:

需求: "支持邮箱和手机号两种注册方式"

```python
# ❌ 只实现了邮箱注册
def register(credential: str, password: str):
    if "@" in credential:
        return create_user_by_email(credential, password)
    # 缺少手机号注册分支
    raise ValueError("Unsupported registration method")
```

### 业务逻辑错误 (CRITICAL)

代码实现与需求描述的业务流程矛盾。

**示例**:

需求: "订单支付流程: 1.验证库存 2.扣减库存 3.创建订单"

```python
# ❌ 流程顺序错误
async def create_order(items: List[Item]):
    order = await order_repo.create(items)  # 先创建订单
    await inventory_repo.deduct(items)  # 后扣减库存
    # 如果扣减失败,订单已创建 → 数据不一致
```

---

## 检测优先级汇总

| 缺陷类型 | 严重程度 | 分数 | 影响 | 检测关键词 |
|---------|---------|------|------|-----------|
| SQL 注入 | 🔴 Blocker | 10 | 数据泄露 | f-string + SQL, .format() |
| 命令注入 | 🔴 Blocker | 10 | 系统破坏 | os.system, eval, exec |
| 敏感信息泄露 | 🔴 Blocker | 10 | 凭证泄露 | password/key = "..." |
| 资源泄漏 | 🟠 Critical | 5 | 资源耗尽 | open() without with |
| 不安全反序列化 | 🟠 Critical | 5 | 代码执行 | pickle.loads, yaml.load |
| 异常处理不当 | 🟡 Major | 2 | 隐藏错误 | except: pass |
| 类型错误 | 🟡 Major | 2 | 运行时崩溃 | Missing type hints |
| 并发问题 | 🟡 Major | 2 | 数据不一致 | Global state, race condition |
| N+1 查询 | 🟢 Minor | 1 | 性能下降 | Loop + query |

**风险分数计算**: `Blocker×10 + Critical×5 + Major×2 + Minor×1`

---

## 参考资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Bandit - Python Security Linter](https://bandit.readthedocs.io/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [SQLAlchemy Security](https://docs.sqlalchemy.org/en/20/faq/security.html)

---

**版本**: 1.0.0
**创建**: 2025-11-08
