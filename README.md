# Skills

面向 AI coding agent 的 [Agent Skills](https://agentskills.io/) 收集仓。每个 skill 是独立目录，入口为 `SKILL.md`，可被 [skills.sh](https://skills.sh) / `npx skills` 发现与安装。

[![skills.sh](https://skills.sh/b/GGquanta/Skills)](https://skills.sh/GGquanta/Skills)

## 安装

```bash
npx skills add GGquanta/Skills
```

只装某一个：

```bash
npx skills add GGquanta/Skills --skill icraft-3d-architecture
```

Claude Code 也可注册为 plugin marketplace：

```
/plugin marketplace add GGquanta/Skills
```

## 当前 Skills

### icraft-3d-architecture

用 [iCraft Editor](https://icraft.gantcloud.com/app/editor) 绘制、修订企业级 3D 架构图。以场景元素 JSON 为交付主路径，用 Python 生成直角走线、分区着色与已验证模型路径。

**适用场景：**

- 画或改 iCraft 3D 架构图（网络、混合云、机房、云产品拓扑）
- 根据编辑器导出的元素 JSON 改布局、换模型、改连线
- 对齐官方模板画风

路径：[`skills/icraft-3d-architecture`](./skills/icraft-3d-architecture)

## 仓库结构

```
skills/
  {skill-name}/
    SKILL.md          # 必填
    scripts/          # 可选
    references/       # 可选
```

`npx skills` 会扫描 `skills/` 下最多三层的 `SKILL.md`。新增 skill 的约定见 [AGENTS.md](./AGENTS.md)。

## License

MIT
