# 已验证模型路径

下列路径均在 iCraft 图库与官方网络模板语境下可落地。Agent **只使用本表或用户导出 JSON 里已出现的路径**；不要发明 `model/v1/kubernetes/scene.glb` 这类未验证路径。

材质色从同类导出拷贝。换 GLB 后不要沿用旧 `color` 长度。

## 网络与安全

| 角色 | 路径 | 外观 | 注意 |
|---|---|---|---|
| Internet | `model/v1/network/scene.glb` | 地球仪 | 只给公网入口 |
| 路由器 / VPN 网关 | `model/v1/router/scene.glb` | 路由器 | 网关换橙色材质 + 标签「VPN Gateway」 |
| 防火墙（推荐） | `model/v1/firewall1/scene.glb` | 立方体 + 盾 | 与官方网络参考图一致 |
| 防火墙（避免） | `model/v1/firewall/scene.glb` | 砖墙 | 企业架构图里像一堵墙，不要用 |
| 交换机 | `model/v1/switch/scene.glb` | 交换机 | 核心 / 汇聚 |

## 计算与存储

| 角色 | 路径 | 外观 | 注意 |
|---|---|---|---|
| Web | `model/v1/web-server/scene.glb` | Web 机柜 | 与 App 区分 |
| App / K8s 节点 | `model/v1/application-server/scene.glb` | 应用机柜 | K8s 无独立图标时用此；标签写 K8s |
| 本地数据库 | `model/v1/database-server/scene.glb` | 机架库 | 标签 Database |
| 云数据库 | `model/v1/database/scene.glb` | 圆柱库 | 标签 CloudDB |
| 对象存储 | `model/v1/storage/scene.glb` | 存储柜 | OSS / 对象存储 |

## 终端

| 角色 | 路径 | scale |
|---|---|---|
| PC | `model/v1/PC/scene.glb` | `0.7` |
| 笔记本 | `model/v1/laptop/scene.glb` | `0.7` |

## 参考色板（可直接抄）

路由器（蓝）：

```
["#5c6fda", "#ffffff", "#ffffff", "#e7e7e7", "#e7e7e7", "#e7e7e7", "#e7e7e7", "#ffffff", "#ffffff", "#ff920c"]
```

VPN 网关（橙，同槽位）：

```
["#faac4c", "#ffffff", "#ffffff", "#e7e7e7", "#e7e7e7", "#e7e7e7", "#e7e7e7", "#ffffff", "#ffffff", "#ff920c"]
```

地球仪：`["#fff8f8", "#5c6fda"]`  
交换机 / 圆柱库：`["#ffffff", "#3968d9"]` 或云库 `["#ffffff", "#faac4c"]`  
防火墙 `firewall1`：`["#ffffff", "#222222", "#faac4c", "#222222", "#faac4c", "#5c6fda", "#ffffff"]`

机柜类（web / app / database-server）色槽较多，从用户最近一次导出或本仓库 `hybrid-cloud-architecture.json` 拷贝对应数组。

## 分区台面色

| 分区 | `color` | `borderColor` |
|---|---|---|
| Internet / 本地 DC | `#d6dfff` | `#8f97b3` |
| 公有云 | `#ffe4cc` | `#c4925a` |
| 分支 / 用户 | `#e4f0e6` | `#7d9a82` |

## Mermaid 图标名（仅起稿）

`architecture-beta` 的 `service id(IconName)[Label]` 中，`IconName` 无空格。未命中图库 → 问号立方体。

不要指望 `Cloud` / `Gateway` 得到 Kubernetes 或独立网关模型；起稿后必须在 JSON 阶段按上表替换。
