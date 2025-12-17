# DrawIO 布局约束规则

**核心原则：先规划布局，再生成 XML；避免连线穿越障碍物**

## 画布约束

```
坐标范围: x ∈ [40, 760], y ∈ [40, 560]
容器最大: 700×500
起始边距: 40px
页面尺寸: 800×600 (默认)
```

## 节点尺寸

| 类型 | 尺寸 (w×h) | 用途 |
|------|-----------|------|
| S | 80×40 | 简单标签、状态 |
| M | 120×60 | 标准节点、步骤 |
| L | 160×80 | 容器标题、重点 |

## 节点间距

**关键：间距要足够大以留出连线通道！**

| 级别 | 值 | 用途 |
|------|-----|------|
| 紧凑 | 60px | 同组内紧密节点 |
| 标准 | 120px | 普通节点间（推荐） |
| 宽松 | 180px | 需要复杂连线时 |

---

## 连线规则（核心！）

### Rule 1: 显式指定锚点

**每条连线必须指定 exitX/exitY/entryX/entryY**

```xml
style="edgeStyle=orthogonalEdgeStyle;exitX=1;exitY=0.5;entryX=0;entryY=0.5;endArrow=classic;"
```

### Rule 2: 标准连接点（不用角落！）

| 方向 | exit | entry |
|------|------|-------|
| 右→左 | exitX=1;exitY=0.5 | entryX=0;entryY=0.5 |
| 下→上 | exitX=0.5;exitY=1 | entryX=0.5;entryY=0 |
| 左→右 | exitX=0;exitY=0.5 | entryX=1;entryY=0.5 |
| 上→下 | exitX=0.5;exitY=0 | entryX=0.5;entryY=1 |

**❌ 禁止使用角落连接点**: `exitX=1;exitY=1` 或 `entryX=0;entryY=0`

### Rule 3: 双向连线用相反的边

```xml
<!-- A→B: 从 A 右侧出，从 B 左侧入 -->
<mxCell id="e1" style="...exitX=1;exitY=0.3;entryX=0;entryY=0.3..." source="a" target="b"/>

<!-- B→A: 从 B 左侧出，从 A 右侧入，使用不同的 Y 位置避免重叠 -->
<mxCell id="e2" style="...exitX=0;exitY=0.7;entryX=1;entryY=0.7..." source="b" target="a"/>
```

### Rule 4: 多条连线不能共享路径

如果两条连线连接相同节点对，必须使用不同的出入点：
- 第一条: `exitY=0.3`, `entryY=0.3`
- 第二条: `exitY=0.7`, `entryY=0.7`

### Rule 5: 障碍物避让（关键！）

**生成连线前必须检查：源和目标之间是否有其他节点？**

如果有障碍物，必须使用 waypoints 绕行：

```xml
<mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=1;entryX=0.5;entryY=0;endArrow=classic;" edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="150"/>  <!-- 绕行点1 -->
      <mxPoint x="400" y="150"/>  <!-- 绕行点2 -->
    </Array>
  </mxGeometry>
</mxCell>
```

**绕行原则**：
- 沿图表边缘外围绕行，不穿过中间
- 距离障碍物边界至少 30px
- 使用 L 形或 U 形路径

### Rule 6: 验证清单

生成连线前，对每条边问自己：
1. ❓ 这条线会穿过其他节点吗？→ 如果是，添加 waypoints
2. ❓ 有其他线共享同一路径吗？→ 如果是，调整 exit/entry Y 位置
3. ❓ 用了角落连接点吗？→ 如果是，改用边缘中点

---

## 布局模板

### 模板 A：水平流程

```
适用：流程图、工作流、时间线

[节点1] ──→ [节点2] ──→ [节点3]

规则：
- 所有节点 y 坐标相同
- 节点间距 120px
- 连线：exitX=1;exitY=0.5 → entryX=0;entryY=0.5
```

### 模板 B：垂直层级

```
适用：架构图、组织结构

       [顶层]
          ↓
    [中1]  [中2]  [中3]
          ↓
       [底层]

规则：
- 同层节点 x 坐标居中分布
- 层间距 120px
- 连线：exitX=0.5;exitY=1 → entryX=0.5;entryY=0
```

**重点：避免"一对多"连线交叉**

当顶层节点需要连接多个中层节点时：
- 方案1：使用不同的 exitY 位置 (0.3, 0.5, 0.7)
- 方案2：中层节点水平排列足够宽，连线自然分开

### 模板 C：网格布局

```
适用：卡片、图标、矩阵

[1]  [2]  [3]
[4]  [5]  [6]
```

### 模板 D：中心辐射

```
适用：API 网关、负载均衡

        [Client1]  [Client2]  [Client3]
              ↘      ↓      ↙
              [API Gateway]
              ↙      ↓      ↘
        [Svc1]    [Svc2]    [Svc3]

规则：
- 中心节点居中
- 上下两层节点水平分布
- 从中心向外辐射连线
```

---

## 标准颜色

| 语义 | 填充色 | 边框色 |
|------|--------|--------|
| 主要 | #dae8fc | #6c8ebf |
| 成功 | #d5e8d4 | #82b366 |
| 警告 | #fff2cc | #d6b656 |
| 错误 | #f8cecc | #b85450 |
| 中性 | #f5f5f5 | #666666 |

---

## XML 结构规范

### 基本结构

```xml
<mxGraphModel dx="800" dy="600" grid="1" gridSize="10" page="1" pageWidth="800" pageHeight="600">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- 所有节点和连线作为兄弟元素放在这里 -->
  </root>
</mxGraphModel>
```

### 关键规则

1. **所有 mxCell 必须是 `<root>` 的直接子元素** - 不能嵌套
2. **id="0" 和 id="1" 是保留的** - 用户内容从 id="2" 开始
3. **容器内的子元素通过 parent 属性关联** - 不是 XML 嵌套

### 节点示例

```xml
<mxCell id="2" value="Label" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

### 连线示例（带锚点）

```xml
<mxCell id="3" style="edgeStyle=orthogonalEdgeStyle;rounded=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;endArrow=classic;strokeColor=#666666;" edge="1" parent="1" source="2" target="4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 带绕行点的连线

```xml
<mxCell id="5" style="edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=1;entryX=0.5;entryY=0;endArrow=classic;" edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="200" y="300"/>
      <mxPoint x="400" y="300"/>
    </Array>
  </mxGeometry>
</mxCell>
```

---

## 生成前检查清单

1. [ ] 规划好节点位置，确保间距足够（至少 120px）
2. [ ] 识别所有需要的连线
3. [ ] 对每条连线检查：是否穿过其他节点？
4. [ ] 如果穿过，规划绕行路径
5. [ ] 显式指定每条连线的 exitX/exitY/entryX/entryY
6. [ ] 检查是否有连线共享路径
7. [ ] 所有坐标对齐到 10 的倍数
