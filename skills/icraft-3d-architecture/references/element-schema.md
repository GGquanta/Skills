# iCraft 场景元素 JSON

编辑器「JSON 导入与导出」读写的是 **元素数组**，与运行时 `getAllSceneElementsData()` 一致。不是 `.icraft` 工程文件。

## 元素种类

| `type` | 作用 |
|---|---|
| `directionallight` | 平行光；保留一盏 `defaultLight: true` 即可 |
| `area` | 分区台面（圆角薄板） |
| `text` | 地面标签或区标题 |
| `model` | 3D 资产，`options.type` 为 GLB 路径 |
| `line` | 连线，`points` 为扁平坐标 |

每项形如 `{ "key": "...", "type": "...", "options": { ..., "key": "<同外层 key>" } }`。`options.key` 必须与外层 `key` 相同。

## 坐标与高度

- 俯视平面：`x` 左右，`z` 前后。`y` 向上。
- 台面：`y = 0`，`height ≈ 0.19`。
- 连线：全部顶点 `y = 0.22`。
- 文字：`y = 0.21`。
- 模型 `y` 因 GLB 包围盒而异，修订时优先沿用同类模型的高度；换模型后若陷入台面或悬浮过大，按同类参考值微调。

## `area`

必要字段：`name`, `width`, `length`, `height`, `x`, `y`, `z`, `color`, `borderColor`, `showBorder`, `materialType: "clay"`, `opacity`（台面常用 `0.7`）, `radius`（常用 `0.3`）。

`x,z` 是台面中心。标题文字放在左上角外侧，不要放在模型正上方。

## `text`

| 用途 | `textAlign` | `anchorX` | `anchorY` | 位置 |
|---|---|---|---|---|
| 分区标题 | `left` | `left` | `top` | 台面左上角外 |
| 设备标签 | `center` | `center` | `middle` | `(模型x, 0.21, 模型z + 0.62)` |

常用：`font: "AlibabaPuHuiTi"`, `weight: "Bold"`, `fontSize` 区标题 `0.26`、设备 `0.22`，`outlineWidth: 0.02`，`outlineColor: "#ffffff"`。`maxWidth` 按字数大约 `0.12 * 字符数`，下限约 `0.5`。

地面文字与悬浮标签（`model.tipShow`）可同时存在；评审要求设备开启 `tipShow`。

## `model`

```json
{
  "name": "Firewall",
  "type": "model/v1/firewall1/scene.glb",
  "x": -2, "y": 0.487, "z": -2.5,
  "scale": 1,
  "tipShow": true,
  "materialType": "base",
  "color": ["#ffffff", "#222222"],
  "linkLineKeys": ["line-key-1", "line-key-2"],
  "rotateX": 0, "rotateY": 0, "rotateZ": 0
}
```

- `type` 必须是图库真实路径。未命中则显示问号立方体。
- `color` 是材质槽颜色数组，长度随 GLB 变化；换路径时整组替换。
- `linkLineKeys` 列出所有以该模型为端点的线。增删线时两端都要改。

## `line`

```json
{
  "showArrow": true,
  "arrowSize": 0.8,
  "arrowPositionPercent": 0.72,
  "doubleArrow": false,
  "dashed": false,
  "linewidth": 0.05,
  "routingMode": "normal",
  "points": [-1.5, 0.22, -2.5, 6.0, 0.22, -2.5],
  "startElementKey": "fw-key",
  "endElementKey": "gw-key",
  "x": 2.25, "y": 0.22, "z": -2.5
}
```

- `points`：`[x0,y0,z0, x1,y1,z1, ...]`，相邻两点只变 `x` 或只变 `z`（直角）。
- `x,y,z`：各顶点算术平均，仅作元素锚点。
- 箭头表示流量方向（访问 / 入云）。VPN / 专线：`dashed: true`。
- 不要默认抄用户导出的 `doubleArrow: true`。

## `directionallight`

保留用户导出的平行光即可。参考值：`intensity: 3.5`，`y: 16`，`shadowResolution: "high"`，`shadowSize: 48`，`defaultLight: true`。

## 修订已有导出

1. 建立 `原 key → 角色` 映射，生成时写回同一 `key`。
2. 语义变化的边（例如 PC–Laptop 改为 Switch–Laptop）**复用旧线 key**，但重写 `points`、起终点与 `linkLineKeys`。
3. 不要删除灯光除非用户要求。

## 校验

生成后用脚本检查：

- 所有 `key` 唯一。
- 每个 `linkLineKeys[i]` 对应一条 `type==line`。
- 每条 line 的 `startElementKey` / `endElementKey` 对应 `type==model`。
- 互引闭合：若 A 列出线 L，则 L 的端点之一为 A。
