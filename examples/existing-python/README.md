# 🐍 已有 Python 项目示例

此目录包含**可以运行的最小 Python 代码及测试**，用于检验初始化工具不会覆盖已有实现，也用于人工验证 Prompt 在既有代码仓库上的适配表现。

## 当前结构

```text
existing-python/
├── README.md
├── src/app.py
└── tests/test_app.py
```

## 运行原项目测试

从 Agent Engineering Kit 根目录执行：

```bash
python -m unittest discover -s examples/existing-python/tests -v
```

## 验证初始化

建议将本目录复制到临时目录后，再使用初始化 CLI：

```bash
python scripts/init.py --target /tmp/existing-python --lang en
python scripts/init.py --target /tmp/existing-python --lang en --apply
```

再运行上述原项目测试，并让 Agent 读取安装的 Prompt、识别真实 `src`、`tests` 和运行命令。

**验收重点**：现有代码及测试行为不变；文档中的路径和测试命令真实存在；不声明虚构功能；重复安装时拒绝覆盖。
