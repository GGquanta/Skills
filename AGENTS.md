# AGENTS.md

给在本仓库工作的 coding agent 用的说明。

## 仓库做什么

这是一份 [Agent Skills](https://agentskills.io/) 收集仓。每个 skill 是独立目录，入口是 `SKILL.md`。`npx skills` 会扫描 `skills/`（最多三层）并发现其中的 `SKILL.md`。

## 目录约定

```
skills/
  {skill-name}/           # kebab-case
    SKILL.md              # 必填：YAML frontmatter + 指令
    scripts/              # 可选：可执行脚本
    references/           # 可选：按需加载的参考文档
    assets/               # 可选：模板、图标等输出资源
```

不要在 skill 目录里放 `README.md`。给人看的说明写在仓库根 `README.md`。

## 命名

- 目录名与 `SKILL.md` 的 `name` 一致，kebab-case
- 入口文件必须是 `SKILL.md`（全大写，不能改名）
- 脚本用 `kebab-case.py` / `kebab-case.sh` / `kebab-case.mjs`

## SKILL.md 格式

```markdown
---
name: {skill-name}
description: 第三人称。写清做什么、何时用，并带上触发词。
---

# {Skill Title}

## 何时使用
...

## 标准工作流
...

## Additional resources
- 细节见 [references/foo.md](references/foo.md)
```

必填字段：`name`（≤64，小写字母/数字/连字符）、`description`（≤1024，含 WHAT + WHEN）。

## 编写约束

- `SKILL.md` 控制在 500 行以内；细节放到 `references/`
- 从 `SKILL.md` 只链一层引用文件
- 描述写第三人称，带触发短语
- 能脚本化的不要把大段代码写进 SKILL.md
- 新增 skill 后同步：根 `README.md`、`.claude-plugin/marketplace.json`

## 安装命令（给用户看的）

```bash
npx skills add GGquanta/Skills
npx skills add GGquanta/Skills --skill {skill-name}
```

Claude Code marketplace：

```
/plugin marketplace add GGquanta/Skills
```
