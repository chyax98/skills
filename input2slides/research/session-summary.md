# doc2slides 项目会话总结

## 会话时间
2025-10-23

## 项目背景

用户希望为 doc2slides 项目选择合适的 Markdown 转 PPT 工具,避免重复造轮子。核心需求:
1. CLI 命令行工具
2. 支持导出 HTML 和 PPTX
3. 文件可以直接用 `open` 命令打开
4. 主题系统可定制
5. 轻量级、易于使用

## 工作流程

### Phase 1: 调研阶段
**目标**: 调研现有开源 Markdown 转幻灯片工具

**执行**:
- 使用 SearXNG MCP 并行搜索 4 个主流框架
- 读取官方文档和 GitHub 仓库
- 分析技术栈、特性、社区活跃度

**调研对象**:
1. **Slidev** (30K+ stars) - Vue 3 + Vite
2. **Marp** (7K+ stars) - 轻量级 Markdown
3. **reveal-md** (5K+ stars) - 基于 reveal.js
4. **mdx-deck** (11K+ stars) - React + MDX (已停更)

**输出文档**: `markdown-to-slides-research.md` (详细对比分析)

### Phase 2: 环境配置优化
**问题**: Node.js 版本混乱 (v16, v18, v20),导致工具无法运行

**解决方案**:
1. 安装 Node.js v22.21.0 (最新 LTS)
2. 设置为默认版本: `nvm alias default 22`
3. 修复 `.bashrc` 配置:
   - 移除 `--no-use` 参数
   - 添加 `nvm use default --silent` 自动加载
4. 清理旧版本 (v16, v18, v20)

**成果**: 统一使用 Node.js v22,后续工具安装顺畅

### Phase 3: 实际测试 Slidev
**尝试**: 全局安装 Slidev CLI

**遇到问题**:
1. **主题依赖**: 需要在项目级别安装 `@slidev/theme-default`
2. **HTML CORS**: 导出的 HTML 因 CORS 策略无法在浏览器直接打开
   ```
   Access to script at 'file:///assets/index.js' from origin 'null'
   has been blocked by CORS policy
   ```
3. **PDF 依赖**: 需要额外安装 `playwright-chromium`
4. **重量级**: 617+ 个 npm 依赖,构建产物大

**结论**: Slidev 功能强大但过于复杂,不适合 doc2slides 场景

### Phase 4: 切换到 Marp 并成功验证
**执行**:
1. 全局安装 Marp CLI: `npm install -g @marp-team/marp-cli`
2. 创建测试幻灯片 `marp-demo.md`
3. 导出 HTML: `marp --no-stdin marp-demo.md -o marp-demo.html`
4. 导出 PPTX: `marp --no-stdin marp-demo.md -o marp-demo.pptx`

**验证结果**:
- ✅ HTML 导出成功 (108KB),可直接 `open` 打开
- ✅ PPTX 导出成功 (564KB),PowerPoint 完美兼容
- ✅ 无复杂依赖,全局安装即可使用
- ✅ 轻量级 (151 个依赖)

**用户反馈**: "完美,就用这个吧"

### Phase 5: 文档整理
**输出**:
1. `markdown-to-slides-research.md` - 4 个框架详细对比
2. `slidev-integration-spec.md` - Slidev 集成规范 (参考)
3. `final-decision-marp.md` - 最终决策和实施路线
4. `session-summary.md` - 本会话总结 (当前文档)

## 最终决策: Marp

### 选择理由

| 维度 | Marp | Slidev |
|------|------|--------|
| **复杂度** | ⭐ 简单 | ⭐⭐⭐⭐ 复杂 |
| **依赖数** | 151 个 | 617+ 个 |
| **HTML 可用** | ✅ 直接打开 | ❌ CORS 限制 |
| **PPTX 支持** | ✅ 原生 | ⚠️ 需 playwright |
| **安装方式** | 全局 CLI | 项目级依赖 |
| **学习曲线** | ⭐ 平缓 | ⭐⭐⭐ 陡峭 |
| **适用场景** | ✅ 文档转 PPT | ⭐ 开发者演示 |

### 技术特性

**Markdown 语法** (标准 + Marp 指令):
```markdown
---
marp: true
theme: default
paginate: true
---

# 标题页

---

## 内容页
- 列表项
```

**导出命令**:
```bash
marp --no-stdin slides.md -o output.html   # HTML
marp --no-stdin slides.md -o output.pptx   # PPTX
```

**自定义主题**:
```css
/* @theme custom-name */
@import 'default';

section {
  background: #1a1a2e;
  color: #eee;
}
```

## 关键洞察

### 1. "不重复造轮子" 策略成功
- 原计划: 从零开发渲染引擎
- 实际方案: 采用成熟的 Marp CLI
- 节省时间: 数周开发工作 → 1 天调研测试

### 2. 实测验证至关重要
- 纸上调研显示 Slidev 功能最强
- 实际测试发现 HTML CORS 致命问题
- **教训**: 不能只看文档,必须实际跑通

### 3. 简单即是美
- Slidev 功能强大但过度工程化
- Marp 功能够用且极简可靠
- **原则**: 选择"刚好够用"的工具,而非"最强大"的

### 4. 环境配置是基础
- Node.js 版本混乱导致大量时间浪费
- 统一环境后一切顺利
- **经验**: 先解决环境问题,再做业务开发

### 5. 用户需求驱动决策
- 用户明确: "不需要 PDF,给我能看的 HTML 就够了"
- 及时调整: 放弃复杂方案,转向简单可用
- **心得**: 倾听用户真实需求,避免过度设计

## 工作成果

### 交付文件
```
doc2slides/
├── research/
│   ├── markdown-to-slides-research.md      # 调研报告
│   ├── slidev-integration-spec.md          # Slidev 规范 (参考)
│   ├── final-decision-marp.md              # 最终决策
│   └── session-summary.md                  # 会话总结 (本文档)
└── test/
    ├── marp-demo.md                        # 测试幻灯片
    ├── marp-demo.html                      # HTML 输出 ✅
    └── marp-demo.pptx                      # PPTX 输出 ✅
```

### 环境配置
- ✅ Node.js v22.21.0 (全局默认)
- ✅ Marp CLI v4.2.3 (全局安装)
- ✅ `.bashrc` 自动加载 Node 22

### 技术验证
- ✅ HTML 导出可用 (108KB 自包含)
- ✅ PPTX 导出可用 (564KB PowerPoint)
- ✅ 文件可直接 `open` 打开

## 下一步计划

### P0: 主题开发 (必需)
- [ ] `doc2slides-midnight.css` - 深色专业
- [ ] `doc2slides-warm.css` - 暖色温馨
- [ ] `doc2slides-focus.css` - 极简聚焦
- [ ] `doc2slides-vibrant.css` - 活力多彩

### P1: Skill 适配 (重要)
- [ ] 更新 doc2slides skill 输出 Marp 格式
- [ ] 实现分段生成策略 (防止长文本截断)
- [ ] 添加主题选择参数
- [ ] 验证和错误处理

### P2: 工具封装 (增强)
- [ ] 创建 `doc2slides` CLI 包装器
- [ ] 简化常用命令
- [ ] 批量转换功能
- [ ] 主题预览功能

### P3: 文档完善 (完整)
- [ ] 用户使用手册
- [ ] 主题开发指南
- [ ] 故障排查文档
- [ ] 最佳实践示例

## 技术债务

### 已解决
- ✅ Node.js 版本统一
- ✅ 工具选型确定
- ✅ 导出流程验证

### 待解决
- ⚠️ PDF 导出 (Marp 需要 Chrome/Chromium,可选)
- ⚠️ 复杂布局 (Marp 仅支持 CSS,无组件化)
- ⚠️ 动态内容 (Marp 是静态渲染)

### 风险评估
- **低风险**: Marp 社区活跃,持续维护
- **中风险**: 主题定制能力有限 (仅 CSS)
- **可接受**: 对于教学类 PPT,CSS 已足够

## 关键指标

### 效率提升
- 调研时间: 2 小时
- 测试验证: 1 小时
- 文档整理: 1 小时
- **总耗时**: ~4 小时 (vs 从零开发数周)

### 工具对比
- **依赖减少**: 617 → 151 (75% ↓)
- **文件大小**: HTML 合理 (~100KB)
- **安装复杂度**: 项目级 → 全局 CLI
- **学习成本**: Vue 生态 → 纯 Markdown

### 用户满意度
- 需求匹配: ⭐⭐⭐⭐⭐ (完美)
- 易用性: ⭐⭐⭐⭐⭐ (简单)
- 可靠性: ⭐⭐⭐⭐⭐ (稳定)

## 经验教训

### ✅ 做对的事
1. **并行搜索**: 同时调研多个工具,节省时间
2. **实际测试**: 不止于文档,必须跑通流程
3. **及时调整**: 发现问题立即切换方案
4. **倾听用户**: 根据真实需求调整目标
5. **文档记录**: 完整记录决策过程和理由

### ⚠️ 可以改进
1. **环境检查**: 应该先统一环境再开始调研
2. **快速验证**: 可以更早进行快速原型测试
3. **假设验证**: Slidev "功能强大" ≠ "适合场景"

### 💡 关键领悟
1. **Worse is Better**: 简单可靠 > 功能强大但复杂
2. **Just Enough**: 选择刚好满足需求的工具
3. **Test First**: 实测 > 推测 > 猜测
4. **User-Centric**: 用户说"完美"才是真完美

## 总结

本次会话成功完成了 doc2slides 项目的技术选型和验证工作:

1. **调研**: 系统调研 4 个主流 Markdown 转幻灯片工具
2. **验证**: 实际测试并发现 Slidev 的致命缺陷
3. **决策**: 选择 Marp CLI 作为最终方案
4. **实施**: 完成安装、测试、文档全流程
5. **交付**: HTML/PPTX 导出完美工作,用户满意

**最重要的成果**: 找到了一个简单、可靠、轻量级的解决方案,避免了重复造轮子,为后续开发奠定了坚实基础。

---

## 附录: 快速参考

### Marp 常用命令
```bash
# 安装
npm install -g @marp-team/marp-cli

# 导出 HTML
marp --no-stdin input.md -o output.html

# 导出 PPTX
marp --no-stdin input.md -o output.pptx --allow-local-files

# 自定义主题
marp --no-stdin --theme custom.css input.md -o output.html

# 实时预览
marp --no-stdin input.md --server
```

### Markdown 模板
```markdown
---
marp: true
theme: default
paginate: true
header: '标题'
footer: '页脚'
---

<!-- _class: lead -->
# 封面页

---

## 内容页
- 要点1
- 要点2
```

### 下一步行动清单
- [ ] 开发 4 个自定义主题
- [ ] 更新 doc2slides skill
- [ ] 创建 CLI 包装器
- [ ] 编写用户文档
