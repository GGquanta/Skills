# 架构图评审清单

来自企业混合云 3D 图的实际返工。生成 JSON 后逐项勾选；任一失败则改脚本重生成，不要只改一两处坐标凑合。

## 模型语义

| 检查 | 失败样子 | 改法 |
|---|---|---|
| 网关外形 | HybridGW / VPN 与 Internet 同为地球仪 | 网关改 `router`，橙材质，标签 VPN Gateway |
| 本地库命名 | 本地机架标成 CloudDB | 本地 Database + `database-server`；云 CloudDB + `database` |
| 计算 vs 存储 | K8s 与 OSS 同一团云 / 同一机柜无差别 | K8s 用 application-server（或库内 K8s 图标）；OSS 用 storage |
| 防火墙 | 砖墙 `firewall` | 改 `firewall1` |
| 问号立方体 | Mermaid icon 或编造的 GLB 路径 | 只使用 model-catalog 中的路径 |

## 拓扑

| 检查 | 失败样子 | 改法 |
|---|---|---|
| 终端上联 | PC 与 Laptop 互连 | 删除该边；两台都连 CoreSwitch（或楼层交换机） |
| 出云路径 | 从交换机或某台服务器直连云 | Firewall → 混合网关（虚线） |
| 云区结构 | K8s 串 CloudDB 再串 OSS | 网关分别连 K8s、CloudDB、OSS |
| 流量方向 | 全是双向箭头、看不出访问方向 | 入云 / 访问用单箭头；专线虚线 |

## 版式

| 检查 | 失败样子 | 改法 |
|---|---|---|
| 走线 | 斜线穿过机柜 | 直角折线，在空地拐弯 |
| 共线误读 | Laptop 走线看起来经 PC 中转 | 先沿汇聚轴走一段，再提前分叉到目标 `x` |
| 分区 | 全图同一浅蓝 | 云区橙、分支绿灰 |
| 终端比例 | PC / 笔记本与机柜一样大 | `scale: 0.7` |
| 标签 | 只有地面字或只有悬浮 | 设备 `tipShow: true`，地面仍保留短标签 |
| 对齐 | 坐标带一长串小数、左右错位 | 网格对齐（整数或 0.25） |

## 数据完整性

- `key` 唯一；`options.key` 与外层一致。
- `linkLineKeys` ↔ `line` ↔ `startElementKey`/`endElementKey` 三向闭合。
- 修订旧图时未悄悄丢掉灯光或区标题。
