---
name: java-git-defect-analyzer
description: This skill should be used when the user wants to analyze Java code changes in Git commits against requirement documents to identify functional defects, implementation gaps, and high-impact code issues with prioritized fix suggestions.
license: Apache-2.0
---

# Java Git Defect Analyzer

Comprehensive code review skill for analyzing Java projects by comparing Git commit changes against requirement documents to identify functional defects, implementation gaps, and code quality issues.

## Overview

This skill performs **requirement-driven code analysis** focusing on:
1. **Functional Defect Detection** (Primary): Verifying code changes match requirement specifications
2. **High-Impact Bug Detection**: Identifying critical issues (NPE, resource leaks, security vulnerabilities)
3. **Code Quality Assessment**: Detecting low-priority issues that don't significantly impact functionality

The analysis prioritizes functional correctness over code style, ensuring implementations fulfill business requirements.

## When to Use

Activate this skill when the user needs to:
- Review code changes with keywords like `review-java`
- Verify if a Git commit properly implements specified requirements
- Identify functional gaps between requirements and implementation
- Detect high-impact defects that could cause runtime failures
- Generate prioritized issue lists with actionable fix suggestions

**Typical Scenarios**:
- Pre-merge PR reviews with requirement documentation
- Post-commit verification against feature specifications
- Sprint review code quality checks
- Technical debt assessment focusing on functional correctness

## How It Works

### Step 1: Input Collection

Gather two essential inputs:
1. **Requirement Document**: Feature specification, user story, or technical design document
   - Accepted formats: Markdown, plain text, or inline description
   - Should clearly describe expected functionality and business logic
2. **Git Commit Reference**: Commit hash, branch name, or `HEAD`
   - Will analyze the code changes introduced in this commit

**Example Interaction**:
```
User: review-java
You: 请提供以下信息:
     1. 需求文档 (文件路径或直接粘贴)
     2. Git commit reference (默认: HEAD)
```

### Step 2: Extract Code Changes

Execute `scripts/analyze_commit.py` to extract Java code modifications:

```bash
python scripts/analyze_commit.py <commit_hash>
```

**Output**:
- List of modified Java files
- Added/deleted/modified methods
- Code diff context (±5 lines)
- Change summary (new classes, modified logic, deleted code)

**Key Focus**:
- Extract method signatures and implementation logic
- Identify new business logic vs. refactoring
- Capture error handling and edge cases

### Step 3: Requirement Matching Analysis

Execute `scripts/requirement_matcher.py` to compare requirements against implementation:

```bash
python scripts/requirement_matcher.py \
    --requirement <requirement_doc> \
    --commit <commit_hash>
```

**Analysis Process**:

**3.1 Extract Requirement Features**
- Parse requirement document to identify key functional points
- Extract expected behaviors, business rules, data flows
- Identify mandatory vs. optional features

**3.2 Map Code to Requirements**
- Match code changes to requirement specifications
- Verify business logic implementation completeness
- Check data validation and error handling

**3.3 Gap Analysis**
- Identify missing functionality (requirement exists, code doesn't)
- Detect implementation deviations (code behaves differently than specified)
- Flag incomplete implementations (partial logic, missing edge cases)

**Reference**: `references/functional_defect_patterns.md` for common functional defect patterns
**Reference**: `references/requirement_checklist.md` for systematic verification checklist

### Step 4: High-Impact Defect Detection

Execute `scripts/defect_detector.py` on code changes to identify critical bugs:

```bash
python scripts/defect_detector.py <commit_hash>
```

**Detection Categories** (by priority):

**🔴 CRITICAL - High-Impact Bugs**:
- **NPE Risks**: Method calls on potentially null objects without null checks
- **Resource Leaks**: Unclosed `Connection`, `InputStream`, `Statement`, `ResultSet`
- **SQL Injection**: String concatenation in SQL queries
- **Hardcoded Secrets**: Passwords, API keys, tokens in code
- **Concurrency Issues**: Race conditions, improper synchronization

**🟡 MEDIUM - Moderate Impact**:
- **Error Handling**: Missing try-catch, swallowed exceptions
- **Transaction Issues**: Database operations without transaction boundaries
- **Performance**: Inefficient algorithms with measurable impact (N+1 queries)

**Reference**: `references/critical_bugs.md` for detailed defect patterns and detection rules

### Step 5: Priority Classification

Classify all detected issues using `assets/priority_matrix.json`:

**Priority Levels**:

**🔴 CRITICAL** (Score: 10):
- Complete functional requirement missing
- Core business logic error causing incorrect behavior
- Business process interruption or data corruption risk

**🟠 HIGH** (Score: 7-9):
- Partial requirement implementation (incomplete features)
- Implementation deviation from specification
- High-impact bugs: NPE, resource leaks, security vulnerabilities

**🟡 MEDIUM** (Score: 4-6):
- Performance issues with actual user impact
- Concurrency problems in multi-threaded scenarios
- Incomplete error handling for edge cases

**🟢 LOW** (Score: 1-3):
- Code formatting and style issues
- Naming convention violations
- Missing or incomplete comments
- Minor performance optimizations with negligible impact

### Step 6: Generate Issue Report

Create a structured Markdown report with:

**Report Structure**:

```markdown
# Java Code Review Report

## Executive Summary
- Total Issues: X
- Critical: X | High: X | Medium: X | Low: X
- Requirement Match Score: X/10

## 🔴 CRITICAL - Functional Defects

### Issue 1: [缺失功能描述]
- **Requirement**: [需求原文引用]
- **Implementation Status**: ❌ 完全缺失 / ⚠️ 实现不完整
- **Impact**: [业务影响说明]
- **Location**: `ClassName.java:line_number`
- **Fix Suggestion**:
  ```java
  // 建议实现代码
  ```
- **Explanation**: [修复说明]

## 🟠 HIGH - Implementation Gaps & Critical Bugs

### Issue 2: [功能偏差/高影响缺陷]
- **Type**: Functional Deviation / NPE Risk / Resource Leak / Security
- **Problem**: [问题详细描述]
- **Code Location**: `ClassName.java:line_number`
- **Current Code**:
  ```java
  // 问题代码
  ```
- **Fix Suggestion**:
  ```java
  // 修复后代码
  ```
- **Explanation**: [为什么这样修复]

## 🟡 MEDIUM - Moderate Impact Issues

[同上结构,简化说明]

## 🟢 LOW - Code Quality Improvements

[简要列表,不详细展开]
- 命名规范问题: [文件:行号]
- 格式问题: [文件:行号]

## Requirement Coverage Analysis

| 需求功能点 | 实现状态 | 问题说明 |
|-----------|---------|---------|
| 用户登录 | ✅ 完整实现 | - |
| 日志记录 | ❌ 缺失 | 未记录登录日志 |
| 邮箱验证 | ⚠️ 部分实现 | 仅支持手机号 |

## Recommendations

1. 优先修复 CRITICAL 功能缺陷
2. 处理 HIGH 级别的安全和稳定性问题
3. MEDIUM 和 LOW 问题可在后续迭代优化
```

### Step 7: Interactive Refinement

Present the report to the user and offer:
- **Clarification**: Explain any unclear issues
- **Prioritization Adjustment**: Re-classify issues based on user feedback
- **Deep Dive**: Provide detailed analysis for specific issues
- **Fix Guidance**: Offer step-by-step implementation guidance

## Resources

### Scripts (`scripts/`)

**`analyze_commit.py`**
- Extracts Java code changes from Git commits
- Parses method signatures and implementation logic
- Generates structured change summaries

**`requirement_matcher.py`**
- Compares requirement documents with code implementation
- Identifies functional gaps and deviations
- Produces requirement coverage matrix

**`defect_detector.py`**
- Applies pattern matching for common Java defects
- Detects high-impact bugs (NPE, leaks, security)
- Uses regex and heuristic rules from reference documents

### References (`references/`)

**`functional_defect_patterns.md`**
- Common functional defect patterns (missing features, logic errors)
- Requirement verification techniques
- Business logic validation checklist

**`requirement_checklist.md`**
- Systematic requirement verification steps
- Data consistency validation rules
- Exception handling verification guide

**`critical_bugs.md`**
- High-impact bug patterns (NPE, resource leaks, SQL injection)
- Security vulnerability patterns
- Concurrency issue detection rules

**`low_priority_issues.md`**
- Code style and formatting guidelines
- Naming convention standards
- Comment and documentation requirements

### Assets (`assets/`)

**`priority_matrix.json`**
- Issue severity scoring configuration
- Priority level definitions
- Category-to-severity mapping rules

## Best Practices

### For Effective Analysis

1. **Provide Clear Requirements**: Detailed requirement documents yield better analysis
2. **Commit Scope**: Analyze focused commits (single feature) for clearer results
3. **Context Matters**: Include relevant background info for complex business logic
4. **Iterative Review**: Use for incremental commits during development, not just final review

### For Interpreting Results

1. **Prioritize Functionally**: Fix functional defects before code style issues
2. **Validate Findings**: Some detected issues may be false positives, verify before fixing
3. **Context-Aware Decisions**: LOW priority issues in critical paths may need upgrading
4. **Track Over Time**: Use consistently to measure code quality trends

### For Fix Implementation

1. **Address Root Causes**: Don't just fix symptoms, understand why the issue occurred
2. **Comprehensive Testing**: Add unit tests for fixed defects
3. **Document Changes**: Update requirement docs if implementation intentionally deviates
4. **Review Again**: Re-run analysis after fixes to verify resolution

## Examples

### Example 1: Functional Gap Detection

**Requirement**:
```
用户登录成功后,系统需要:
1. 记录登录日志(时间、IP、设备)
2. 发送登录通知邮件
3. 更新最后登录时间
```

**Code Review Output**:
```markdown
## 🔴 CRITICAL - Functional Defects

### 缺失功能: 登录日志记录
- **Requirement**: 记录登录日志(时间、IP、设备)
- **Implementation Status**: ❌ 完全缺失
- **Location**: `UserController.java:45`
- **Fix Suggestion**:
  ```java
  @PostMapping("/login")
  public ResponseEntity<UserVO> login(@RequestBody LoginRequest request) {
      User user = authService.authenticate(request);

      // 🔴 添加日志记录
      LoginLog log = new LoginLog();
      log.setUserId(user.getId());
      log.setLoginTime(LocalDateTime.now());
      log.setIpAddress(request.getRemoteAddr());
      log.setDeviceInfo(request.getHeader("User-Agent"));
      loginLogService.save(log);

      return ResponseEntity.ok(userMapper.toVO(user));
  }
  ```
```

### Example 2: High-Impact Bug Detection

**Code**:
```java
public User getUserById(Long id) {
    User user = userRepository.findById(id);
    return user.getUsername(); // 🔴 NPE Risk
}
```

**Analysis Output**:
```markdown
## 🟠 HIGH - NPE Risk

### NPE 风险: 未检查 null
- **Location**: `UserService.java:23`
- **Problem**: `findById()` 可能返回 null, 直接调用 `getUsername()` 会抛出 NPE
- **Fix Suggestion**:
  ```java
  public String getUserById(Long id) {
      User user = userRepository.findById(id);
      if (user == null) {
          throw new UserNotFoundException("User not found: " + id);
      }
      return user.getUsername();
  }
  ```
```

### Example 3: Priority Classification

**Mixed Issues**:
- Missing email notification (CRITICAL - functional requirement)
- NPE in error handler (HIGH - runtime failure risk)
- Inefficient loop (MEDIUM - measurable performance impact)
- Variable naming `usrNm` (LOW - readability, no functional impact)

**Report Prioritization**:
```
🔴 CRITICAL (1):
  - Missing email notification → Fix immediately

🟠 HIGH (1):
  - NPE in error handler → Fix before merge

🟡 MEDIUM (1):
  - Inefficient loop → Optimize in next sprint

🟢 LOW (1):
  - Variable naming → Tech debt backlog
```

## Notes

- **Token Efficiency**: Reference documents loaded on-demand only when specific defect types detected
- **Customization**: Edit `assets/priority_matrix.json` to adjust severity scoring for your team
- **Script Requirements**: Python 3.8+, GitPython library for script execution
- **False Positives**: Static analysis may flag intentional patterns, human review recommended
- **Continuous Improvement**: Contribute new defect patterns to reference documents as discovered
