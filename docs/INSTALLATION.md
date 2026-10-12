# 🧰 安全初始化工具

本仓库附带 Python 3.10+、无第三方依赖的初始化工具 [scripts/init.py](../scripts/init.py)。用途是把**一份选定语言的 Prompt**和**用户明确选择的 Skills**安装到已有项目目录；它**不会替你生成业务需求、架构设计或未确认的项目文档**。

## 准备

1. 获取/克隆 Agent Engineering Kit 仓库。
2. 在本机安装 Python 3.10+。
3. 准备一个**已经存在的目标项目目录**，它不应是本工具包仓库自身。

### Windows PowerShell

以下命令在工具包根目录执行，路径请按实际项目修改：

```powershell
# 只预览，不写入
python scripts/init.py --target ..\my-project --lang zh-CN --skill git-commit

# 确认变更后写入
python scripts/init.py --target ..\my-project --lang zh-CN --skill git-commit --apply

# 列出支持安装的 Skills
python scripts/init.py --list-skills
```

### Linux / macOS

```bash
python3 scripts/init.py --target ../my-project --lang en --skill git-commit
python3 scripts/init.py --target ../my-project --lang en --skill git-commit --apply
```

`--skill` 可以重复指定，例如 `--skill git-commit --skill github-issues`。不指定时仅安装 Prompt。

**选择目标 Agent：** 使用 `--agent` 显式选择安装目录。默认值是 `generic`，以保持原有命令兼容。

| `--agent` | Skills 安装位置 | 说明 |
| --- | --- | --- |
| `generic`（默认） | `.agents/skills/` | 按需复用，自动发现取决于工具 |
| `codex` | `.agents/skills/` | 按 Codex 项目 Skills 约定安装 |
| `opencode` | `.agents/skills/` | OpenCode 官方支持的兼容路径 |
| `claude-code` | `.claude/skills/` | Claude Code 项目 Skills 标准目录 |

例如给 Claude Code 安装英文 Prompt 和指定 Skill：

```powershell
python scripts/init.py --target ..\\my-project --lang en --agent claude-code --skill git-commit
python scripts/init.py --target ..\\my-project --lang en --agent claude-code --skill git-commit --apply
```

该参数只调整 Skills 目录，Prompt 仍保存到 `.agents/prompts/project-initialization.md`，需要明确提示 Agent 阅读。安装路径符合文档规范不等于实测客户端已完成加载。

## 安装结果

```text
my-project/
└── .agents/
    ├── prompts/
    │   └── project-initialization.md
    └── skills/                 # 仅指定 --skill 时创建
        └── git-commit/
            ├── SKILL.md
            └── THIRD_PARTY_LICENSE.md
```

选定 Skill 内的 references/、scripts/、assets/（如果实际存在）会一起复制，以避免缺少引用资料。原始目录中的许可记录也会保留。

## 安全行为

- **默认 dry-run**：不加 `--apply` 只显示将写入的路径，目标目录不会变化。
- **不覆盖已有文件**：安装前检查所有目标文件；发现冲突便停止，没有 `--force` 参数。
- **路径保护**：拒绝未知 Skill、路径穿越名称、工具包目录或其子目录，以及符号链接技能文件；目标中如有符号链接父目录也会阻止安装。
- **失败回滚**：写入途中异常时删除本次创建的文件和空目录，不删除原有内容。
- **不做超出授权的操作**：不自动调用 Agent、不执行第三方 Skill、不操作 Git 提交/推送、不修改业务代码。

**注意：** 该工具只负责文件复制。安装之后，需要在目标项目的 AI 编程工具中**明确要求 Agent 阅读** `.agents/prompts/project-initialization.md` 并开始项目审查；目标工具是否会自动加载 Skills 必须另行验证。

## 实际验证

参阅 [使用示例与验收](EXAMPLES.md) 或从仓库根目录运行：

```bash
python -m unittest discover -s tests -v
bash scripts/smoke_init.sh
```

`smoke_init.sh` 是 Linux/macOS/GitHub Actions 使用的 Bash 脚本。Windows PowerShell 用户可直接运行 Python 单元测试，或在 Git Bash/WSL 环境中运行 Smoke Test。所有写入演示均在临时目录中进行。

## 维护规则

安装工具的 CLI 参数、目标文件路径、权限和覆盖行为变化时，必须同步更新 README 中英文版本、此文档、测试及 CI。绝不能将“Prompt/Skills 文件复制成功”描述为“目标 Agent 工程体系已通过实际验收”。
