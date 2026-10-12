# 🔐 安全政策 / Security Policy

## 支持的版本

| 版本 | 维护状态 |
| --- | --- |
| V1.1 | 当前稳定版 |
| V1.0 | 历史版本；建议升级 |

本仓库主要提供 Markdown Prompt、Skills 和自动化脚本；**任何外部 Skills 与脚本均应在执行前审查其来源和权限**。

## 漏洞报告

如果发现凭据泄露、恶意工作流、命令执行/路径遍历或供应链风险，**请勿在公开 Issue 中透露可利用细节或密钥**。优先通过 GitHub 的私密漏洞报告功能提交（若仓库已启用）：

- https://github.com/adui-dev/agent-engineering-kit/security/advisories/new

如上述入口不可用，请先通过私密渠道与仓库维护者联系，勿在公开仓库粘贴敏感数据。本仓库目前**不承诺固定响应时限**，会根据影响程度评估并处理。

## 贡献者安全约定

- 不提交 Token、密码、私钥或其他真实凭据。
- 新增第三方 Skill 时检查许可证、引用脚本及请求的外部权限。
- 工作流遵循最小权限，外部 Actions 版本使用不可变 Commit SHA。
- 不在 Pull Request 中执行来自不可信输入的高权限操作。
- 发现可疑内容请停止执行并报告，不以删除检查机制作为修复手段。

## English summary

Report suspected vulnerabilities **privately** via GitHub Security Advisories where enabled. Do not disclose secrets or exploitable details in public Issues. Review third-party Skills and scripts before executing them. No guaranteed response SLA is currently offered.
