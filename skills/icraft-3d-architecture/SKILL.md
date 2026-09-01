---
name: icraft-3d-architecture
description: >-
  用 iCraft Editor 绘制、修订企业级 3D 架构图。默认以场景元素 JSON
  （getAllSceneElementsData 数组）为交付主路径，用 Python 生成直角走线、
  分区着色与已验证模型路径；Mermaid architecture-beta 仅作起稿。当用户提到
  iCraft、icraft.gantcloud.com、3D 架构图、混合云拓扑、场景 JSON 导入导出、
  .icraft、或要把网络/云架构画成 3D 时使用。
---

# iCraft 3D 架构图

面向 Agent 的操作规程。目标是可导入、可迭代、外观可区分的场景 JSON，而不是手改加密工程文件。

## 何时使用

- 用户要画或改 **iCraft** 3D 架构图（网络、混合云、机房、云产品拓扑）。
- 用户贴出编辑器导出的 **元素 JSON**，要求改布局、换模型、改连线。
- 用户给参考截图 / 官方模板，要求对齐画风。

不要用本技能去手改 `.icraft` 文件，也不要把 JSON 改扩展名当工程文件打开。

## 交付原则（按优先级）

1. **JSON 是唯一可靠交付物**：编辑器汉堡菜单 →「JSON 导入与导出」。数组形态与 `getAllSceneElementsData()` 一致。
2. **Mermaid 只起稿**：`https://icraft.gantcloud.com/app/editor?defaultOpen=mermaid`。布局、模型、走线最终必须落到 JSON。
3. **`.icraft` 不可作为输入或输出**：官方模板是 AES 加密 ZIP，不能当明文 JSON 编辑，也不能把元素数组改扩展名打开。
4. **用脚本生成 JSON**，禁止在对话里手改上千行坐标。修订已有图时 **保留原 `key`**，便于对照导入。
5. 语雀手册（`gant.yuque.com/fdt/qgzed0`）经常抓取失败；以本技能、官方模板观感、用户导出 JSON 为准。

参考链接：

- 编辑器：<https://icraft.gantcloud.com/app/editor>
- 仓库：<https://github.com/gantFDT/icraft>
- 官方网络模板：`templates/NetworkArchitecture.icraft`（只能在编辑器中打开，用于对照画风）

JSON 字段细节见 [references/element-schema.md](references/element-schema.md)。已验证模型路径见 [references/model-catalog.md](references/model-catalog.md)。

---

## 标准工作流

复制并跟踪：

```
- [ ] 1. 拓扑清单：分区 / 节点 / 边 / 流量方向
- [ ] 2. 模型选型：每个角色外观可区分，路径来自 model-catalog
- [ ] 3. 网格布局：分区着色，坐标取整或 0.25 网格
- [ ] 4. Python 生成 JSON（保留 key；直角折线；linkLineKeys 闭合）
- [ ] 5. 评审清单全部通过
- [ ] 6. 告知用户：清空画布 → JSON 导入 → R 复位相机
```

### 1. 先写拓扑，再写坐标

向用户确认或自行从需求抽出四张表，缺一就补问：

| 表 | 内容 |
|---|---|
| 分区 | 名称、范围（Internet / 本地 DC / 公有云 / 分支等） |
| 节点 | 角色、落在哪一区、标签文案（地面文字可与 `name` 不同） |
| 边 | 谁连谁、单向还是双向、实线还是虚线（专线 / VPN 用虚线） |
| 禁连 | 明确不要画的边（例如终端互连、云资源糖葫芦串联） |

混合云默认拓扑（可按需求裁剪）：

```
Internet → Router → Firewall → CoreSwitch
                              ├─ WebServer
                              ├─ AppServer → Database
                              ├─ PC（分支，各自上联）
                              └─ Laptop（分支，各自上联）
Firewall ─虚线─ VPN Gateway ─┬─ K8s
                             ├─ CloudDB
                             └─ OSS
```

### 2. 模型选型硬规则

- **同一外形不得承担两个语义角色**。`model/v1/network/scene.glb` 是地球仪，只给 Internet；混合网关 / VPN 必须用路由器或网关模型，换橙色材质与标签「VPN Gateway」。
- **防火墙**用 `firewall1`（立方体 + 盾），不要用砖墙 `firewall`。
- **本地库 vs 云库**：本地用 `database-server`（机架），云用 `database`（圆柱）；标签分别是 Database / CloudDB，禁止把本地库写成 CloudDB。
- **K8s vs OSS**：计算用 `application-server`（或库内 Kubernetes 图标），对象存储必须用 `storage`。未命中图库的 icon 会变成带问号的立方体。
- 终端（PC / Laptop）`scale` 用 `0.7`；打开模型 `tipShow: true`。
- `color` 数组长度必须匹配该 GLB 的材质槽；改模型时从 catalog 拷贝整组颜色，不要沿用旧模型的数组。

### 3. 布局与画风

坐标约定：`x` 左右，`z` 前后（俯视），`y` 高度。连线高度固定 `y = 0.22`，地面文字 `y = 0.21`，台面 `y = 0`。

| 分区 | 台面色 | 边框色 | 用途 |
|---|---|---|---|
| Internet / On-Prem | `#d6dfff` | `#8f97b3` | 入口与本地 |
| Public Cloud | `#ffe4cc` | `#c4925a` | 云区一眼可辨 |
| Branch | `#e4f0e6` | `#7d9a82` | 终端区 |

- 核心链路沿同一 `x` 或同一 `z` 对齐（例如 Router / Firewall / CoreSwitch 共线）。
- 云区资源从网关 **并联**，不要 K8s → DB → OSS 串联。
- 分支终端不要互连；各从上联交换机引出，走线在中途分叉，避免看起来像经另一台终端中转。
- 区标题：`textAlign: left`，`anchorX: left`，`anchorY: top`，放在台面左上角外侧。
- 设备标签：`textAlign: center`，`anchorX/Y: center/middle`，位置约 `(模型x, 0.21, 模型z + 0.62)`。
- 字体用 `AlibabaPuHuiTi`，`weight: Bold`。

### 4. 用 Python 生成，不要手改

先 Read `scripts/icraft_scene.py`，把 `area` / `model` / `line` / `default_light` / `dumps` 拷进本次生成脚本（或把该目录加入 `sys.path`）。要求：

- 输出 **元素数组**（可含一盏 `directionallight`）。
- 修订用户导出时，`key` 映射表照抄原文；新增元素再生成新 key。
- `line.points` 为扁平 `[x,y,z, x,y,z, ...]`，只做轴对齐折线（每次只改 x 或只改 z）。
- `line.options.x/y/z` 取各顶点均值。
- 每条线写 `startElementKey` / `endElementKey`；两端模型的 `linkLineKeys` 必须包含该线。
- 入云 / 访问方向：`showArrow: true`，`doubleArrow: false`。专线 / VPN：`dashed: true`。
- 生成后立刻校验：JSON 可解析；每个 `linkLineKeys` 都能找到对应 `line`；每条 `line` 的起终点都存在。

### 5. 导入与验收

告诉用户：

1. 打开编辑器，必要时「创建新绘图」或清空画布。
2. 汉堡菜单 → JSON 导入，选生成的文件。
3. 快捷键：`V` 俯视核对走线，`C` 透视看立体，`R` 复位相机，`G` 网格吸附。
4. 图库单击即可落盘；不要拖拽到画布外。

若用浏览器代为验证：导入后截俯视图，对照下方评审清单；不要用 Chrome DevTools 的 `fill` 往 Monaco 里灌 Mermaid（见陷阱）。

---

## 评审清单（必须全过）

完整条目与反例见 [references/review-checklist.md](references/review-checklist.md)。生成后自检：

- [ ] 网关不是地球仪；Internet 才是地球仪
- [ ] 本地库与云库外形不同，标签不混用
- [ ] K8s 与 OSS 外形不同
- [ ] 无终端互连；终端各自上联汇聚设备
- [ ] 出云从防火墙到混合网关，云资源并联
- [ ] 直角走线，不斜穿模型
- [ ] 分区颜色可区分；终端缩小；设备悬浮标签开启
- [ ] 未使用图库里不存在的模型路径

---

## 已知陷阱（Agent 高频翻车）

**文件与导入**

- `.icraft` ≠ JSON。改扩展名会打不开。
- JSON 导入覆盖当前场景；提醒用户先导出备份或在空画布导入。

**Mermaid `architecture-beta`（仅起稿）**

- 组名、服务 id、括号内图标名 **不能有空格**。`On-Prem DC`、`Web Server` 会解析失败；写成 `OnPremDC`、`WebServer`。
- `service id(IconName)[Label] in groupId`：`IconName` 必须能映射到图库，否则变成带 `?` 的立方体。
- 不要假设 `Gateway` / `Cloud` 会得到网关或 Kubernetes；实测 `HybridGW` 会映射成与 Internet 相同的地球仪。
- 浏览器自动化：对 Monaco 使用 `fill` 会 **逐行递增缩进**，代码损坏。应取出 webpack 中的 `monaco.editor.getEditors()[0].setValue(code)` 一次性写入。

**连线语义**

- 用户导出里常见 `doubleArrow: true` 且无方向；交付版改为有方向的单箭头，专线用虚线。
- 复用旧 `line` 的 `key` 时，必须同步改 `startElementKey` / `endElementKey` / 两端 `linkLineKeys`，否则编辑器里线还连着旧节点。
- 折线第一个/最后一个顶点应落在元件边缘附近（约半个模型宽度），中间顶点用于绕行，避免穿过机柜。

**浏览器操作**

- 首次打开会有更新日志 /「创建新绘图」弹窗，先关掉再操作。
- 无障碍 snapshot 点不准时，用 `evaluate_script` 按按钮文案 `click()`。
- 快捷键帮助在设置里；画布快捷键以编辑器内说明为准。

---

## 给用户的回复模板

交付 JSON 文件路径后，用短列表说明相对原稿改了什么（模型、拓扑、版式），不要把整份 JSON 贴进对话。

```
已生成：<路径>

导入：编辑器汉堡菜单 → JSON 导入（建议空画布）。导入后按 R 复位。

相对原稿：
- 模型：…
- 拓扑：…
- 版式：…
```
