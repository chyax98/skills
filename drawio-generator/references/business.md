# 业务流程素材库

金融、电商、HR、供应链等行业流程图元素和模板。

## 通用业务元素

### 角色/参与者

```xml
<!-- 用户/客户 -->
<mxCell value="👤 Customer"
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="40" y="100" width="40" height="80" as="geometry"/>
</mxCell>

<!-- 管理员/操作员 -->
<mxCell value="👨‍💼 Admin"
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
        vertex="1" .../>

<!-- 系统/自动化 -->
<mxCell value="🤖 System"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
        vertex="1" .../>
```

### 文档类型

```xml
<!-- 表单/申请 -->
<mxCell value="📝 Application Form"
        style="shape=document;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" .../>

<!-- 合同/协议 -->
<mxCell value="📄 Contract"
        style="shape=note;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;"
        vertex="1" .../>

<!-- 报告/审批单 -->
<mxCell value="📊 Report"
        style="shape=card;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;"
        vertex="1" .../>

<!-- 发票/收据 -->
<mxCell value="🧾 Invoice"
        style="shape=document;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" .../>
```

### 审批状态

```xml
<!-- 待审批 -->
<mxCell value="⏳ Pending"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF9C4;strokeColor=#F9A825;fontColor=#333333;"
        vertex="1" .../>

<!-- 已批准 -->
<mxCell value="✅ Approved"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#2E7D32;fontColor=#333333;"
        vertex="1" .../>

<!-- 已拒绝 -->
<mxCell value="❌ Rejected"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFCDD2;strokeColor=#C62828;fontColor=#333333;"
        vertex="1" .../>

<!-- 需补充材料 -->
<mxCell value="📎 More Info"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#BBDEFB;strokeColor=#1976D2;fontColor=#333333;"
        vertex="1" .../>
```

---

## 金融行业

### 支付流程

```xml
<!-- 银行/金融机构 -->
<mxCell value="🏦 Bank"
        style="shape=cube;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#1565C0;strokeColor=#0D47A1;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 支付网关 -->
<mxCell value="💳 Payment Gateway"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#7B1FA2;strokeColor=#4A148C;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 钱包 -->
<mxCell value="👛 Wallet"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#00897B;strokeColor=#004D40;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 交易 -->
<mxCell value="💰 Transaction"
        style="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fillColor=#FFC107;strokeColor=#FFA000;"
        vertex="1" .../>
```

### 贷款审批流程模板

```
[申请] → [资料审核] → [信用评估] → [风控审批] → [放款]
                                        ↓
                                   [拒绝通知]
```

| 节点 | 颜色 | 说明 |
|------|------|------|
| 申请 | #BBDEFB | 客户发起 |
| 资料审核 | #FFF9C4 | 人工审核 |
| 信用评估 | #E1BEE7 | 自动评分 |
| 风控审批 | #FFCCBC | 风险决策 |
| 放款 | #C8E6C9 | 资金发放 |
| 拒绝 | #FFCDD2 | 申请被拒 |

### 风控元素

```xml
<!-- 风险等级 - 高 -->
<mxCell value="🔴 High Risk"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F44336;strokeColor=#C62828;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 风险等级 - 中 -->
<mxCell value="🟡 Medium Risk"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF9800;strokeColor=#E65100;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 风险等级 - 低 -->
<mxCell value="🟢 Low Risk"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=#2E7D32;fontColor=#FFFFFF;"
        vertex="1" .../>
```

---

## 电商行业

### 订单流程

```xml
<!-- 购物车 -->
<mxCell value="🛒 Cart"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF9800;strokeColor=#E65100;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 订单 -->
<mxCell value="📦 Order"
        style="shape=document;whiteSpace=wrap;html=1;fillColor=#42A5F5;strokeColor=#1E88E5;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 库存 -->
<mxCell value="📋 Inventory"
        style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#78909C;strokeColor=#546E7A;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 物流 -->
<mxCell value="🚚 Shipping"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#26A69A;strokeColor=#00897B;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 退货/退款 -->
<mxCell value="↩️ Return"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EF5350;strokeColor=#C62828;fontColor=#FFFFFF;"
        vertex="1" .../>
```

### 订单状态流

```
[下单] → [待支付] → [已支付] → [备货中] → [已发货] → [已签收]
    ↓         ↓                              ↓
 [取消]    [超时关闭]                     [退货申请]
```

| 状态 | 颜色代码 | 说明 |
|------|----------|------|
| 待支付 | #FFF9C4 | 等待付款 |
| 已支付 | #BBDEFB | 付款成功 |
| 备货中 | #E1BEE7 | 仓库拣货 |
| 已发货 | #B2DFDB | 物流运输 |
| 已签收 | #C8E6C9 | 完成交付 |
| 取消/关闭 | #ECEFF1 | 订单终止 |
| 退货 | #FFCDD2 | 售后处理 |

### 电商平台架构

```xml
<!-- 前台/App -->
<mxCell value="📱 App / Web"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#42A5F5;strokeColor=#1E88E5;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 商品服务 -->
<mxCell value="🏷️ Product Service"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#66BB6A;strokeColor=#43A047;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 订单服务 -->
<mxCell value="📝 Order Service"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFA726;strokeColor=#FB8C00;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 支付服务 -->
<mxCell value="💳 Payment Service"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#AB47BC;strokeColor=#8E24AA;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 搜索服务 -->
<mxCell value="🔍 Search Service"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#29B6F6;strokeColor=#039BE5;fontColor=#FFFFFF;"
        vertex="1" .../>
```

---

## HR/人事

### 招聘流程

```xml
<!-- 职位发布 -->
<mxCell value="📢 Job Posting"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#42A5F5;strokeColor=#1E88E5;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 简历筛选 -->
<mxCell value="📄 Resume Screening"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFA726;strokeColor=#FB8C00;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 面试 -->
<mxCell value="🎤 Interview"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#AB47BC;strokeColor=#8E24AA;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- Offer -->
<mxCell value="🎉 Offer"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#66BB6A;strokeColor=#43A047;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 入职 -->
<mxCell value="🚀 Onboarding"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#26A69A;strokeColor=#00897B;fontColor=#FFFFFF;"
        vertex="1" .../>
```

### 组织架构

```xml
<!-- 部门 -->
<mxCell value="🏢 Department"
        style="swimlane;horizontal=1;startSize=30;fillColor=#E3F2FD;strokeColor=#1976D2;"
        vertex="1" .../>

<!-- 团队 -->
<mxCell value="👥 Team"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#BBDEFB;strokeColor=#1976D2;"
        vertex="1" .../>

<!-- 员工 -->
<mxCell value="👤 Employee"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;"
        vertex="1" .../>
```

### 请假审批

```
[员工申请] → [直属主管] → [HR审核] → [通过/拒绝]
                 ↓
            [驳回修改]
```

---

## 供应链/物流

### 供应链节点

```xml
<!-- 供应商 -->
<mxCell value="🏭 Supplier"
        style="shape=cube;whiteSpace=wrap;html=1;fillColor=#78909C;strokeColor=#546E7A;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 仓库 -->
<mxCell value="🏪 Warehouse"
        style="shape=cube;whiteSpace=wrap;html=1;fillColor=#8D6E63;strokeColor=#5D4037;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 配送中心 -->
<mxCell value="📦 Distribution Center"
        style="shape=cube;whiteSpace=wrap;html=1;fillColor=#FFB74D;strokeColor=#F57C00;fontColor=#333333;"
        vertex="1" .../>

<!-- 零售店 -->
<mxCell value="🏬 Retail Store"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#81C784;strokeColor=#43A047;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 最终客户 -->
<mxCell value="👤 End Customer"
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
        vertex="1" .../>
```

### 物流追踪状态

| 状态 | 图标 | 颜色 |
|------|------|------|
| 已下单 | 📝 | #BBDEFB |
| 待发货 | 📦 | #FFF9C4 |
| 运输中 | 🚚 | #B2EBF2 |
| 派送中 | 🏃 | #DCEDC8 |
| 已签收 | ✅ | #C8E6C9 |
| 异常 | ⚠️ | #FFCDD2 |

---

## 审批流程通用模板

### 多级审批

```xml
<!-- 审批节点样式 -->
<!-- 一级审批 -->
<mxCell value="L1 Approval"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFF9C4;strokeColor=#F9A825;"
        vertex="1" .../>

<!-- 二级审批 -->
<mxCell value="L2 Approval"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFECB3;strokeColor=#FF8F00;"
        vertex="1" .../>

<!-- 终审 -->
<mxCell value="Final Approval"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFE0B2;strokeColor=#E65100;"
        vertex="1" .../>
```

### 会签/或签

```xml
<!-- 会签（全部通过） -->
<mxCell value="AND"
        style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#CE93D8;strokeColor=#8E24AA;fontColor=#FFFFFF;fontStyle=1;"
        vertex="1" .../>

<!-- 或签（任一通过） -->
<mxCell value="OR"
        style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#90CAF9;strokeColor=#1976D2;fontColor=#FFFFFF;fontStyle=1;"
        vertex="1" .../>
```

---

## 行业配色方案

### 金融

```
主色: #1565C0 (信任蓝)
成功: #2E7D32 (交易成功)
警告: #F57C00 (风险提示)
错误: #C62828 (交易失败)
金色: #FFC107 (VIP/高端)
```

### 电商

```
主色: #FF5722 (活力橙)
购买: #4CAF50 (立即购买)
促销: #E91E63 (促销粉)
价格: #F44336 (价格红)
中性: #607D8B (辅助灰)
```

### 医疗

```
主色: #00BCD4 (清新青)
紧急: #F44336 (急诊红)
安全: #4CAF50 (健康绿)
警示: #FF9800 (警示橙)
专业: #3F51B5 (专业蓝)
```

### 政务

```
主色: #C62828 (政务红)
辅助: #1565C0 (公信蓝)
通过: #2E7D32 (办结绿)
等待: #F57C00 (处理中橙)
中性: #455A64 (稳重灰)
```
