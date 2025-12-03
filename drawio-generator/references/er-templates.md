# ER 图模板库

## 适用场景

- 数据库设计
- 实体关系建模
- 数据字典可视化
- 表结构文档

---

## 一、实体（表）样式

### 1.1 标准表格式

```xml
<!-- 使用 table shape 创建表格 -->
<mxCell id="table_user" value="User"
        style="shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;align=center;resizeLast=1;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="150" as="geometry"/>
</mxCell>

<!-- 表头行 -->
<mxCell id="row_header" value=""
        style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;top=0;left=0;right=0;bottom=1;"
        vertex="1" parent="table_user">
  <mxGeometry y="30" width="200" height="30" as="geometry"/>
</mxCell>

<!-- 列名单元格 -->
<mxCell id="cell_colname" value="Column"
        style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;fontStyle=1;overflow=hidden;whiteSpace=wrap;html=1;"
        vertex="1" parent="row_header">
  <mxGeometry width="100" height="30" as="geometry"/>
</mxCell>

<mxCell id="cell_type" value="Type"
        style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;fontStyle=1;overflow=hidden;whiteSpace=wrap;html=1;"
        vertex="1" parent="row_header">
  <mxGeometry x="100" width="100" height="30" as="geometry"/>
</mxCell>

<!-- 数据行 -->
<mxCell id="row_id" value=""
        style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;top=0;left=0;right=0;bottom=0;"
        vertex="1" parent="table_user">
  <mxGeometry y="60" width="200" height="30" as="geometry"/>
</mxCell>

<mxCell id="cell_id_name" value="🔑 id"
        style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;whiteSpace=wrap;html=1;"
        vertex="1" parent="row_id">
  <mxGeometry width="100" height="30" as="geometry"/>
</mxCell>

<mxCell id="cell_id_type" value="BIGINT"
        style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;whiteSpace=wrap;html=1;"
        vertex="1" parent="row_id">
  <mxGeometry x="100" width="100" height="30" as="geometry"/>
</mxCell>
```

### 1.2 简化实体样式

```xml
<!-- 简化版：使用普通矩形 + 多行文本 -->
<mxCell id="entity_simple" value="User&#xa;──────────&#xa;🔑 id: BIGINT&#xa;name: VARCHAR(100)&#xa;email: VARCHAR(255)&#xa;created_at: DATETIME"
        style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=5;spacingTop=5;fillColor=#dae8fc;strokeColor=#6c8ebf;fontFamily=Courier New;fontSize=11;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="180" height="130" as="geometry"/>
</mxCell>
```

### 1.3 字段标识符

| 符号 | 含义 |
|------|------|
| 🔑 或 PK | 主键 (Primary Key) |
| 🔗 或 FK | 外键 (Foreign Key) |
| * 或 NN | 非空 (Not Null) |
| U | 唯一 (Unique) |
| AI | 自增 (Auto Increment) |

---

## 二、关系连线

### 2.1 ER 关系符号

```xml
<!-- 一对一 (1:1) -->
<mxCell id="one_to_one" style="edgeStyle=orthogonalEdgeStyle;rounded=0;startArrow=ERone;startFill=0;endArrow=ERone;endFill=0;strokeWidth=2;"
        edge="1" parent="1" source="table_a" target="table_b">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 一对多 (1:N) -->
<mxCell id="one_to_many" style="edgeStyle=orthogonalEdgeStyle;rounded=0;startArrow=ERone;startFill=0;endArrow=ERmany;endFill=0;strokeWidth=2;"
        edge="1" parent="1" source="table_one" target="table_many">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 多对多 (M:N) - 通常需要关联表 -->
<mxCell id="many_to_many" style="edgeStyle=orthogonalEdgeStyle;rounded=0;startArrow=ERmany;startFill=0;endArrow=ERmany;endFill=0;strokeWidth=2;"
        edge="1" parent="1" source="table_m" target="table_n">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 零或一 (0..1) -->
<mxCell id="zero_to_one" style="edgeStyle=orthogonalEdgeStyle;rounded=0;startArrow=ERzeroToOne;startFill=0;endArrow=ERone;endFill=0;strokeWidth=2;"
        edge="1" parent="1" source="optional" target="required">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 一或多 (1..*) -->
<mxCell id="one_to_many_required" style="edgeStyle=orthogonalEdgeStyle;rounded=0;startArrow=ERone;startFill=0;endArrow=ERoneToMany;endFill=0;strokeWidth=2;"
        edge="1" parent="1" source="parent" target="children">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 零或多 (0..*) -->
<mxCell id="zero_to_many" style="edgeStyle=orthogonalEdgeStyle;rounded=0;startArrow=ERzeroToMany;startFill=0;endArrow=ERone;endFill=0;strokeWidth=2;"
        edge="1" parent="1" source="optional_many" target="one_side">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 2.2 ER 箭头对照表

| 符号名 | 含义 | 图形 |
|--------|------|------|
| ERone | 恰好一个 | \| |
| ERmany | 多个 | < |
| ERzeroToOne | 零或一个 | o\| |
| ERoneToMany | 一或多个 | \|< |
| ERzeroToMany | 零或多个 | o< |

### 2.3 关系标签

```xml
<!-- 在连线上添加关系名称 -->
<mxCell id="rel_label" value="has"
        style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;fontStyle=2;"
        vertex="1" connectable="0" parent="one_to_many">
  <mxGeometry x="0.5" relative="1" as="geometry"/>
</mxCell>
```

---

## 三、ER 图布局

### 3.1 分组布局

```xml
<!-- 模块分组 -->
<mxCell id="module_user" value="用户模块"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;verticalAlign=top;align=left;spacingLeft=10;dashed=1;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="350" height="300" as="geometry"/>
</mxCell>

<mxCell id="module_order" value="订单模块"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#4CAF50;verticalAlign=top;align=left;spacingLeft=10;dashed=1;"
        vertex="1" parent="1">
  <mxGeometry x="450" y="50" width="350" height="300" as="geometry"/>
</mxCell>
```

### 3.2 布局建议

| 场景 | 推荐布局 |
|------|----------|
| 少于 5 个表 | 水平或垂直排列 |
| 5-15 个表 | 按模块分组 |
| 大于 15 个表 | 分层 + 分组 |

**间距建议**：
- 表与表：150-200px
- 分组内边距：30px
- 分组间距：50px

---

## 四、完整示例：电商数据库

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Claude Code">
  <diagram name="电商ER图" id="ecommerce_er">
    <mxGraphModel dx="1200" dy="800" grid="1" page="1" pageWidth="1200" pageHeight="800">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- User 表 -->
        <mxCell id="user" value="User&#xa;──────────────&#xa;🔑 id: BIGINT&#xa;* username: VARCHAR(50)&#xa;* email: VARCHAR(100)&#xa;* password_hash: VARCHAR(255)&#xa;created_at: DATETIME&#xa;updated_at: DATETIME"
                style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=5;spacingTop=5;fillColor=#dae8fc;strokeColor=#6c8ebf;fontFamily=Courier New;fontSize=11;"
                vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="200" height="160" as="geometry"/>
        </mxCell>

        <!-- Order 表 -->
        <mxCell id="order" value="Order&#xa;──────────────&#xa;🔑 id: BIGINT&#xa;🔗 user_id: BIGINT&#xa;* order_no: VARCHAR(32)&#xa;* status: VARCHAR(20)&#xa;* total_amount: DECIMAL&#xa;created_at: DATETIME"
                style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=5;spacingTop=5;fillColor=#d5e8d4;strokeColor=#82b366;fontFamily=Courier New;fontSize=11;"
                vertex="1" parent="1">
          <mxGeometry x="400" y="100" width="200" height="160" as="geometry"/>
        </mxCell>

        <!-- OrderItem 表 -->
        <mxCell id="order_item" value="OrderItem&#xa;──────────────&#xa;🔑 id: BIGINT&#xa;🔗 order_id: BIGINT&#xa;🔗 product_id: BIGINT&#xa;* quantity: INT&#xa;* unit_price: DECIMAL"
                style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=5;spacingTop=5;fillColor=#d5e8d4;strokeColor=#82b366;fontFamily=Courier New;fontSize=11;"
                vertex="1" parent="1">
          <mxGeometry x="400" y="320" width="200" height="140" as="geometry"/>
        </mxCell>

        <!-- Product 表 -->
        <mxCell id="product" value="Product&#xa;──────────────&#xa;🔑 id: BIGINT&#xa;🔗 category_id: BIGINT&#xa;* name: VARCHAR(200)&#xa;* price: DECIMAL&#xa;* stock: INT&#xa;description: TEXT"
                style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=5;spacingTop=5;fillColor=#fff2cc;strokeColor=#d6b656;fontFamily=Courier New;fontSize=11;"
                vertex="1" parent="1">
          <mxGeometry x="700" y="100" width="200" height="160" as="geometry"/>
        </mxCell>

        <!-- Category 表 -->
        <mxCell id="category" value="Category&#xa;──────────────&#xa;🔑 id: BIGINT&#xa;🔗 parent_id: BIGINT&#xa;* name: VARCHAR(100)&#xa;sort_order: INT"
                style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=5;spacingTop=5;fillColor=#fff2cc;strokeColor=#d6b656;fontFamily=Courier New;fontSize=11;"
                vertex="1" parent="1">
          <mxGeometry x="700" y="320" width="200" height="120" as="geometry"/>
        </mxCell>

        <!-- 关系连线 -->
        <!-- User 1:N Order -->
        <mxCell id="rel_user_order" style="edgeStyle=orthogonalEdgeStyle;rounded=0;startArrow=ERone;startFill=0;endArrow=ERmany;endFill=0;strokeWidth=2;"
                edge="1" parent="1" source="user" target="order">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- Order 1:N OrderItem -->
        <mxCell id="rel_order_item" style="edgeStyle=orthogonalEdgeStyle;rounded=0;startArrow=ERone;startFill=0;endArrow=ERmany;endFill=0;strokeWidth=2;"
                edge="1" parent="1" source="order" target="order_item">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- Product 1:N OrderItem -->
        <mxCell id="rel_product_item" style="edgeStyle=orthogonalEdgeStyle;rounded=0;startArrow=ERone;startFill=0;endArrow=ERmany;endFill=0;strokeWidth=2;"
                edge="1" parent="1" source="product" target="order_item">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- Category 1:N Product -->
        <mxCell id="rel_category_product" style="edgeStyle=orthogonalEdgeStyle;rounded=0;startArrow=ERone;startFill=0;endArrow=ERmany;endFill=0;strokeWidth=2;"
                edge="1" parent="1" source="category" target="product">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- Category 自关联 (parent_id) -->
        <mxCell id="rel_category_self" style="edgeStyle=orthogonalEdgeStyle;rounded=1;startArrow=ERzeroToOne;startFill=0;endArrow=ERmany;endFill=0;strokeWidth=2;exitX=1;exitY=0.5;entryX=1;entryY=0.8;"
                edge="1" parent="1" source="category" target="category">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="950" y="380"/>
              <mxPoint x="950" y="420"/>
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 五、ER 图配色方案

| 模块类型 | fillColor | strokeColor |
|----------|-----------|-------------|
| 用户相关 | #dae8fc | #6c8ebf |
| 订单相关 | #d5e8d4 | #82b366 |
| 商品相关 | #fff2cc | #d6b656 |
| 支付相关 | #f8cecc | #b85450 |
| 系统配置 | #e1d5e7 | #9673a6 |
| 日志审计 | #f5f5f5 | #666666 |
