# Kotlin + Android 缺陷检测规则

针对 **MagicFrame Android** 项目,基于 Repository + ViewModel 架构的缺陷检测规则。

## 规则概览

按严重度分级:

- 🔴 **Blocker**(阻断级): 内存泄漏、ANR 风险、安全漏洞
- 🟠 **Critical**(严重级): 生命周期问题、线程安全
- 🟡 **Major**(重要级): 资源泄漏、性能问题
- 🟢 **Minor**(次要级): 代码质量、最佳实践

---

## 🔴 Blocker - 阻断级

### 1. Context/Activity 内存泄漏

**风险等级**: 🔴 Blocker (10分)

**描述**: 静态变量、单例、匿名内部类持有 Context 引用导致内存泄漏。

**危险模式**:

```kotlin
// 模式 1: 静态变量持有 Context
companion object {
    private var context: Context? = null  // ❌ 静态持有

    fun init(ctx: Context) {
        context = ctx
    }
}

// 模式 2: 单例持有 Activity
object NetworkManager {
    private var activity: Activity? = null  // ❌ 单例持有

    fun setup(act: Activity) {
        activity = act
    }
}

// 模式 3: 匿名内部类/Lambda 隐式持有
class MainActivity : AppCompatActivity() {
    private val handler = Handler(Looper.getMainLooper())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // ❌ 延迟任务持有 Activity 引用
        handler.postDelayed({
            updateUI()  // 隐式持有 this@MainActivity
        }, 10000)
    }
}

// 模式 4: 监听器未移除
class MyActivity : AppCompatActivity() {
    private val listener = object : WifiStatusListener {
        override fun onStatusChanged(status: WifiStatus) {
            updateUI()  // ❌ 持有 Activity 引用
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WifiStatusManager.addListener(listener)  // ❌ 未在 onDestroy 移除
    }
}
```

**影响**:
- Activity 无法被 GC 回收
- 内存占用持续增长
- OOM 崩溃

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'companion object.*Context|object.*Activity|Handler\(.*postDelayed'

# Level 2 - Serena MCP
查询: "查找所有 companion object 中持有 Context 的代码"
查询: "查找所有单例持有 Activity 引用的代码"
查询: "查找所有 Handler.postDelayed 使用 lambda 的代码"
```

**安全示例**:

```kotlin
// ✅ 使用 Application Context
companion object {
    private var appContext: Context? = null

    fun init(context: Context) {
        appContext = context.applicationContext  // ✅ 使用 Application Context
    }
}

// ✅ 使用弱引用
class NetworkManager private constructor() {
    private var activityRef: WeakReference<Activity>? = null  // ✅ 弱引用

    fun setup(activity: Activity) {
        activityRef = WeakReference(activity)
    }

    fun getActivity(): Activity? = activityRef?.get()

    companion object {
        @Volatile
        private var instance: NetworkManager? = null

        fun getInstance(): NetworkManager {
            return instance ?: synchronized(this) {
                instance ?: NetworkManager().also { instance = it }
            }
        }
    }
}

// ✅ 使用静态内部类 + 弱引用
class MainActivity : AppCompatActivity() {
    private val handler = MyHandler(this)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        handler.sendEmptyMessageDelayed(0, 10000)
    }

    override fun onDestroy() {
        handler.removeCallbacksAndMessages(null)  // ✅ 清理
        super.onDestroy()
    }

    private class MyHandler(activity: MainActivity) : Handler(Looper.getMainLooper()) {
        private val activityRef = WeakReference(activity)  // ✅

        override fun handleMessage(msg: Message) {
            activityRef.get()?.updateUI()
        }
    }
}

// ✅ 监听器正确移除
class MyActivity : AppCompatActivity() {
    private val listener = object : WifiStatusListener {
        override fun onStatusChanged(status: WifiStatus) {
            updateUI()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WifiStatusManager.addListener(listener)
    }

    override fun onDestroy() {
        WifiStatusManager.removeListener(listener)  // ✅ 移除监听器
        super.onDestroy()
    }
}
```

**修复建议**:
1. 静态/单例使用 `applicationContext`
2. 必须持有 Activity 时用 `WeakReference`
3. Handler 使用静态内部类 + 弱引用
4. 监听器在 `onDestroy` 中移除

**参考**: LeakCanary 检测

---

### 2. 主线程阻塞导致 ANR

**风险等级**: 🔴 Blocker (10分)

**描述**: 在主线程执行耗时操作(网络、IO、数据库)导致 ANR。

**危险模式**:

```kotlin
// 模式 1: 主线程网络请求
fun loadData() {
    val response = retrofitService.getData().execute()  // ❌ 同步调用
    updateUI(response.body())
}

// 模式 2: 主线程数据库操作
fun saveData(data: Resource) {
    XDatabase.resourceDao().insert(data)  // ❌ Room 同步调用
}

// 模式 3: 主线程文件操作
fun readFile(): String {
    return File("/sdcard/large_file.txt").readText()  // ❌ 主线程读大文件
}

// 模式 4: 循环中调用耗时操作
fun processItems(items: List<Item>) {
    items.forEach { item ->
        val bitmap = BitmapFactory.decodeFile(item.imagePath)  // ❌ 循环解码图片
        processBitmap(bitmap)
    }
}
```

**影响**:
- ANR 对话框
- 应用无响应
- 用户投诉和卸载

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E '\.execute\(\)|\.readText\(\)|BitmapFactory\.decode'

# Level 2 - Serena MCP
查询: "查找所有在非协程/非后台线程中调用 Retrofit execute 的代码"
查询: "查找所有在主线程调用 Room 数据库同步方法的代码"
查询: "查找所有循环中执行 IO 操作的代码"
```

**安全示例**:

```kotlin
// ✅ 使用协程
class MyViewModel : ViewModel() {
    fun loadData() {
        viewModelScope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    retrofitService.getData()  // ✅ IO 线程
                }
                updateUI(response)
            } catch (e: Exception) {
                handleError(e)
            }
        }
    }
}

// ✅ Room 协程支持
@Dao
interface ResourceDao {
    @Insert
    suspend fun insert(resource: Resource)  // ✅ suspend 函数

    @Query("SELECT * FROM resources")
    fun getAllFlow(): Flow<List<Resource>>  // ✅ Flow 自动后台
}

// 使用
viewModelScope.launch {
    XDatabase.resourceDao().insert(data)  // ✅ 协程中调用
}

// ✅ 文件操作使用协程
suspend fun readFile(): String = withContext(Dispatchers.IO) {
    File("/sdcard/large_file.txt").readText()
}

// ✅ 批量操作使用并发
suspend fun processItems(items: List<Item>) = coroutineScope {
    items.map { item ->
        async(Dispatchers.Default) {  // ✅ 并发处理
            val bitmap = BitmapFactory.decodeFile(item.imagePath)
            processBitmap(bitmap)
        }
    }.awaitAll()
}
```

**修复建议**:
1. 网络请求使用协程 `suspend`
2. Room 使用 `suspend` 或 `Flow`
3. 文件 IO 使用 `Dispatchers.IO`
4. 图片解码使用 `Dispatchers.Default`

**参考**: Android Vitals - ANR Rate

---

### 3. 硬编码签名密钥

**风险等级**: 🔴 Blocker (10分)

**描述**: build.gradle 中硬编码签名密钥。

**危险模式**:

```gradle
// build.gradle - ❌ 硬编码密码
signingConfigs {
    release {
        storeFile file('../keystore_rk/platform.jks')
        storePassword "mgframe62425.."  // ❌ 明文密码
        keyAlias "platform"
        keyPassword "mgframe62425.."    // ❌ 明文密码
    }
}
```

**攻击风险**:
- 代码泄露导致签名被盗用
- 恶意 APK 签名
- 品牌信誉损失

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'storePassword|keyPassword' | grep -v 'System.getenv'

# Level 2 - Serena MCP
查询: "查找 build.gradle 中硬编码密码的配置"
```

**安全示例**:

```gradle
// ✅ 从环境变量读取
signingConfigs {
    release {
        storeFile file('../keystore_rk/platform.jks')
        storePassword System.getenv("KEYSTORE_PASSWORD")
        keyAlias System.getenv("KEY_ALIAS")
        keyPassword System.getenv("KEY_PASSWORD")
    }
}

// ✅ 从 local.properties 读取(不提交到 Git)
def localProperties = new Properties()
def localPropertiesFile = rootProject.file('local.properties')
if (localPropertiesFile.exists()) {
    localPropertiesFile.withInputStream { stream ->
        localProperties.load(stream)
    }
}

signingConfigs {
    release {
        storeFile file('../keystore_rk/platform.jks')
        storePassword localProperties.getProperty('storePassword')
        keyAlias localProperties.getProperty('keyAlias')
        keyPassword localProperties.getProperty('keyPassword')
    }
}
```

**.gitignore** 确保包含:
```
local.properties
keystore_rk/
*.jks
*.keystore
```

**修复建议**:
1. 密钥从环境变量或 `local.properties` 读取
2. `local.properties` 加入 `.gitignore`
3. CI/CD 使用加密变量

---

## 🟠 Critical - 严重级

### 4. LiveData/Flow 泄漏

**风险等级**: 🟠 Critical (8分)

**描述**: LiveData observe 使用 Activity 作为 LifecycleOwner,或 Flow collect 未取消。

**危险模式**:

```kotlin
// 模式 1: Fragment 中使用 Activity 作为 LifecycleOwner
class MyFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        viewModel.data.observe(requireActivity()) { data ->  // ❌ 使用 Activity
            updateUI(data)
        }
    }
}

// 模式 2: Flow collect 未绑定生命周期
class MyActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        GlobalScope.launch {  // ❌ 使用 GlobalScope
            viewModel.dataFlow.collect { data ->
                updateUI(data)
            }
        }
    }
}

// 模式 3: 自定义生命周期观察者未移除
class MyActivity : AppCompatActivity() {
    private val observer = Observer<String> { data ->
        updateUI(data)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        viewModel.data.observeForever(observer)  // ❌ 未在 onDestroy 移除
    }
}
```

**影响**:
- Activity/Fragment 泄漏
- 重复观察多次触发
- 崩溃(UI 更新时 View 已销毁)

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E '\.observe\(requireActivity|GlobalScope\.launch|observeForever'

# Level 2 - Serena MCP
查询: "查找 Fragment 中 LiveData.observe 使用 requireActivity 的代码"
查询: "查找所有使用 GlobalScope.launch 的代码"
查询: "查找 observeForever 但未调用 removeObserver 的代码"
```

**安全示例**:

```kotlin
// ✅ Fragment 使用 viewLifecycleOwner
class MyFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        viewModel.data.observe(viewLifecycleOwner) { data ->  // ✅
            updateUI(data)
        }
    }
}

// ✅ Flow 使用 lifecycleScope
class MyActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        lifecycleScope.launch {  // ✅ 绑定生命周期
            viewModel.dataFlow.collect { data ->
                updateUI(data)
            }
        }
    }
}

// ✅ 或使用 repeatOnLifecycle
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {  // ✅ 仅在 STARTED 时收集
        viewModel.dataFlow.collect { data ->
            updateUI(data)
        }
    }
}

// ✅ observeForever 正确移除
class MyActivity : AppCompatActivity() {
    private val observer = Observer<String> { data ->
        updateUI(data)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        viewModel.data.observeForever(observer)
    }

    override fun onDestroy() {
        viewModel.data.removeObserver(observer)  // ✅
        super.onDestroy()
    }
}
```

**修复建议**:
1. Fragment 使用 `viewLifecycleOwner`
2. Flow 使用 `lifecycleScope` 或 `repeatOnLifecycle`
3. `observeForever` 必须在 `onDestroy` 中移除
4. 避免使用 `GlobalScope`

---

### 5. 协程作用域滥用

**风险等级**: 🟠 Critical (7分)

**描述**: 使用错误的协程作用域导致任务泄漏或过早取消。

**危险模式**:

```kotlin
// 模式 1: 使用 GlobalScope
class MyActivity : AppCompatActivity() {
    fun loadData() {
        GlobalScope.launch {  // ❌ 永不取消
            val data = repository.fetchData()
            updateUI(data)
        }
    }
}

// 模式 2: Repository 中使用 viewModelScope
class MyRepository {
    fun fetchData(viewModelScope: CoroutineScope) {
        viewModelScope.launch {  // ❌ Repository 不应依赖 ViewModel
            // ...
        }
    }
}

// 模式 3: 自定义 Scope 未取消
class MyService : Service() {
    private val serviceScope = CoroutineScope(Dispatchers.Default)  // ❌ 未取消

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        serviceScope.launch {
            // 长时间任务
        }
        return START_STICKY
    }
}
```

**影响**:
- 任务永不取消,浪费资源
- Activity 销毁后仍执行
- 崩溃或异常行为

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'GlobalScope\.launch|CoroutineScope\(Dispatchers'

# Level 2 - Serena MCP
查询: "查找所有使用 GlobalScope.launch 的代码"
查询: "查找 Repository 中使用 viewModelScope 的代码"
查询: "查找自定义 CoroutineScope 但未调用 cancel 的代码"
```

**安全示例**:

```kotlin
// ✅ Activity 使用 lifecycleScope
class MyActivity : AppCompatActivity() {
    fun loadData() {
        lifecycleScope.launch {  // ✅ Activity 销毁时自动取消
            val data = repository.fetchData()
            updateUI(data)
        }
    }
}

// ✅ Repository 返回 suspend 或 Flow
class MyRepository {
    suspend fun fetchData(): Data = withContext(Dispatchers.IO) {
        // IO 操作
    }

    fun fetchDataFlow(): Flow<Data> = flow {
        emit(fetchData())
    }.flowOn(Dispatchers.IO)
}

// ✅ 自定义 Scope 正确取消
class MyService : Service() {
    private val serviceScope = CoroutineScope(
        SupervisorJob() + Dispatchers.Default
    )

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        serviceScope.launch {
            // 长时间任务
        }
        return START_STICKY
    }

    override fun onDestroy() {
        serviceScope.cancel()  // ✅ 取消所有协程
        super.onDestroy()
    }
}
```

**修复建议**:
1. Activity/Fragment 使用 `lifecycleScope`
2. ViewModel 使用 `viewModelScope`
3. Repository 返回 `suspend` 函数或 `Flow`
4. 自定义 Scope 必须在适当时机 `cancel()`

---

### 6. Room 数据库迁移缺失

**风险等级**: 🟠 Critical (7分)

**描述**: 修改数据库结构但未提供迁移策略。

**危险模式**:

```kotlin
// 模式 1: 版本升级无迁移
@Database(
    entities = [Resource::class, User::class],
    version = 2,  // ❌ 从版本 1 升级,但未提供 Migration
    exportSchema = true
)
abstract class XDatabase : RoomDatabase() {
    // ...
}

// 模式 2: fallbackToDestructiveMigration 滥用
Room.databaseBuilder(context, XDatabase::class.java, "database")
    .fallbackToDestructiveMigration()  // ❌ 生产环境会删除所有数据
    .build()
```

**影响**:
- 应用崩溃
- 用户数据丢失
- 严重用户投诉

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E '@Database.*version.*=' | grep -v 'Migration'

# Level 2 - Serena MCP
查询: "查找 @Database 版本升级但未提供 Migration 的代码"
查询: "查找使用 fallbackToDestructiveMigration 的代码"
```

**安全示例**:

```kotlin
// ✅ 提供迁移策略
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(database: SupportSQLiteDatabase) {
        // 添加新列
        database.execSQL("ALTER TABLE Resource ADD COLUMN cover_url TEXT")
    }
}

val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(database: SupportSQLiteDatabase) {
        // 创建新表
        database.execSQL("""
            CREATE TABLE IF NOT EXISTS `User` (
                `id` INTEGER PRIMARY KEY NOT NULL,
                `name` TEXT NOT NULL
            )
        """.trimIndent())
    }
}

@Database(
    entities = [Resource::class, User::class],
    version = 3,
    exportSchema = true
)
abstract class XDatabase : RoomDatabase() {
    // ...
}

// 构建数据库
Room.databaseBuilder(context, XDatabase::class.java, "database")
    .addMigrations(MIGRATION_1_2, MIGRATION_2_3)  // ✅
    .build()

// ✅ 仅开发环境使用 fallbackToDestructiveMigration
Room.databaseBuilder(context, XDatabase::class.java, "database")
    .apply {
        if (BuildConfig.DEBUG) {
            fallbackToDestructiveMigration()  // ✅ 仅调试
        } else {
            addMigrations(MIGRATION_1_2, MIGRATION_2_3)
        }
    }
    .build()
```

**修复建议**:
1. 版本升级必须提供 `Migration`
2. 生产环境禁用 `fallbackToDestructiveMigration`
3. 测试迁移路径(1→2, 1→3, 2→3)

---

## 🟡 Major - 重要级

### 7. Bitmap 未回收

**风险等级**: 🟡 Major (6分)

**描述**: 手动加载 Bitmap 后未调用 `recycle()`。

**危险模式**:

```kotlin
// 模式 1: 直接解码不回收
fun loadImage(path: String): Bitmap {
    return BitmapFactory.decodeFile(path)  // ❌ 未回收
}

// 模式 2: 循环加载大量 Bitmap
fun loadImages(paths: List<String>) {
    paths.forEach { path ->
        val bitmap = BitmapFactory.decodeFile(path)  // ❌ 大量内存占用
        processBitmap(bitmap)
        // 未回收
    }
}
```

**影响**:
- 内存占用过高
- OOM 崩溃

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'BitmapFactory\.decode' | grep -v 'recycle'

# Level 2 - Serena MCP
查询: "查找所有使用 BitmapFactory.decode 但未调用 recycle 的代码"
```

**安全示例**:

```kotlin
// ✅ 使用 Glide 自动管理
Glide.with(context)
    .load(imageUrl)
    .into(imageView)  // ✅ Glide 自动管理内存

// ✅ 手动加载时正确回收
fun loadImage(path: String, onLoaded: (Bitmap) -> Unit) {
    var bitmap: Bitmap? = null
    try {
        bitmap = BitmapFactory.decodeFile(path)
        onLoaded(bitmap)
    } finally {
        bitmap?.recycle()  // ✅ finally 确保回收
    }
}

// ✅ 或使用 use 扩展函数
fun processBitmap(path: String) {
    BitmapFactory.decodeFile(path)?.use { bitmap ->
        // 处理 bitmap
    }  // ✅ 自动回收
}

// 定义 use 扩展
inline fun <T : Bitmap, R> T.use(block: (T) -> R): R {
    try {
        return block(this)
    } finally {
        recycle()
    }
}
```

**修复建议**:
1. 优先使用 Glide/Coil 等图片库
2. 手动加载在 `finally` 中回收
3. 大图使用 `BitmapFactory.Options` 压缩

---

### 8. 广播接收器未注销

**风险等级**: 🟡 Major (6分)

**描述**: 动态注册的广播接收器未在 `onDestroy` 中注销。

**危险模式**:

```kotlin
// 模式 1: 未注销
class MyActivity : AppCompatActivity() {
    private val receiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            handleBroadcast(intent)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val filter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        registerReceiver(receiver, filter)  // ❌ 未注销
    }
}
```

**影响**:
- Activity 泄漏
- 重复注册导致多次回调

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'registerReceiver' | grep -v 'unregisterReceiver'

# Level 2 - Serena MCP
查询: "查找 registerReceiver 但未调用 unregisterReceiver 的代码"
```

**安全示例**:

```kotlin
// ✅ 正确注销
class MyActivity : AppCompatActivity() {
    private val receiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            handleBroadcast(intent)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val filter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        registerReceiver(receiver, filter)
    }

    override fun onDestroy() {
        unregisterReceiver(receiver)  // ✅
        super.onDestroy()
    }
}

// ✅ 或使用安全的注册方式
class MyActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val filter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        lifecycleScope.launch {
            lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) {
                // 仅在 STARTED 状态注册
                registerReceiver(receiver, filter)
                try {
                    suspendCancellableCoroutine<Unit> { /* 挂起直到取消 */ }
                } finally {
                    unregisterReceiver(receiver)  // ✅ 自动注销
                }
            }
        }
    }
}
```

**修复建议**:
1. `onDestroy` 中注销接收器
2. 使用 `try-finally` 确保注销
3. 考虑使用静态注册(Manifest)

---

### 9. SharedPreferences 同步调用

**风险等级**: 🟡 Major (5分)

**描述**: 使用 `commit()` 而非 `apply()`,阻塞主线程。

**危险模式**:

```kotlin
// 模式 1: 使用 commit()
fun saveData(key: String, value: String) {
    sharedPreferences.edit()
        .putString(key, value)
        .commit()  // ❌ 同步写入,阻塞主线程
}

// 模式 2: 循环中使用 commit()
fun saveMultiple(data: Map<String, String>) {
    data.forEach { (key, value) ->
        sharedPreferences.edit()
            .putString(key, value)
            .commit()  // ❌ 多次同步写入
    }
}
```

**影响**:
- 主线程阻塞
- UI 卡顿
- ANR 风险

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E '\.commit\(\)'

# Level 2 - Serena MCP
查询: "查找所有使用 SharedPreferences.commit 的代码"
```

**安全示例**:

```kotlin
// ✅ 使用 apply()
fun saveData(key: String, value: String) {
    sharedPreferences.edit()
        .putString(key, value)
        .apply()  // ✅ 异步写入
}

// ✅ 批量操作
fun saveMultiple(data: Map<String, String>) {
    sharedPreferences.edit().apply {
        data.forEach { (key, value) ->
            putString(key, value)
        }
    }.apply()  // ✅ 一次性写入
}

// ✅ 使用 MMKV (更高性能)
import com.tencent.mmkv.MMKV

val mmkv = MMKV.defaultMMKV()
mmkv.encode("key", "value")  // ✅ 同步但性能高

// ✅ 或使用 DataStore (协程友好)
val Context.dataStore: DataStore<Preferences> by preferencesDataStore("settings")

suspend fun saveData(key: String, value: String) {
    context.dataStore.edit { preferences ->
        preferences[stringPreferencesKey(key)] = value
    }
}
```

**修复建议**:
1. 使用 `apply()` 而非 `commit()`
2. 批量操作减少写入次数
3. 考虑 MMKV 或 DataStore

---

### 10. WorkManager 任务未设置约束

**风险等级**: 🟡 Major (5分)

**描述**: 后台任务未设置网络、电池等约束,浪费资源。

**危险模式**:

```kotlin
// 模式 1: 无约束任务
val request = OneTimeWorkRequestBuilder<UploadWorker>()
    .build()  // ❌ 未设置约束

WorkManager.getInstance(context).enqueue(request)

// 模式 2: 频繁定期任务
val periodicRequest = PeriodicWorkRequestBuilder<SyncWorker>(
    15, TimeUnit.MINUTES  // ❌ 间隔过短
).build()
```

**影响**:
- 耗电量大
- 流量消耗
- 用户投诉

**检测方法**:

```bash
# Level 1 - 文本匹配
git diff HEAD~3..HEAD | grep -E 'WorkRequestBuilder' | grep -v 'setConstraints'

# Level 2 - Serena MCP
查询: "查找所有 WorkRequest 未设置 Constraints 的代码"
查询: "查找 PeriodicWorkRequest 间隔小于 15 分钟的代码"
```

**安全示例**:

```kotlin
// ✅ 设置约束
val constraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.CONNECTED)  // ✅ 需要网络
    .setRequiresBatteryNotLow(true)  // ✅ 电量充足
    .setRequiresCharging(false)  // 根据需求
    .build()

val request = OneTimeWorkRequestBuilder<UploadWorker>()
    .setConstraints(constraints)  // ✅
    .setBackoffCriteria(
        BackoffPolicy.EXPONENTIAL,
        WorkRequest.MIN_BACKOFF_MILLIS,
        TimeUnit.MILLISECONDS
    )
    .build()

WorkManager.getInstance(context).enqueue(request)

// ✅ 定期任务最小间隔 15 分钟
val periodicRequest = PeriodicWorkRequestBuilder<SyncWorker>(
    15, TimeUnit.MINUTES  // ✅ Android 最小间隔
).setConstraints(constraints)
 .build()
```

**修复建议**:
1. 上传/下载任务设置网络约束
2. 大任务设置电量约束
3. 定期任务间隔 ≥ 15 分钟

---

## 🟢 Minor - 次要级

### 11. 硬编码字符串未提取

**风险等级**: 🟢 Minor (3分)

**描述**: UI 文本硬编码,不利于国际化。

**危险模式**:

```kotlin
// 模式 1: 硬编码字符串
textView.text = "欢迎使用 MagicFrame"  // ❌

// 模式 2: 字符串拼接
val message = "您有 $count 条新消息"  // ❌ 无法国际化
```

**安全示例**:

```kotlin
// ✅ 使用字符串资源
textView.text = getString(R.string.welcome_message)

// ✅ 格式化字符串
val message = getString(R.string.new_messages_format, count)

// strings.xml
// <string name="welcome_message">欢迎使用 MagicFrame</string>
// <string name="new_messages_format">您有 %d 条新消息</string>
```

---

### 12. 未使用 ViewBinding

**风险等级**: 🟢 Minor (3分)

**描述**: 使用 `findViewById` 而非 ViewBinding。

**危险模式**:

```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val textView = findViewById<TextView>(R.id.textView)  // ❌
    }
}
```

**安全示例**:

```kotlin
// ✅ 使用 ViewBinding
class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.textView.text = "Hello"  // ✅ 类型安全
    }
}
```

---

## MagicFrame Android 特定规则

### 13. IoT 消息处理未验证

**风险等级**: 🟠 Critical (7分)

**描述**: MQTT 消息处理未验证来源和格式。

**危险模式**:

```kotlin
// 模式 1: 未验证消息格式
fun handleMessage(message: TopicMessage2) {
    val data = message.data  // ❌ 未验证
    processData(data)
}

// 模式 2: 未验证设备 ID
fun handleResourceMessage(msg: ResourceMessage) {
    val resource = msg.data.toResource()  // ❌ 未验证来源
    XDatabase.resourceDao().insert(resource)
}
```

**安全示例**:

```kotlin
// ✅ 验证消息格式
fun handleMessage(message: TopicMessage2) {
    if (message.data == null) {
        XLog.w(TAG, "Invalid message: data is null")
        return
    }

    try {
        processData(message.data)
    } catch (e: Exception) {
        XLog.e(TAG, "Failed to process message", e)
    }
}

// ✅ 验证设备 ID 和数据完整性
suspend fun handleResourceMessage(msg: ResourceMessage) {
    val deviceId = XKeyValue.getDeviceId()

    // 验证消息是否发给当前设备
    if (msg.deviceId != deviceId) {
        XLog.w(TAG, "Message not for this device")
        return
    }

    // 验证数据完整性
    val resource = msg.data.toResource()
    if (!isResourceValid(resource)) {
        XLog.w(TAG, "Invalid resource data")
        return
    }

    XDatabase.resourceDao().insert(resource)
}

private fun isResourceValid(resource: Resource): Boolean {
    return resource.rid.isNotEmpty() &&
           resource.url.isNotEmpty() &&
           resource.type in ResourceType.values()
}
```

**修复建议**:
1. 验证消息格式和字段完整性
2. 验证设备 ID 和用户权限
3. 异常处理不阻塞消息队列

---

### 14. 下载任务无限重试

**风险等级**: 🟡 Major (6分)

**描述**: 下载失败无限重试,浪费流量和电量。

**危险模式**:

```kotlin
// 模式 1: 无限重试
suspend fun downloadFile(url: String) {
    while (true) {  // ❌ 无限循环
        try {
            val result = downloadManager.download(url)
            if (result.success) break
        } catch (e: Exception) {
            delay(1000)  // ❌ 继续重试
        }
    }
}
```

**安全示例**:

```kotlin
// ✅ 限制重试次数
suspend fun downloadFile(url: String, maxRetries: Int = 3): Result<File> {
    var lastError: Exception? = null

    repeat(maxRetries) { attempt ->
        try {
            val result = downloadManager.download(url)
            if (result.success) {
                return Result.success(result.file)
            }
        } catch (e: Exception) {
            lastError = e
            XLog.w(TAG, "Download failed (attempt ${attempt + 1}/$maxRetries)", e)

            if (attempt < maxRetries - 1) {
                // 指数退避
                val delayMs = (1000 * (attempt + 1) * (attempt + 1)).toLong()
                delay(delayMs)
            }
        }
    }

    return Result.failure(lastError ?: Exception("Download failed"))
}

// ✅ 或使用 WorkManager 自动重试
val constraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.CONNECTED)
    .build()

val request = OneTimeWorkRequestBuilder<DownloadWorker>()
    .setConstraints(constraints)
    .setBackoffCriteria(
        BackoffPolicy.EXPONENTIAL,
        WorkRequest.MIN_BACKOFF_MILLIS,
        TimeUnit.MILLISECONDS
    )
    .setInputData(workDataOf("url" to url))
    .build()
```

**修复建议**:
1. 限制重试次数(3-5次)
2. 使用指数退避策略
3. 网络错误使用 WorkManager 重试

---

## 检测工具推荐

### Serena MCP 查询示例

针对 MagicFrame Android 项目的常用查询:

```
# 内存泄漏
"查找所有 companion object 中持有 Context 的代码"
"查找所有 Handler.postDelayed 使用 lambda 的代码"
"查找所有监听器注册但未移除的代码"

# 生命周期
"查找 Fragment 中 LiveData.observe 使用 requireActivity 的代码"
"查找所有使用 GlobalScope.launch 的代码"
"查找 BroadcastReceiver 注册但未注销的代码"

# 协程和线程
"查找所有在主线程调用 Retrofit execute 的代码"
"查找所有在主线程操作数据库的代码"
"查找所有自定义 CoroutineScope 未 cancel 的代码"

# 资源管理
"查找所有 BitmapFactory.decode 未 recycle 的代码"
"查找所有 Hive.openBox 未 close 的代码"
"查找所有 FileInputStream 未 close 的代码"

# MagicFrame 特定
"查找所有处理 IoT 消息未验证格式的代码"
"查找所有下载任务无限重试的代码"
"查找所有 XEventBus.post 但未 subscribe 的代码"
```

---

## 总结

针对 MagicFrame Android 项目的缺陷检测重点:

1. **内存管理**: Context 泄漏、LiveData/Flow 泄漏、Bitmap 回收
2. **生命周期**: 协程作用域、监听器注销、广播接收器
3. **线程安全**: ANR 风险、主线程阻塞、协程调度
4. **数据安全**: 签名密钥、IoT 消息验证、数据库迁移
5. **性能优化**: WorkManager 约束、下载重试、资源释放

**项目特定关注**:
- Repository + ViewModel 架构正确使用
- Room + Coroutines + Flow 配合
- MQTT IoT 消息处理安全
- 下载管理器资源控制
- XEventBus 事件总线使用
- MMKV 替代 SharedPreferences
- LeakCanary 内存泄漏检测
