# 📝 更新日志

本仓库采用 **V主版本.次版本** 的公开版本标识，版本来源为根目录 [VERSION](VERSION)。不自动将文档版本视为 Git Tag 或 GitHub Release。

## V1.0 — 首个正式版本（2026-10-12）

**发布说明：** [V1.0](docs/releases/V1.0.md) · **Git Tag：** `v1.0.0`

- 🧭 提供跨技术栈工程初始化 Prompt，覆盖 AGENTS、REQUIREMENTS、SDD、ARCHITECTURE、PROJECT_CONTEXT、CODEBASE_MAP、Skills 与 Harness。
- 🧩 收录 8 项 Git/GitHub/Actions Skills，保留第三方上游版本与 MIT 许可。
- 📝 提供中文 + Emoji Conventional Commits 协作规则。
- ✅ 增加依赖 Python 标准库的文档与 Skills 校验脚本、单元测试及质量检查 CI。
- 📚 完善快速使用、版本约定及质量检查说明。

### 已知限制

- 初始化 Prompt 必须在目标工作区由具有访问权限的 Agent 执行，单独复制 Prompt 不会自动修改仓库。
- Skills 是否被自动发现及支持的外部操作，取决于具体 AI 编程工具和连接权限。
- 静态校验不等同于业务测试、全面语义一致性或安全审计。

## 更新约定

- 更新版本时先调整 [VERSION](VERSION)，再同步 Prompt、README、AGENTS 及本文档。
- 新增正式版本章节，不覆盖历史记录。
- Git Tag 和 GitHub Release 仅在通过检查并得到明确授权后创建；流程见 [发布规范](docs/RELEASING.md)，不强制修改已发布版本。
