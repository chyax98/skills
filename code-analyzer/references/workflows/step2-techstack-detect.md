# Step 2: 技术栈识别

## 目标

自动识别项目的技术栈,加载对应的缺陷检测规则和最佳实践。

## 支持的技术栈

| 技术栈 | 识别特征 | 规则模板 |
|--------|---------|---------|
| Java + SpringBoot | pom.xml + @SpringBootApplication | @templates/java-springboot/ |
| Python | requirements.txt / pyproject.toml / setup.py | @templates/python/ |
| JavaScript/TypeScript + Node.js | package.json + Node modules | @templates/javascript-typescript/ |
| Flutter + Dart | pubspec.yaml + .dart 文件 | @templates/flutter-dart/ |
| Kotlin + Android | build.gradle + .kt 文件 + AndroidManifest.xml | @templates/kotlin-android/ |

> 🚀 **扩展性**: 架构支持多语言扩展,参见主文档 ARCHITECTURE.md "扩展示例"章节

## 识别流程

### 1. 扫描项目根目录

检查标志性文件:

```bash
# Java 项目
ls pom.xml build.gradle

# Python 项目
ls requirements.txt pyproject.toml setup.py

# JavaScript/TypeScript 项目
ls package.json

# Flutter 项目
ls pubspec.yaml

# Android 项目
ls app/build.gradle AndroidManifest.xml
```

### 2. Java + SpringBoot 识别

**必要条件**:

- 存在 `pom.xml` 或 `build.gradle`
- 包含 `spring-boot-starter` 依赖

**检测命令**:

```bash
# Maven 项目
grep -q "spring-boot-starter" pom.xml && echo "SpringBoot"

# Gradle 项目
grep -q "spring-boot-starter" build.gradle && echo "SpringBoot"

# 检查代码中是否有 @SpringBootApplication
grep -r "@SpringBootApplication" src/
```

**版本检测**:

```bash
# Maven
grep "<spring-boot.version>" pom.xml

# Gradle
grep "springBootVersion" build.gradle
```

### 3. Flutter + Dart 识别

**必要条件**:

- 存在 `pubspec.yaml`
- 包含 Flutter SDK 依赖
- 存在 `.dart` 文件

**检测命令**:

```bash
# 检查 pubspec.yaml
ls pubspec.yaml && echo "Flutter project found"

# 检查 Flutter SDK 依赖
grep -q "flutter:" pubspec.yaml && echo "Flutter SDK found"

# 检查 Dart 文件
find lib -name "*.dart" | head -1
```

**特定框架检测**:

```bash
# GetX 状态管理
grep -q "get:" pubspec.yaml && echo "Using GetX"

# Dio 网络库
grep -q "dio:" pubspec.yaml && echo "Using Dio"

# Hive 本地存储
grep -q "hive:" pubspec.yaml && echo "Using Hive"
```

**MagicFrame App 特征**:

```bash
# 检查是否为 MagicFrame App 项目
grep -q "magic_frame_app" pubspec.yaml
```

### 4. Kotlin + Android 识别

**必要条件**:

- 存在 `build.gradle` (kotlin-android plugin)
- 存在 `AndroidManifest.xml`
- 存在 `.kt` 文件

**检测命令**:

```bash
# 检查 build.gradle
grep -q "kotlin-android" build.gradle && echo "Kotlin Android found"

# 检查 AndroidManifest
ls app/src/main/AndroidManifest.xml

# 检查 Kotlin 文件
find app/src/main/java -name "*.kt" | head -1
```

**架构和库检测**:

```bash
# Room 数据库
grep -q "androidx.room:room" build.gradle && echo "Using Room"

# Coroutines
grep -q "kotlinx-coroutines" build.gradle && echo "Using Coroutines"

# ViewModel
grep -q "androidx.lifecycle:lifecycle-viewmodel" build.gradle && echo "Using ViewModel"

# WorkManager
grep -q "androidx.work:work" build.gradle && echo "Using WorkManager"
```

**MagicFrame Android 特征**:

```bash
# 检查是否为 MagicFrame Android 项目
grep -q "com.hillsdale.magic_frame" app/build.gradle
```

## 加载规则模板

根据识别结果,加载对应的规则模板:

### Java + SpringBoot

```
templates/java-springboot/
└── defect-rules.md         # 8大缺陷检测规则
```

### Python

```
templates/python/
└── defect-rules.md         # Python 缺陷检测规则
```

### JavaScript/TypeScript

```
templates/javascript-typescript/
└── defect-rules.md         # JS/TS 缺陷检测规则
```

### Flutter + Dart

```
templates/flutter-dart/
└── defect-rules.md         # Flutter/Dart 缺陷检测规则 (MagicFrame App 专用)
```

### Kotlin + Android

```
templates/kotlin-android/
└── defect-rules.md         # Kotlin/Android 缺陷检测规则 (MagicFrame Android 专用)
```

## 混合技术栈处理

如果项目包含多种技术栈:

1. 按变更文件的扩展名分组
2. 对每组应用对应的规则
3. 汇总所有检测结果

**示例**: 前后端分离项目

```
src/
├── backend/  (Java + SpringBoot) → 使用 java-springboot 规则
└── frontend/ (React + TypeScript) → 暂不支持,仅记录变更
```

## 输出

识别结果:

```json
{
  "techstack": "java-springboot",
  "version": "3.2.0",
  "build_tool": "maven",
  "template_path": "templates/java-springboot/",
  "confidence": "high",
  "evidence": [
    "pom.xml exists",
    "spring-boot-starter-web found in dependencies",
    "@SpringBootApplication found in src/main/java/Application.java"
  ]
}
```

## MCP 工具使用

**不使用 MCP**: 此步骤仅使用文件扫描和 grep 即可完成。

## 注意事项

1. **多模块项目**: 分别识别每个模块的技术栈
2. **版本兼容**: 注意 SpringBoot 2.x 和 3.x 的差异
3. **微服务**: 如果是微服务,需要识别每个服务的技术栈
4. **本地检查**: 基于本地代码库识别,不需要网络请求

## 常见问题

**Q: 如果识别失败怎么办?**

A: 要求用户明确指定技术栈或提供识别特征。

**Q: 如何支持新的技术栈?**

A: 参见 ARCHITECTURE.md "扩展示例"章节,在 templates/ 目录下新增对应模板。

## 下一步

→ **Step 3**: 缺陷检测 (@step3-defect-detect.md)
