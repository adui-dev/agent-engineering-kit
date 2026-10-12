# 📝 更新日志

本仓库采用 **V主版本.次版本** 的公开版本标识，版本来源为根目录 [VERSION](VERSION)。不自动将文档版本视为 Git Tag 或 GitHub Release。

## 未发布（Unreleased）

- ✅ 将 CI 扩展至 Ubuntu/Python 3.10、3.13 与 Windows/Python 3.13，统一 UTF-8 输出编码；发布前验证也包括初始化 Smoke Test。

- 🔧 支持按 Codex、OpenCode、Claude Code 选择 Skills 目标目录，并补充目录隔离、符号链接和兼容路径的回归测试。
- 📖 明确官方目录兼容与真实客户端实测的区别，保留尚未完成的 E2E 验收状态。

- 🧰 新增 Python 标准库初始化 CLI：默认预览、按需选择语言和 Skills、冲突拒绝及失败回滚。
- 🧪 增加空项目与已有 Python 项目的使用示例、CLI 单元测试与 Smoke Test，并接入 CI。
- 🔐 增加安全政策、Issue/PR 模板与 CODEOWNERS，准备更规范的开源协作。
- 🛡️ 将正式发布改为显式手动触发，避免版本文件的普通提交自动创建 Release。
- 🔗 修正 V1.1 发布说明中在 Release 页面无法正确跳转的相对链接，并增加兼容性与安装说明。

## V1.1 — 双语文档与英文初始化 Prompt（2026-10-12）

**发布说明：** [V1.1](docs/releases/V1.1.md) · **Git Tag：** `v1.1.0`

- 🌐 新增完整英文初始化 Prompt，保留与中文版对应的 16 个主章节和 8 类核心工程资产，支持双向语言切换。
- 📚 优化中文版 README、新增英文 README，补全快速使用、Skills 导航、质量检查及版本说明。
- ✅ 将双语 README、双语 Prompt 的存在性、版本号、链接和章节结构纳入自动校验，单元测试扩展至 15 项。
- 🔐 保持现有 Skills、许可声明和 GitHub Actions 质量校验机制，不引入新的业务框架或依赖。

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
