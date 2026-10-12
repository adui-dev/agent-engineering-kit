# 🆕 空仓库初始化示例

这是一个**尚未选定技术栈**的项目示例，用于演示安全的初始化操作。不要据此虚构用户、业务或架构。

## 操作

从 Agent Engineering Kit 仓库根目录执行（下面的路径按实际位置修改）：

```bash
python scripts/init.py --target ./examples/greenfield --lang zh-CN
python scripts/init.py --target ./examples/greenfield --lang zh-CN --apply
```

第一次仅预览，第二次才会将 Prompt 写入目标项目。**执行示例前请在临时副本中操作**，避免把演示安装文件提交到工具包仓库。

然后要求 Agent 读取目标目录的 `.agents/prompts/project-initialization.md`，识别这是一个空项目，与使用者确认真实目标，按需创建工程规范。

**验收重点**：不编造业务；未确定技术栈不自行锁定；只创建必要文件；报告真实执行结果。
