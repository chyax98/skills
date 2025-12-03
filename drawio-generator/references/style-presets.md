# 样式预设库

## 适用场景

- 需要特定配色方案
- 需要高级样式效果（渐变、阴影、玻璃效果）
- 需要品牌一致性
- 需要特殊视觉效果

---

## 一、配色方案

### 1.1 Material Design 配色

| 颜色名 | 主色 (fill) | 深色 (stroke) | 浅色 (bg) |
|--------|-------------|---------------|-----------|
| Red | #F44336 | #C62828 | #FFCDD2 |
| Pink | #E91E63 | #AD1457 | #F8BBD9 |
| Purple | #9C27B0 | #6A1B9A | #E1BEE7 |
| Deep Purple | #673AB7 | #4527A0 | #D1C4E9 |
| Indigo | #3F51B5 | #283593 | #C5CAE9 |
| Blue | #2196F3 | #1565C0 | #BBDEFB |
| Light Blue | #03A9F4 | #0277BD | #B3E5FC |
| Cyan | #00BCD4 | #00838F | #B2EBF2 |
| Teal | #009688 | #00695C | #B2DFDB |
| Green | #4CAF50 | #2E7D32 | #C8E6C9 |
| Light Green | #8BC34A | #558B2F | #DCEDC8 |
| Lime | #CDDC39 | #9E9D24 | #F0F4C3 |
| Yellow | #FFEB3B | #F9A825 | #FFF9C4 |
| Amber | #FFC107 | #FF8F00 | #FFECB3 |
| Orange | #FF9800 | #EF6C00 | #FFE0B2 |
| Deep Orange | #FF5722 | #D84315 | #FFCCBC |
| Brown | #795548 | #4E342E | #D7CCC8 |
| Grey | #9E9E9E | #616161 | #F5F5F5 |
| Blue Grey | #607D8B | #37474F | #CFD8DC |

### 1.2 语义化配色

```xml
<!-- 成功/正向 -->
<mxCell style="fillColor=#C8E6C9;strokeColor=#4CAF50;fontColor=#1B5E20;" .../>

<!-- 警告/注意 -->
<mxCell style="fillColor=#FFF9C4;strokeColor=#FBC02D;fontColor=#F57F17;" .../>

<!-- 错误/危险 -->
<mxCell style="fillColor=#FFCDD2;strokeColor=#F44336;fontColor=#B71C1C;" .../>

<!-- 信息/中性 -->
<mxCell style="fillColor=#BBDEFB;strokeColor=#2196F3;fontColor=#0D47A1;" .../>

<!-- 禁用/灰色 -->
<mxCell style="fillColor=#EEEEEE;strokeColor=#9E9E9E;fontColor=#616161;" .../>
```

### 1.3 暗色主题配色

| 元素 | fillColor | strokeColor | fontColor |
|------|-----------|-------------|-----------|
| 背景 | #1E1E1E | #333333 | #FFFFFF |
| 卡片 | #2D2D2D | #404040 | #E0E0E0 |
| 主要 | #BB86FC | #9A67EA | #FFFFFF |
| 次要 | #03DAC6 | #00C4B4 | #000000 |
| 错误 | #CF6679 | #B00020 | #FFFFFF |

---

## 二、渐变效果

### 2.1 线性渐变

```xml
<!-- 垂直渐变（上深下浅） -->
<mxCell style="fillColor=#2196F3;gradientColor=#64B5F6;gradientDirection=south;" .../>

<!-- 垂直渐变（下深上浅） -->
<mxCell style="fillColor=#64B5F6;gradientColor=#2196F3;gradientDirection=north;" .../>

<!-- 水平渐变（左深右浅） -->
<mxCell style="fillColor=#2196F3;gradientColor=#64B5F6;gradientDirection=east;" .../>

<!-- 水平渐变（右深左浅） -->
<mxCell style="fillColor=#64B5F6;gradientColor=#2196F3;gradientDirection=west;" .../>
```

### 2.2 预设渐变组合

```xml
<!-- 蓝色按钮 -->
<mxCell style="rounded=1;fillColor=#2196F3;gradientColor=#1976D2;gradientDirection=south;strokeColor=#1565C0;fontColor=#ffffff;shadow=1;" .../>

<!-- 绿色按钮 -->
<mxCell style="rounded=1;fillColor=#4CAF50;gradientColor=#388E3C;gradientDirection=south;strokeColor=#2E7D32;fontColor=#ffffff;shadow=1;" .../>

<!-- 橙色按钮 -->
<mxCell style="rounded=1;fillColor=#FF9800;gradientColor=#F57C00;gradientDirection=south;strokeColor=#EF6C00;fontColor=#ffffff;shadow=1;" .../>

<!-- 红色按钮 -->
<mxCell style="rounded=1;fillColor=#F44336;gradientColor=#D32F2F;gradientDirection=south;strokeColor=#C62828;fontColor=#ffffff;shadow=1;" .../>

<!-- 紫色按钮 -->
<mxCell style="rounded=1;fillColor=#9C27B0;gradientColor=#7B1FA2;gradientDirection=south;strokeColor=#6A1B9A;fontColor=#ffffff;shadow=1;" .../>
```

---

## 三、阴影效果

### 3.1 基础阴影

```xml
<!-- 标准阴影 -->
<mxCell style="shadow=1;" .../>

<!-- 自定义阴影 -->
<mxCell style="shadow=1;shadowColor=#000000;shadowOpacity=0.25;shadowOffsetX=3;shadowOffsetY=3;" .../>
```

### 3.2 阴影强度预设

```xml
<!-- 轻微阴影 -->
<mxCell style="shadow=1;shadowColor=#000000;shadowOpacity=0.1;shadowOffsetX=1;shadowOffsetY=1;shadowBlur=2;" .../>

<!-- 中等阴影 -->
<mxCell style="shadow=1;shadowColor=#000000;shadowOpacity=0.2;shadowOffsetX=2;shadowOffsetY=2;shadowBlur=4;" .../>

<!-- 强烈阴影 -->
<mxCell style="shadow=1;shadowColor=#000000;shadowOpacity=0.3;shadowOffsetX=4;shadowOffsetY=4;shadowBlur=8;" .../>

<!-- 柔和大阴影 -->
<mxCell style="shadow=1;shadowColor=#000000;shadowOpacity=0.15;shadowOffsetX=0;shadowOffsetY=8;shadowBlur=16;" .../>
```

---

## 四、玻璃效果

### 4.1 玻璃卡片

```xml
<!-- 蓝色玻璃 -->
<mxCell style="rounded=1;fillColor=#E3F2FD;gradientColor=#BBDEFB;glass=1;strokeColor=#1976D2;shadow=1;" .../>

<!-- 绿色玻璃 -->
<mxCell style="rounded=1;fillColor=#E8F5E9;gradientColor=#C8E6C9;glass=1;strokeColor=#4CAF50;shadow=1;" .../>

<!-- 紫色玻璃 -->
<mxCell style="rounded=1;fillColor=#F3E5F5;gradientColor=#E1BEE7;glass=1;strokeColor=#9C27B0;shadow=1;" .../>
```

### 4.2 毛玻璃效果（模拟）

```xml
<mxCell style="rounded=1;fillColor=#ffffff;opacity=80;strokeColor=#E0E0E0;strokeWidth=1;shadow=1;shadowBlur=10;" .../>
```

---

## 五、边框样式

### 5.1 边框粗细

```xml
<!-- 细边框 -->
<mxCell style="strokeWidth=1;" .../>

<!-- 普通边框 -->
<mxCell style="strokeWidth=2;" .../>

<!-- 粗边框 -->
<mxCell style="strokeWidth=3;" .../>

<!-- 超粗边框 -->
<mxCell style="strokeWidth=4;" .../>
```

### 5.2 虚线样式

```xml
<!-- 短虚线 -->
<mxCell style="dashed=1;dashPattern=4 4;" .../>

<!-- 长虚线 -->
<mxCell style="dashed=1;dashPattern=8 8;" .../>

<!-- 点线 -->
<mxCell style="dashed=1;dashPattern=1 4;" .../>

<!-- 点划线 -->
<mxCell style="dashed=1;dashPattern=8 4 2 4;" .../>

<!-- 双点划线 -->
<mxCell style="dashed=1;dashPattern=8 4 2 4 2 4;" .../>
```

### 5.3 圆角大小

```xml
<!-- 小圆角 -->
<mxCell style="rounded=1;arcSize=10;" .../>

<!-- 中等圆角 -->
<mxCell style="rounded=1;arcSize=20;" .../>

<!-- 大圆角 -->
<mxCell style="rounded=1;arcSize=40;" .../>

<!-- 胶囊形状（最大圆角） -->
<mxCell style="rounded=1;arcSize=50;" .../>
```

---

## 六、文字样式

### 6.1 字体大小

| 用途 | fontSize |
|------|----------|
| 标题 | 18-24 |
| 副标题 | 14-16 |
| 正文 | 12 |
| 注释 | 10 |
| 小字 | 8 |

### 6.2 字体样式

```xml
<!-- 粗体 -->
<mxCell style="fontStyle=1;" .../>

<!-- 斜体 -->
<mxCell style="fontStyle=2;" .../>

<!-- 粗斜体 -->
<mxCell style="fontStyle=3;" .../>

<!-- 下划线 -->
<mxCell style="fontStyle=4;" .../>

<!-- 粗体+下划线 -->
<mxCell style="fontStyle=5;" .../>
```

### 6.3 文字对齐

```xml
<!-- 水平对齐 -->
<mxCell style="align=left;" .../>
<mxCell style="align=center;" .../>
<mxCell style="align=right;" .../>

<!-- 垂直对齐 -->
<mxCell style="verticalAlign=top;" .../>
<mxCell style="verticalAlign=middle;" .../>
<mxCell style="verticalAlign=bottom;" .../>

<!-- 组合 -->
<mxCell style="align=left;verticalAlign=top;spacingLeft=10;spacingTop=5;" .../>
```

---

## 七、特殊效果

### 7.1 手绘风格 (Sketch)

```xml
<!-- 粗糙手绘 -->
<mxCell style="sketch=1;sketchStyle=rough;" .../>

<!-- 卡通风格 -->
<mxCell style="sketch=1;sketchStyle=comic;" .../>
```

### 7.2 3D 效果

```xml
<!-- 立方体 -->
<mxCell style="shape=cube;size=10;fillColor=#dae8fc;strokeColor=#6c8ebf;" .../>

<!-- 圆柱体 -->
<mxCell style="shape=cylinder3;size=10;fillColor=#dae8fc;strokeColor=#6c8ebf;" .../>
```

### 7.3 透明度

```xml
<!-- 整体透明 -->
<mxCell style="opacity=50;" .../>

<!-- 仅填充透明 -->
<mxCell style="fillOpacity=50;" .../>

<!-- 仅边框透明 -->
<mxCell style="strokeOpacity=50;" .../>
```

---

## 八、连线样式预设

### 8.1 标准连线

```xml
<!-- 实线箭头 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;strokeWidth=2;" .../>

<!-- 虚线箭头 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;dashed=1;strokeWidth=1;" .../>

<!-- 无箭头 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=none;strokeWidth=2;" .../>

<!-- 双向箭头 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;startArrow=classic;endArrow=classic;strokeWidth=2;" .../>
```

### 8.2 曲线连线

```xml
<!-- 圆角折线 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=classic;strokeWidth=2;" .../>

<!-- 平滑曲线 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;curved=1;endArrow=classic;strokeWidth=2;" .../>
```

### 8.3 连线跳过

```xml
<!-- 弧形跳过 -->
<mxCell style="jumpStyle=arc;" .../>

<!-- 间隙跳过 -->
<mxCell style="jumpStyle=gap;" .../>

<!-- 尖角跳过 -->
<mxCell style="jumpStyle=sharp;" .../>
```

---

## 九、组合样式模板

### 9.1 卡片样式

```xml
<!-- 标准卡片 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#E0E0E0;shadow=1;"

<!-- 悬浮卡片 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#E0E0E0;shadow=1;shadowOffsetX=0;shadowOffsetY=4;shadowBlur=8;shadowOpacity=0.15;"

<!-- 边框卡片 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#1976D2;strokeWidth=2;"
```

### 9.2 按钮样式

```xml
<!-- 主要按钮 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1976D2;gradientColor=#1565C0;strokeColor=#0D47A1;fontColor=#ffffff;fontStyle=1;shadow=1;"

<!-- 次要按钮 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#1976D2;strokeWidth=2;fontColor=#1976D2;"

<!-- 危险按钮 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F44336;gradientColor=#D32F2F;strokeColor=#B71C1C;fontColor=#ffffff;fontStyle=1;shadow=1;"
```

### 9.3 标签样式

```xml
<!-- 成功标签 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#4CAF50;fontColor=#1B5E20;fontSize=10;arcSize=50;"

<!-- 警告标签 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF9C4;strokeColor=#FBC02D;fontColor=#F57F17;fontSize=10;arcSize=50;"

<!-- 错误标签 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFCDD2;strokeColor=#F44336;fontColor=#B71C1C;fontSize=10;arcSize=50;"
```

---

## 十、品牌配色参考

### 10.1 科技公司

| 品牌 | 主色 | 辅色 |
|------|------|------|
| Google Blue | #4285F4 | #1967D2 |
| Google Red | #EA4335 | #C5221F |
| Google Yellow | #FBBC04 | #F9AB00 |
| Google Green | #34A853 | #188038 |
| Microsoft | #00A4EF | #0078D4 |
| Amazon | #FF9900 | #146EB4 |
| Apple | #000000 | #555555 |
| Meta | #1877F2 | #0866FF |

### 10.2 云服务商

| 服务商 | 主色 | 描述 |
|--------|------|------|
| AWS Orange | #FF9900 | AWS 标志色 |
| AWS Dark | #232F3E | AWS 深色 |
| Azure Blue | #0078D4 | Azure 主色 |
| GCP Blue | #4285F4 | GCP 主色 |
| Alibaba Orange | #FF6A00 | 阿里云主色 |
