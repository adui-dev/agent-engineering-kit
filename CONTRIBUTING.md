# 🤝 贡献与 Git 提交规范

本仓库默认使用**简体中文**编写文档、PR 描述和 Git Commit 描述，英文用于必要的跨语言交流。

## 提交格式

```text
<type>(<scope>): <emoji> <中文描述>
```

例如：

```text
docs(prompt): 📝 增加通用项目工程初始化指令
feat(skills): ✨ 集成 git-commit 提交技能
fix(docs): 🐛 修复文档链接
ci(check): 👷 增加 Markdown 自动校验
chore(repo): 🔧 更新仓库配置
```

类型：`feat` 新能力、`fix` 修复、`docs` 文档、`style` 格式、`refactor` 重构、`perf` 性能、`test` 测试、`build` 构建、`ci` 持续集成、`chore` 维护、`revert` 回退。

建议主题行控制在 72 个字符内；实际判断 type 和 scope 应以 diff 为准。一次提交只包含一个逻辑变更；不提交敏感信息；不得使用 `--no-verify` 绕过 hooks，未经授权不得强制推送。破坏性变更遵循 Conventional Commits 的 `!` 或 `BREAKING CHANGE:`。

## git-commit Skill

项目已收录 GitHub awesome-copilot 的 [git-commit](.agents/skills/git-commit/SKILL.md) Skill。上游采用 MIT，许可及署名保留于 [THIRD_PARTY_LICENSE.md](.agents/skills/git-commit/THIRD_PARTY_LICENSE.md)。

Skill 的标准流程（审查 diff → 按逻辑暂存 → 选择类型与范围 → 提交）保持不变。**本仓库的中文和 Emoji 要求由本文件及 AGENTS.md 提供，并覆盖该 Skill 默认的英文描述示例。**

## conventional-commit Skill

项目同时收录 [conventional-commit](.agents/skills/conventional-commit/SKILL.md)，用于规范提交消息。两项 Skill 的通用英文示例仅供参考：**本仓库统一采用 `type(scope): emoji 中文描述`**。无论 Skills 如何描述执行流程，实际 Git 提交和推送均需要获得用户授权。

## 中英文文档维护

- [README.md](README.md) 是默认中文版，[README.en.md](README.en.md) 为英文版。两个入口必须相互链接。
- 项目介绍、主要能力、使用步骤、版本与许可证说明变动时，同步更新两份 README，不添加未实现的英文初始化 Prompt。
- 仓库中的项目规范和上游 Skills 保持各自原有语言；英文版 README 应准确指向真实存在的文件，不应虚构英文版规范。
- 修改后运行项目文档验证和单元测试。

## 正式发布

首次版本与后续发布操作请遵循 [发布规范](docs/RELEASING.md)，发布前先审查代码和 Release Notes；版本 Tag 不得强制覆盖。

## 提交前验证

修改 Prompt、文档或 Skills 后，建议运行：

```bash
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

详细规则见 [仓库质量检查](docs/QUALITY.md)，首次正式版本 V1.0 见 [更新日志](CHANGELOG.md)。只提交必要文件，不绕过校验。
