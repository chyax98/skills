---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform Claude from a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Claude as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when Claude will use the skill. Be specific about what the skill does and when to use it. Use the third-person (e.g. "This skill should be used when..." instead of "Use this skill when...").

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by Claude for patching or environment-specific adjustments

##### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform Claude's process and thinking.

- **When to include**: For documentation that Claude should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window. Keep only essential procedural instructions and workflow guidance in SKILL.md; move detailed reference material, schemas, and examples to references files.

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables Claude to use files without loading them into context

#### What to Not Include in a Skill

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files, including:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

The skill should only contain the information needed for an AI agent to do the job at hand. It should not contain auxiliary context about the process that went into creating it, setup and testing procedures, user-facing documentation, etc. Creating additional documentation files just adds clutter and confusion.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited*)

*Unlimited because scripts can be executed without reading into context window.

## Skill Creation Process

To create a skill, follow the "Skill Creation Process" in order, skipping steps only if there is a clear reason why they are not applicable.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful to store in the skill

Example: When designing a `frontend-webapp-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

When creating a new skill from scratch, always run the `init_skill.py` script. The script conveniently generates a new template skill directory that automatically includes everything a skill requires, making the skill creation process much more efficient and reliable.

Usage:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script:

- Creates the skill directory at the specified path
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`
- Adds example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of Claude to use. Focus on including information that would be beneficial and non-obvious to Claude. Consider what procedural knowledge, domain-specific details, or reusable assets would help another Claude instance execute these tasks more effectively.

#### Start with Reusable Skill Contents

To begin implementation, start with the reusable resources identified above: `scripts/`, `references/`, and `assets/` files. Note that this step may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `assets/`, or documentation to store in `references/`.

Also, delete any example files and directories not needed for the skill. The initialization script creates example files in `scripts/`, `references/`, and `assets/` to demonstrate structure, but most skills won't need all of them.

#### Update SKILL.md

**Writing Style:** Write the entire skill using **imperative/infinitive form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "You should do X" or "If you need to do X"). This maintains consistency and clarity for AI consumption.

**DEPTH Framework:** For complex skills with multi-step workflows, apply the DEPTH framework to enhance quality and effectiveness. See the DEPTH Framework section below for detailed guidance.

To complete SKILL.md, answer the following questions:

1. What is the purpose of the skill, in a few sentences?
2. When should the skill be used?
3. In practice, how should Claude use the skill? All reusable skill contents developed above should be referenced so that Claude knows how to use them.

### Step 5: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**
1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

## DEPTH Framework

The DEPTH framework is a comprehensive methodology for creating high-quality, production-ready skills with multi-step workflows. Apply this framework to skills that involve complex processes, multiple decision points, or require consistent quality assurance.

**When to Use DEPTH:**
- Skills with 3+ workflow steps
- Skills requiring quality validation
- Skills involving analysis or generation tasks
- Skills needing context gathering or decision-making

**When to Skip DEPTH:**
- Simple utility skills with single actions
- Skills wrapping existing tools without complex logic
- Skills with straightforward, linear processes

### DEPTH Components

DEPTH is an acronym representing five essential components:

**D - Define Multi-Role Perspectives**
**E - Establish Success Metrics**
**P - Provide Context Collection**
**T - Task Breakdown**
**H - Human Feedback Loop (Self-Assessment)**

Each component addresses a specific aspect of skill quality and should be integrated into the appropriate workflow section.

### D - Define Multi-Role Perspectives (DEPTH: D)

**Purpose:** Establish expert role collaboration to ensure comprehensive coverage of different skill aspects.

**When to Include:** Add near the beginning of SKILL.md, after the introduction but before the workflow steps.

**Structure:**
```markdown
## Multi-Role Collaboration Framework (DEPTH: D)

[Brief description of how roles collaborate to accomplish the skill's goal]

**[Role 1 Name]**:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

**[Role 2 Name]**:
- [Responsibility 1]
- [Responsibility 2]

**[Role 3 Name]**:
- [Responsibility 1]
- [Responsibility 2]
```

**Examples:**

For a code analysis skill:
- **Test Analyst**: Parse changes, analyze impact, determine test scope
- **Security Reviewer**: Detect vulnerabilities, identify risks
- **Code Quality Inspector**: Check code quality, identify performance issues
- **Requirements Validator**: Verify implementation against requirements

For a presentation generation skill:
- **Content Architect**: Design structure, organize information
- **Domain Researcher**: Gather information, extract key concepts
- **Visual Designer**: Select layouts, balance visual elements
- **Quality Reviewer**: Validate specifications, check completeness

**Best Practices:**
- Define 3-5 specialized roles (not too many)
- Each role should have clear, distinct responsibilities
- Roles should cover all aspects of the skill's domain
- Reference roles in workflow steps to show when each role is active

### E - Establish Success Metrics (DEPTH: E)

**Purpose:** Define clear, measurable criteria for determining when the skill has successfully completed its task.

**When to Include:** Add to the final or validation step of the workflow, typically near the end of the process.

**Structure:**
```markdown
### Step N: [Final Step Name] (DEPTH: E)

**[Role Name]**:

[Description of what this step does]

**Success Criteria**:
1. **[Category 1]**: [Specific measurable criterion]
2. **[Category 2]**: [Specific measurable criterion]
3. **[Category 3]**: [Specific measurable criterion]
4. **[Category 4]**: [Specific measurable criterion]
5. **[Category 5]**: [Specific measurable criterion]
```

**Examples:**

For a code analysis skill:
- **Defect Coverage**: All critical security and quality issues identified
- **Requirement Compliance**: All requirement features validated
- **Impact Analysis**: Complete regression test scope determined
- **Risk Assessment**: Accurate risk level and priority assigned
- **Report Quality**: Clear, actionable recommendations provided

For a mindmap generation skill:
- **Structure Metrics**: Main branches 3-7, depth 2-5 levels, nodes 1-2 lines
- **Content Quality**: Key concepts present, no redundancy, clear terminology
- **Mind Map Principles**: Radiant thinking structure, dimensional organization
- **Format Compliance**: Proper heading hierarchy, correct Markdown syntax

**Best Practices:**
- Define 4-6 measurable success criteria
- Make criteria specific and verifiable
- Cover different quality dimensions (completeness, accuracy, format)
- Include both technical and content quality metrics

### P - Provide Context Collection (DEPTH: P)

**Purpose:** Systematically gather essential background information before beginning work to ensure the skill has all necessary context.

**When to Include:** Add as "Step 0" at the very beginning of the workflow, before any actual processing starts.

**Structure:**
```markdown
### Step 0: Background Information Collection (DEPTH: P)

Before [starting main task], collect essential context:

**Required Information**:
1. **[Category 1]**: [What to determine]
2. **[Category 2]**: [What to determine]
3. **[Category 3]**: [What to determine]
4. **[Category 4]**: [What to determine]

**Information Gathering**:
- When [condition]: [Action]
- When [condition]: [Action]
- When [condition]: [Action]
```

**Examples:**

For a presentation generation skill:
- **Content Domain**: Identify the field (Technology/Business/Science/Arts)
- **Target Audience**: Determine viewer level (Beginner/Intermediate/Expert)
- **Presentation Purpose**: Clarify the goal (Teaching/Research/Algorithm/Project)
- **Depth Requirement**: Overview/Detailed/Expert-level
- **Time Constraint**: Presentation duration
- **Special Requirements**: Code examples, diagrams, specific topics

For a code analysis skill:
- **Requirement Description**: Detailed requirement or feature description
- **Git Range**: Specify branch or commit range to analyze
- **Analysis Depth**: Quick scan or comprehensive analysis
- **Priority Focus**: Security/Performance/Functionality

**Best Practices:**
- Identify 4-6 key pieces of context needed
- Specify how to gather information (from user, from files, from inference)
- Include fallback strategies when information is unclear
- Keep this step focused on gathering, not processing

### T - Task Breakdown (DEPTH: T)

**Purpose:** Break down complex workflow steps into explicit sub-tasks to ensure thorough execution and nothing is missed.

**When to Include:** Add to complex workflow steps that involve multiple operations or decision points.

**Structure:**
```markdown
### Step N: [Step Name] (DEPTH: T)

**[Role Name]**:

[Description of overall step goal]

**Task Breakdown**:
1. **[Subtask 1]**: [Description]
2. **[Subtask 2]**: [Description]
3. **[Subtask 3]**: [Description]
4. **[Subtask 4]**: [Description]
5. **[Subtask 5]**: [Description]

[Additional step details...]
```

**Examples:**

For a content generation step:
- **Frontmatter Configuration**: Set theme, title, fonts, layout defaults
- **Opening Slides**: Title, agenda, learning objectives
- **Content Slides**: Core concepts, explanations, examples
- **Code Slides**: Syntax highlighting, line highlighting, annotations
- **Visual Slides**: Diagrams, charts, architecture illustrations
- **Closing Slides**: Summary, Q&A, references

For a defect detection step:
- **Security Vulnerabilities**: SQL injection, XSS, command injection
- **Resource Management**: Resource leaks, connection management
- **Error Handling**: Exception handling, Promise rejections
- **Concurrency Issues**: Race conditions, thread safety
- **Performance**: N+1 queries, inefficient algorithms
- **Type Safety**: Type annotations, null checks

**Best Practices:**
- Break down into 4-7 logical subtasks
- Each subtask should represent a distinct operation
- Order subtasks logically (sequential or by category)
- Make subtasks specific and actionable

### H - Human Feedback Loop / Self-Assessment (DEPTH: H)

**Purpose:** Enable systematic self-evaluation before finalizing output to catch issues and ensure quality standards are met.

**When to Include:** Add as the final step before output, after all processing is complete but before delivering results.

**Structure:**
```markdown
### Step N: Self-Assessment (DEPTH: H)

**[Role Name(s)]**:

Before finalizing [output type], perform self-evaluation to ensure quality:

**[Assessment Category 1]**:
- [Check 1]?
- [Check 2]?
- [Check 3]?

**[Assessment Category 2]**:
- [Check 1]?
- [Check 2]?

**[Assessment Category 3]**:
- [Check 1]?
- [Check 2]?

**Action on Assessment**:
- If [condition]: [Action]
- If [condition]: [Action]
- If passed: [Action]
```

**Examples:**

For a presentation generation skill:
- **Content Structure Assessment**: Logical flow, learning objectives met, balanced density
- **Technical Accuracy Check**: Code examples correct, technical terms accurate
- **Visual Design Evaluation**: Text readable, layouts appropriate, colors consistent
- **Audience Appropriateness**: Terminology suitable, explanations detailed enough
- **Slidev Compliance Check**: Frontmatter configured, separators correct
- **Common Issues Avoidance**: No overcrowded slides, no missing language identifiers

For a mindmap generation skill:
- **Mind Map Philosophy Check**: Radiant thinking, dimensional organization, no document sections
- **Content Quality Assessment**: Meaningful concepts, similar abstraction levels, logical progression
- **Structure Balance Check**: Main branches 3-7, balanced depth, brief nodes
- **Completeness Verification**: Core dimensions covered, key concepts explained
- **Common Pitfall Avoidance**: No tutorial sections, no chronological organization

**Best Practices:**
- Organize checks into 4-6 logical categories
- Phrase checks as yes/no questions for clarity
- Include both technical and content quality checks
- Always specify what action to take based on assessment results
- Reference the success criteria (DEPTH: E) defined earlier

### DEPTH Integration Checklist

When applying DEPTH to a skill, verify:

- [ ] **D - Multi-Role Framework**: Defined 3-5 expert roles with clear responsibilities
- [ ] **E - Success Metrics**: Established 4-6 measurable success criteria in final/validation step
- [ ] **P - Context Collection**: Created Step 0 with 4-6 essential context items
- [ ] **T - Task Breakdown**: Added detailed subtasks (4-7 items) to complex workflow steps
- [ ] **H - Self-Assessment**: Created final assessment step with 4-6 quality check categories

### DEPTH Examples

Reference these skills as complete DEPTH framework implementations:

- **code-analyzer**: Shift-left testing with multi-language support
  - Roles: Test Analyst, Security Reviewer, Code Quality Inspector, Requirements Validator
  - Success Metrics: Defect coverage, requirement compliance, impact analysis, risk assessment, report quality
  - Context: Requirement description, Git range, analysis depth, priority focus
  - Example of comprehensive DEPTH integration

- **slides-generator**: Slidev presentation generation
  - Roles: Content Architect, Domain Researcher, Visual Designer, Quality Reviewer
  - Success Metrics: Content structure, technical accuracy, visual design, audience appropriateness, Slidev compliance
  - Context: Content domain, target audience, presentation purpose, depth requirement, time constraint
  - Example of content creation workflow with DEPTH

- **mindmap-generator**: Markdown mindmap generation
  - Roles: Mind Map Architect, Domain Researcher, Knowledge Organizer, Quality Reviewer
  - Success Metrics: Structure metrics, content quality, mind map principles compliance
  - Context: Topic domain, target audience, primary purpose, depth requirement
  - Example of structured thinking tool with DEPTH

These examples demonstrate how DEPTH components integrate seamlessly into different types of skills while maintaining the core framework principles.

---

## 常见问题（基于官方规范）

**Q: 何时使用 DEPTH 框架？**

A: DEPTH 是**设计指南**，用于创建 skill 时的思考框架。但在最终的 SKILL.md 中：
- ❌ 不要显式标注 `(DEPTH: X)`
- ✅ 理解其思想并隐式应用
- 官方 skills 不使用 DEPTH 标记

**Q: 检查清单应该多详细？**

A: **必须详细完备**。流程型 skill 的检查清单通常有 20-40 项，每个检查项必须明确，包含修正动作。

**Q: 如何平衡简洁和完备？**

A:
- 流程步骤：简洁（每阶段 3-5 点）
- 检查清单：完备（详细列出）
- 示例：适度（每功能 1-2 个）

**Q: 官方推荐的流程型结构？**

A: Phase/Stage 阶段化 + Checklist + CRITICAL 标记 + 保持 <500 行
