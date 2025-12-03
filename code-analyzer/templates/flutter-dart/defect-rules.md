# Flutter + Dart 缺陷检测规则

针对 **MagicFrame App** 项目,基于 GetX 架构模式的缺陷检测规则。

## 规则概览

按严重度分级:

- 🔴 **Blocker**(阻断级): 安全漏洞、内存泄漏
- 🟠 **Critical**(严重级): 性能问题、状态管理错误
- 🟡 **Major**(重要级): 资源泄漏、错误处理
- 🟢 **Minor**(次要级): 代码质量、最佳实践

---

## 🔴 Blocker - 阻断级

### 1. 敏感信息泄露

**风险等级**: 🔴 Blocker (10分)

**描述**: 硬编码 API Key、密码、Token 等敏感信息。

**危险模式**:

```dart
// 模式 1: 硬编码 API Key
class ApiConfig {
  static const String apiKey = "sk_live_123456789abcdef";
  static const String firebaseKey = "AIzaSyB1234567890";
}

// 模式 2: 硬编码密码
final dio = Dio()..options.headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
};

// 模式 3: SharedPreferences 明文存储敏感信息
await prefs.setString('password', userPassword);
await prefs.setString('credit_card', cardNumber);
```

**攻击风险**:
- APK 反编译可直接获取密钥
- 用户数据泄露
- 账号被盗用

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E '(apiKey|API_KEY|password|token|secret|private.*key).*=.*["\']'

# Level 2 - Serena MCP
查询: "查找所有包含 apiKey, password, token 的常量定义"
查询: "查找 SharedPreferences 存储密码或 token 的代码"
```

**安全示例**:

```dart
// ✅ 使用环境变量
class ApiConfig {
  static String get apiKey => const String.fromEnvironment('API_KEY');
  static String get firebaseKey => const String.fromEnvironment('FIREBASE_KEY');
}

// ✅ 使用 flutter_secure_storage 存储敏感信息
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

final storage = FlutterSecureStorage();
await storage.write(key: 'token', value: userToken);
final token = await storage.read(key: 'token');

// ✅ 使用 Hive 加密盒子
import 'package:hive/hive.dart';

final encryptionKey = Hive.generateSecureKey();
final encryptedBox = await Hive.openBox('vault',
  encryptionCipher: HiveAesCipher(encryptionKey));
```

**修复建议**:
1. 敏感配置使用 `--dart-define` 环境变量
2. Token 使用 `flutter_secure_storage` 存储
3. Hive 敏感数据使用加密盒子

**参考**: OWASP Mobile Top 10 - M2: Insecure Data Storage

---

### 2. HTTP 明文传输敏感数据

**风险等级**: 🔴 Blocker (10分)

**描述**: 使用 HTTP 而非 HTTPS 传输敏感信息。

**危险模式**:

```dart
// 模式 1: HTTP URL
final dio = Dio(BaseOptions(
  baseUrl: 'http://api.example.com',  // ❌ HTTP
));

// 模式 2: 混合使用 HTTP/HTTPS
const String imageUrl = 'http://cdn.example.com/image.jpg';

// 模式 3: 允许自签名证书(生产环境)
(dio.httpClientAdapter as DefaultHttpClientAdapter).onHttpClientCreate = (client) {
  client.badCertificateCallback = (cert, host, port) => true;  // ❌
};
```

**攻击风险**:
- 中间人攻击窃取数据
- 用户凭证被拦截
- 数据篡改

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'http://|badCertificateCallback.*true'

# Level 2 - Serena MCP
查询: "查找所有使用 http:// 协议的 URL"
查询: "查找 badCertificateCallback 返回 true 的代码"
```

**安全示例**:

```dart
// ✅ 使用 HTTPS
final dio = Dio(BaseOptions(
  baseUrl: 'https://api.example.com',
));

// ✅ 仅开发环境允许自签名证书
(dio.httpClientAdapter as DefaultHttpClientAdapter).onHttpClientCreate = (client) {
  if (kDebugMode) {
    client.badCertificateCallback = (cert, host, port) => true;
  }
};

// ✅ 生产环境强制 HTTPS
import 'package:dio/adapter.dart';

void setupDio(Dio dio) {
  if (kReleaseMode) {
    // 生产环境禁用不安全证书
    (dio.httpClientAdapter as DefaultHttpClientAdapter).onHttpClientCreate = null;
  }
}
```

**修复建议**:
1. 所有 API 请求使用 HTTPS
2. CDN 资源使用 HTTPS
3. 生产环境禁止信任所有证书

---

### 3. 不安全的 WebView 配置

**风险等级**: 🔴 Blocker (10分)

**描述**: WebView 启用不安全的 JavaScript 交互。

**危险模式**:

```dart
// 模式 1: 允许执行任意 JavaScript
WebView(
  javascriptMode: JavascriptMode.unrestricted,
  onWebViewCreated: (controller) {
    controller.runJavascript('alert(document.cookie)');  // ❌
  },
)

// 模式 2: 未验证 URL 就加载
WebView(
  initialUrl: userInputUrl,  // ❌ 用户输入未验证
)

// 模式 3: 允许 file:// 访问本地文件
WebView(
  initialUrl: 'file:///data/user/0/com.app/files/sensitive.txt',  // ❌
)
```

**攻击风险**:
- XSS 攻击
- 访问本地敏感文件
- 窃取用户数据

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'javascriptMode.*unrestricted|runJavascript|file:///'

# Level 2 - Serena MCP
查询: "查找 WebView javascriptMode 设置为 unrestricted 的代码"
查询: "查找 WebView 加载 file:// URL 的代码"
```

**安全示例**:

```dart
// ✅ 验证 URL 白名单
class WebViewPage extends StatelessWidget {
  final String url;

  bool _isUrlSafe(String url) {
    final allowedDomains = ['example.com', 'trusted.com'];
    final uri = Uri.tryParse(url);
    return uri != null &&
           uri.scheme == 'https' &&
           allowedDomains.any((domain) => uri.host.endsWith(domain));
  }

  @override
  Widget build(BuildContext context) {
    if (!_isUrlSafe(url)) {
      return ErrorPage('Unsafe URL');
    }

    return WebView(
      initialUrl: url,
      javascriptMode: JavascriptMode.disabled,  // 默认禁用
    );
  }
}

// ✅ 安全的 JavaScript 通道
WebView(
  javascriptMode: JavascriptMode.unrestricted,
  javascriptChannels: {
    JavascriptChannel(
      name: 'FlutterBridge',
      onMessageReceived: (JavascriptMessage message) {
        // 验证消息来源和内容
        if (_isMessageValid(message.message)) {
          handleMessage(message.message);
        }
      },
    ),
  },
)
```

**修复建议**:
1. 验证 URL 白名单
2. 仅信任域名启用 JavaScript
3. 禁止 `file://` 协议访问

---

## 🟠 Critical - 严重级

### 4. GetX Controller 内存泄漏

**风险等级**: 🟠 Critical (8分)

**描述**: GetX Controller 中订阅未正确释放,导致内存泄漏。

**危险模式**:

```dart
// 模式 1: Stream 订阅未释放
class MyController extends GetxController {
  StreamSubscription? _subscription;

  @override
  void onInit() {
    _subscription = someStream.listen((data) {
      // 处理数据
    });
    // ❌ onClose 中未取消订阅
  }
}

// 模式 2: Timer 未取消
class MyController extends GetxController {
  Timer? _timer;

  @override
  void onInit() {
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      // 执行任务
    });
    // ❌ onClose 中未取消 Timer
  }
}

// 模式 3: Repository 未清理
class MyController extends BaseController<MyRepository> {
  MyController(MyRepository repository) : super(repository);

  // ❌ 未调用 repository.onClear()
}
```

**影响**:
- 内存持续增长
- 应用卡顿
- OOM 崩溃

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E '\.listen\(|Timer\.periodic|StreamSubscription'

# Level 2 - Serena MCP
查询: "查找所有 GetxController 中有 Stream 订阅但 onClose 中未取消的代码"
查询: "查找所有使用 Timer.periodic 但未在 onClose 中取消的代码"
```

**安全示例**:

```dart
// ✅ 正确释放订阅
class MyController extends GetxController {
  StreamSubscription? _subscription;
  Timer? _timer;

  @override
  void onInit() {
    super.onInit();
    _subscription = someStream.listen((data) {
      handleData(data);
    });

    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      doSomething();
    });
  }

  @override
  void onClose() {
    _subscription?.cancel();
    _timer?.cancel();
    super.onClose();
  }
}

// ✅ BaseController 正确调用 repository.onClear()
class MyController extends BaseController<MyRepository> {
  MyController(MyRepository repository) : super(repository);

  @override
  void onClose() {
    repository.onClear();  // ✅
    super.onClose();
  }
}
```

**修复建议**:
1. `onClose()` 中取消所有订阅
2. 使用 `ever()` 等 GetX 响应式方法(自动管理)
3. BaseController 中必须调用 `repository.onClear()`

---

### 5. 不必要的 Widget rebuild

**风险等级**: 🟠 Critical (7分)

**描述**: 未使用 `const` 构造函数或 `Obx` 导致大量重建。

**危险模式**:

```dart
// 模式 1: 未使用 const
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Title'),  // ❌ 应该是 const Text
      ),
      body: Column(
        children: [
          Icon(Icons.home),  // ❌ 应该是 const Icon
        ],
      ),
    );
  }
}

// 模式 2: GetBuilder 范围过大
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GetBuilder<MyController>(
      builder: (controller) {
        return Scaffold(  // ❌ 整个页面都会重建
          appBar: AppBar(title: Text('Title')),
          body: Column(
            children: [
              Text('Static content'),
              Text(controller.dynamicText.value),
            ],
          ),
        );
      },
    );
  }
}

// 模式 3: 列表 itemBuilder 中创建 Controller
ListView.builder(
  itemBuilder: (context, index) {
    final controller = Get.find<MyController>();  // ❌ 每次都查找
    return ListTile(title: Text(controller.items[index]));
  },
)
```

**影响**:
- 性能下降
- UI 卡顿
- 电量消耗

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'Text\(|Icon\(|Container\(' | grep -v 'const'

# Level 2 - Serena MCP
查询: "查找所有 StatelessWidget 中未使用 const 的静态 Widget"
查询: "查找 GetBuilder 包裹整个 Scaffold 的代码"
```

**安全示例**:

```dart
// ✅ 使用 const
class MyPage extends StatelessWidget {
  const MyPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Title'),  // ✅
      ),
      body: Column(
        children: const [
          Icon(Icons.home),  // ✅
        ],
      ),
    );
  }
}

// ✅ 最小化响应式范围
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Title')),
      body: Column(
        children: [
          const Text('Static content'),  // ✅ 不会重建
          Obx(() {  // ✅ 仅包裹动态部分
            final controller = Get.find<MyController>();
            return Text(controller.dynamicText.value);
          }),
        ],
      ),
    );
  }
}

// ✅ 列表外部获取 Controller
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final controller = Get.find<MyController>();  // ✅
    return ListView.builder(
      itemBuilder: (context, index) {
        return ListTile(title: Text(controller.items[index]));
      },
    );
  }
}
```

**修复建议**:
1. 静态 Widget 使用 `const` 构造函数
2. 最小化 `GetBuilder`/`Obx` 包裹范围
3. Controller 在 build 外部获取

---

### 6. Dio 请求未处理错误

**风险等级**: 🟠 Critical (7分)

**描述**: Dio 请求缺少错误处理,导致崩溃或用户体验差。

**危险模式**:

```dart
// 模式 1: 未 try-catch
Future<void> fetchData() async {
  final response = await dio.get('/api/data');  // ❌ 网络错误会崩溃
  handleData(response.data);
}

// 模式 2: 吞没异常
Future<void> fetchData() async {
  try {
    final response = await dio.get('/api/data');
    handleData(response.data);
  } catch (e) {
    // ❌ 什么都不做
  }
}

// 模式 3: 未处理特定错误类型
Future<void> fetchData() async {
  try {
    final response = await dio.get('/api/data');
    handleData(response.data);
  } catch (e) {
    showError('Network error');  // ❌ 未区分错误类型
  }
}
```

**影响**:
- 应用崩溃
- 用户体验差
- 无法追踪错误

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'dio\.(get|post|put|delete)' | grep -v 'try'

# Level 2 - Serena MCP
查询: "查找所有 dio 请求未包裹在 try-catch 中的代码"
查询: "查找 catch 块为空的异步方法"
```

**安全示例**:

```dart
// ✅ 完整错误处理
Future<ApiResult<T>> request<T>(
  Future<Response> Function() request,
  T Function(dynamic) parser,
) async {
  try {
    final response = await request();

    if (response.statusCode == 200) {
      return ApiResult.success(parser(response.data));
    } else {
      return ApiResult.error('HTTP ${response.statusCode}');
    }
  } on DioException catch (e) {
    if (e.type == DioExceptionType.connectionTimeout) {
      return ApiResult.error('连接超时,请检查网络');
    } else if (e.type == DioExceptionType.receiveTimeout) {
      return ApiResult.error('服务器响应超时');
    } else if (e.response?.statusCode == 401) {
      // 处理未授权
      Get.offAllNamed('/login');
      return ApiResult.error('登录已过期');
    } else {
      return ApiResult.error('网络请求失败: ${e.message}');
    }
  } catch (e) {
    return ApiResult.error('未知错误: $e');
  }
}

// ✅ 使用 ApiResult 封装
class ApiResult<T> {
  final T? data;
  final String? error;
  final bool success;

  ApiResult.success(this.data) : success = true, error = null;
  ApiResult.error(this.error) : success = false, data = null;
}
```

**修复建议**:
1. 所有网络请求包裹 try-catch
2. 区分 DioException 类型
3. 使用统一的错误处理机制

---

## 🟡 Major - 重要级

### 7. 图片缓存未清理

**风险等级**: 🟡 Major (6分)

**描述**: 使用 `CachedNetworkImage` 但未清理缓存,导致存储占用过大。

**危险模式**:

```dart
// 模式 1: 无缓存管理
CachedNetworkImage(
  imageUrl: 'https://example.com/large-image.jpg',
  // ❌ 未设置最大缓存时间
)

// 模式 2: 未提供清理入口
class SettingsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        // ❌ 缺少"清理缓存"选项
      ],
    );
  }
}
```

**影响**:
- 存储空间占用过大
- 显示过期图片
- 用户投诉

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'CachedNetworkImage'

# Level 2 - Serena MCP
查询: "查找所有使用 CachedNetworkImage 的代码"
查询: "查找设置页面是否有清理缓存功能"
```

**安全示例**:

```dart
// ✅ 设置缓存策略
CachedNetworkImage(
  imageUrl: imageUrl,
  cacheManager: CacheManager(
    Config(
      'customCacheKey',
      maxNrOfCacheObjects: 200,  // 最大缓存数量
      stalePeriod: Duration(days: 7),  // 缓存过期时间
    ),
  ),
)

// ✅ 提供清理入口
class SettingsPage extends StatelessWidget {
  Future<void> _clearCache() async {
    await DefaultCacheManager().emptyCache();
    Get.snackbar('成功', '缓存已清理');
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        ListTile(
          title: const Text('清理缓存'),
          onTap: _clearCache,
        ),
      ],
    );
  }
}
```

**修复建议**:
1. 设置缓存过期时间
2. 提供手动清理入口
3. 定期自动清理过期缓存

---

### 8. Hive 数据库未关闭

**风险等级**: 🟡 Major (6分)

**描述**: 打开 Hive Box 后未正确关闭。

**危险模式**:

```dart
// 模式 1: 未关闭 Box
Future<void> saveData(String key, dynamic value) async {
  final box = await Hive.openBox('myBox');
  await box.put(key, value);
  // ❌ 未关闭
}

// 模式 2: 重复打开
class MyService {
  Future<void> operation1() async {
    final box = await Hive.openBox('myBox');  // ❌ 多次打开
    // ...
  }

  Future<void> operation2() async {
    final box = await Hive.openBox('myBox');  // ❌ 重复打开
    // ...
  }
}
```

**影响**:
- 文件句柄泄漏
- 数据损坏风险
- 性能下降

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'Hive\.openBox' | grep -v 'close'

# Level 2 - Serena MCP
查询: "查找所有 Hive.openBox 调用但未调用 close 的代码"
```

**安全示例**:

```dart
// ✅ 全局单例管理
class HiveManager {
  static Box? _box;

  static Future<Box> get box async {
    if (_box == null || !_box!.isOpen) {
      _box = await Hive.openBox('myBox');
    }
    return _box!;
  }

  static Future<void> close() async {
    await _box?.close();
    _box = null;
  }
}

// 使用
await (await HiveManager.box).put(key, value);

// 应用退出时关闭
@override
void dispose() {
  HiveManager.close();
  super.dispose();
}

// ✅ 或使用 LazyBox (按需加载)
final lazyBox = await Hive.openLazyBox('myLazyBox');
await lazyBox.put(key, value);
// LazyBox 可以保持打开状态
```

**修复建议**:
1. 使用全局单例管理 Box
2. 应用退出时统一关闭
3. 使用 LazyBox 减少内存占用

---

### 9. BuildContext 跨异步使用

**风险等级**: 🟡 Major (5分)

**描述**: 异步操作后直接使用 BuildContext,可能导致崩溃。

**危险模式**:

```dart
// 模式 1: 异步后直接使用 context
Future<void> handleSubmit(BuildContext context) async {
  await Future.delayed(Duration(seconds: 2));
  Navigator.pop(context);  // ❌ Widget 可能已销毁
}

// 模式 2: 异步后显示 SnackBar
Future<void> saveData(BuildContext context) async {
  await repository.save();
  ScaffoldMessenger.of(context).showSnackBar(  // ❌
    SnackBar(content: Text('保存成功')),
  );
}
```

**影响**:
- Widget 已销毁时崩溃
- 内存泄漏

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'await.*Navigator\.|await.*Scaffold'

# Level 2 - Serena MCP
查询: "查找所有异步方法中在 await 后使用 BuildContext 的代码"
```

**安全示例**:

```dart
// ✅ 检查 mounted
Future<void> handleSubmit(BuildContext context) async {
  await Future.delayed(Duration(seconds: 2));
  if (!mounted) return;  // ✅ StatefulWidget
  Navigator.pop(context);
}

// ✅ 使用 GetX 导航(无需 context)
Future<void> handleSubmit() async {
  await Future.delayed(Duration(seconds: 2));
  Get.back();  // ✅
}

// ✅ 使用 GetX Snackbar
Future<void> saveData() async {
  await repository.save();
  Get.snackbar('成功', '保存成功');  // ✅
}
```

**修复建议**:
1. 异步后检查 `mounted` 状态
2. 使用 GetX 导航和提示(无需 context)
3. 避免跨异步边界传递 context

---

## 🟢 Minor - 次要级

### 10. 未使用 late 延迟初始化

**风险等级**: 🟢 Minor (3分)

**描述**: 可延迟初始化的变量未使用 `late`,增加启动时间。

**危险模式**:

```dart
// 模式 1: 不必要的立即初始化
class MyController extends GetxController {
  final dio = Dio(BaseOptions(baseUrl: 'https://api.example.com'));  // ❌
  final repository = MyRepository();  // ❌

  @override
  void onInit() {
    // 可能根本不会用到
  }
}

// 模式 2: 可空但必定赋值
class MyService {
  Dio? _dio;  // ❌ 应该用 late

  void init() {
    _dio = Dio();
  }

  void request() {
    _dio!.get('/api');  // 到处需要 !
  }
}
```

**影响**:
- 启动时间增加
- 内存浪费

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'final.*=.*\(|Dio\?|Repository\?'

# Level 2 - Serena MCP
查询: "查找所有在类初始化时创建 Dio 实例的代码"
```

**安全示例**:

```dart
// ✅ 使用 late
class MyController extends GetxController {
  late final Dio dio;
  late final MyRepository repository;

  @override
  void onInit() {
    dio = Dio(BaseOptions(baseUrl: 'https://api.example.com'));
    repository = MyRepository();
  }
}

// ✅ 使用 late (必定赋值)
class MyService {
  late Dio _dio;  // ✅ 不需要可空

  void init() {
    _dio = Dio();
  }

  void request() {
    _dio.get('/api');  // ✅ 无需 !
  }
}
```

**修复建议**:
1. 延迟初始化使用 `late`
2. 必定赋值的变量避免可空
3. 减少启动时不必要的对象创建

---

### 11. 滥用 GlobalKey

**风险等级**: 🟢 Minor (3分)

**描述**: 过度使用 GlobalKey 导致性能问题。

**危险模式**:

```dart
// 模式 1: 列表中使用 GlobalKey
ListView.builder(
  itemBuilder: (context, index) {
    return Container(
      key: GlobalKey(),  // ❌ 每次 rebuild 都创建
      child: ListTile(title: Text('Item $index')),
    );
  },
)

// 模式 2: 可以用 Controller 替代
class MyPage extends StatelessWidget {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey();  // ❌

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      body: ElevatedButton(
        onPressed: () {
          _scaffoldKey.currentState?.showSnackBar(/*...*/);
        },
        child: Text('Show'),
      ),
    );
  }
}
```

**影响**:
- 性能下降
- 内存占用

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'GlobalKey'

# Level 2 - Serena MCP
查询: "查找所有在 itemBuilder 中使用 GlobalKey 的代码"
```

**安全示例**:

```dart
// ✅ 使用 ValueKey
ListView.builder(
  itemBuilder: (context, index) {
    return Container(
      key: ValueKey('item_$index'),  // ✅
      child: ListTile(title: Text('Item $index')),
    );
  },
)

// ✅ 使用 GetX Snackbar (无需 key)
class MyPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ElevatedButton(
        onPressed: () {
          Get.snackbar('Title', 'Message');  // ✅
        },
        child: Text('Show'),
      ),
    );
  }
}
```

**修复建议**:
1. 列表使用 `ValueKey` 或 `ObjectKey`
2. 导航和提示使用 GetX API
3. 仅必要时使用 GlobalKey

---

## MagicFrame App 特定规则

### 12. Firebase Analytics 未捕获异常

**风险等级**: 🟡 Major (5分)

**描述**: Firebase Analytics 事件上报未捕获异常。

**危险模式**:

```dart
// 模式 1: 直接上报
await FirebaseAnalytics.instance.logEvent(
  name: 'purchase',
  parameters: {'item_id': itemId},  // ❌ itemId 可能为 null
);

// 模式 2: 未验证参数
void trackEvent(String name, Map<String, dynamic>? params) {
  FirebaseAnalytics.instance.logEvent(
    name: name,
    parameters: params,  // ❌ 可能为 null
  );
}
```

**安全示例**:

```dart
// ✅ 安全上报
Future<void> trackEvent(String name, Map<String, dynamic>? params) async {
  try {
    await FirebaseAnalytics.instance.logEvent(
      name: name,
      parameters: params ?? {},
    );
  } catch (e) {
    debugPrint('Analytics error: $e');
    // 不阻塞业务流程
  }
}
```

---

### 13. 媒体文件未压缩直接上传

**风险等级**: 🟡 Major (6分)

**描述**: 图片/视频未压缩直接上传,浪费流量和时间。

**危险模式**:

```dart
// 模式 1: 原图上传
final imageFile = await ImagePicker().pickImage(source: ImageSource.gallery);
await dio.post('/upload', data: FormData.fromMap({
  'file': await MultipartFile.fromFile(imageFile!.path),  // ❌ 原图可能很大
}));

// 模式 2: 视频未压缩
final videoFile = await ImagePicker().pickVideo(source: ImageSource.gallery);
await uploadVideo(videoFile!.path);  // ❌ 未压缩
```

**安全示例**:

```dart
// ✅ 图片压缩
import 'package:flutter_image_compress/flutter_image_compress.dart';

Future<File?> compressImage(File file) async {
  final result = await FlutterImageCompress.compressAndGetFile(
    file.absolute.path,
    file.path.replaceAll('.jpg', '_compressed.jpg'),
    quality: 85,
    minWidth: 1920,
    minHeight: 1080,
  );
  return result != null ? File(result.path) : null;
}

// ✅ 视频压缩
import 'package:video_compress/video_compress.dart';

Future<File?> compressVideo(String path) async {
  final info = await VideoCompress.compressVideo(
    path,
    quality: VideoQuality.MediumQuality,
    deleteOrigin: false,
  );
  return info?.file;
}
```

**修复建议**:
1. 图片压缩到 1920x1080 以下
2. 视频使用 MediumQuality 压缩
3. 显示上传进度

---

### 14. In-App Purchase 未验证收据

**风险等级**: 🔴 Blocker (9分)

**描述**: 应用内购买未在服务端验证收据,可能被伪造。

**危险模式**:

```dart
// 模式 1: 客户端直接解锁
final purchaseDetails = await InAppPurchase.instance.queryPastPurchases();
if (purchaseDetails.pastPurchases.isNotEmpty) {
  unlockFeature();  // ❌ 未验证收据
}

// 模式 2: 仅本地验证
void handlePurchase(PurchaseDetails details) {
  if (details.status == PurchaseStatus.purchased) {
    unlockFeature();  // ❌ 未服务端验证
  }
}
```

**安全示例**:

```dart
// ✅ 服务端验证
Future<void> handlePurchase(PurchaseDetails details) async {
  if (details.status == PurchaseStatus.purchased) {
    try {
      // 1. 发送收据到服务端验证
      final response = await dio.post('/api/purchase/verify', data: {
        'receipt': details.verificationData.serverVerificationData,
        'product_id': details.productID,
      });

      // 2. 服务端验证成功后解锁
      if (response.data['verified'] == true) {
        unlockFeature();

        // 3. 完成交易
        await InAppPurchase.instance.completePurchase(details);
      }
    } catch (e) {
      debugPrint('Purchase verification failed: $e');
    }
  }
}
```

**修复建议**:
1. 所有购买必须服务端验证收据
2. 验证成功后才解锁功能
3. 记录购买日志防作弊

---

## 检测工具推荐

### Serena MCP 查询示例

针对 MagicFrame App 项目的常用查询:

```
# GetX 相关
"查找所有 GetxController 中未在 onClose 释放资源的代码"
"查找所有使用 Get.find 但未注册的 Controller"
"查找所有 Obx 包裹范围过大的代码"

# 网络请求
"查找所有 Dio 请求未处理错误的代码"
"查找所有使用 http:// 的 URL"
"查找所有 API 请求未设置超时的代码"

# 媒体处理
"查找所有图片上传未压缩的代码"
"查找所有视频播放未释放资源的代码"

# 存储安全
"查找所有 SharedPreferences 存储敏感信息的代码"
"查找所有 Hive Box 未关闭的代码"

# 性能
"查找所有 ListView.builder 未使用 Key 的代码"
"查找所有未使用 const 的静态 Widget"
```

---

## 总结

针对 MagicFrame App 项目的缺陷检测重点:

1. **安全**: HTTP/HTTPS、敏感信息、WebView、支付验证
2. **内存**: GetX Controller 泄漏、Stream/Timer 未释放
3. **性能**: Widget rebuild、图片缓存、媒体压缩
4. **稳定性**: 错误处理、异步 context、资源释放

**项目特定关注**:
- GetX 架构模式正确使用
- Repository 和 Service 层资源管理
- Dio + Hive 配合使用
- Firebase Analytics 异常处理
- 媒体文件处理和上传优化
- 应用内购买安全验证
