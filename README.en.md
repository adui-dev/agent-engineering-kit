# 🚀 Agent Engineering Kit

[简体中文](README.md) · **English**

[![Release](https://img.shields.io/github/v/release/adui-dev/agent-engineering-kit?label=Release)](https://github.com/adui-dev/agent-engineering-kit/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Quality Checks](https://github.com/adui-dev/agent-engineering-kit/actions/workflows/quality.yml/badge.svg)](https://github.com/adui-dev/agent-engineering-kit/actions/workflows/quality.yml)

**Help AI coding agents understand your project, follow its conventions, verify changes, and keep engineering context up to date—not just generate code.**

Agent Engineering Kit is a **technology-agnostic toolkit for sustainable AI-assisted development**. It provides a reusable project-initialization prompt, task-focused Skills, collaboration rules, and lightweight quality checks for greenfield repositories, existing codebases, and monorepos.

> **Current version: V1.1** · [Stable release](https://github.com/adui-dev/agent-engineering-kit/releases/tag/v1.1.0) · [Changelog](CHANGELOG.md)
>
> This is an **engineering toolkit**, not an application framework. Copying a prompt alone does not create a runnable application.

## ✨ What problems does it solve?

| Challenge | What this toolkit provides |
| --- | --- |
| A new agent lacks project context | A single collaboration entry point, project context, and codebase map |
| Requirements, architecture, and implementation drift apart | Clear document ownership, traceability, and update rules |
| Development instructions must be repeated in every session | Reusable AGENTS rules and task-specific Skills |
| AI-written changes are not properly verified | A Harness, real tests, and a feedback loop |
| New projects and existing repositories need different setups | Repository analysis first, then minimal, incremental initialization |

**Who it's for:** developers and teams working with AI coding tools or multiple agents. It can be applied to web, mobile, backend, desktop, game, and library projects without enforcing a particular language or framework.

## 🚀 Get started in 3 steps

**1. Open your target project**

Open the project you want to initialize in Codex, OpenCode, Claude Code, or another AI coding tool that can access project files. **Do not initialize this toolkit repository as if it were your application.**

**2. Copy the initialization prompt**

Choose **[📋 Universal Project Initialization Prompt V1.1 (English)](prompts/project-initialization.en.md)** or the **[Simplified Chinese version](prompts/project-initialization.zh-CN.md)**. Send the complete prompt in your preferred language to your coding agent. Both versions cover the same 16 sections, engineering assets, and execution constraints.

**3. Review the actual deliverables**

Your agent should inspect the repository before creating or updating the necessary documentation, Skills, and Harness. It should run available checks and report exactly what changed, what passed, and which decisions still need confirmation.

You can append the following instruction:

> Follow Project Initialization Prompt V1.1. Inspect the current repository and existing rules first; make only necessary changes; distinguish implemented features from planned or unconfirmed work; create the required files and run applicable checks instead of producing generic templates.

**Important:** The coding tool needs the necessary filesystem and execution permissions. If an operation cannot be performed, it must be reported rather than presented as completed. The initialized engineering assets belong in the **target repository**.

## 🧰 Optional: safe CLI setup

To copy a selected prompt and optional Skills into an existing project, use the dependency-free Python 3.10+ installer:

```bash
# Preview only (the default, writes nothing)
python scripts/init.py --target ../my-project --lang en --skill git-commit

# Explicitly apply after reviewing the file list
python scripts/init.py --target ../my-project --lang en --skill git-commit --apply
```

Use `--agent codex`, `--agent opencode`, or `--agent claude-code` to select the documented Skills layout (Claude Code uses `.claude/skills/`). The CLI **does not generate project-specific requirements, run third-party Skills, or overwrite existing files**. Cross-platform installation checks are available with `python scripts/smoke_init.py` (Windows/Linux/macOS), plus a [read-only installation integrity check](scripts/verify_installation.py). See the [installation guide](docs/INSTALLATION.md) and [runnable examples](docs/EXAMPLES.md) (documentation currently in Chinese).

## 🧭 Eight core engineering assets

| Asset | Responsibility |
| --- | --- |
| **AGENTS** | How AI agents collaborate and which rules they follow |
| **REQUIREMENTS** | What the project must deliver and how to accept it |
| **SDD** | Detailed module, API, data, and workflow design |
| **ARCHITECTURE** | System organization and technical design rationale |
| **PROJECT_CONTEXT** | Background, actual progress, decisions, and open issues |
| **CODEBASE_MAP** | Where the important code, configuration, and modules live |
| **Skills** | Reusable workflows for specialized tasks |
| **Harness** | How to run, inspect, test, and validate changes |

Add **ADR (Architecture Decision Records)** and **Documentation Validation** when warranted by the project; don't create placeholder assets solely to fill a checklist.

**Continuous development loop:**

```text
Understand requirements → Load context → Design & assess impact → Minimal implementation
            ↑                                                 ↓
      Deliver results ← Update relevant docs ← Test & validate changes
```

## 🧩 Included Skills

The repository includes **8 project-level Skills** that can be loaded as needed:

| Category | Skills |
| --- | --- |
| Git commits | [git-commit](.agents/skills/git-commit/SKILL.md), [conventional-commit](.agents/skills/conventional-commit/SKILL.md) |
| GitHub Issues | [github-issues](.agents/skills/github-issues/SKILL.md), [create issues from implementation plans](.agents/skills/create-github-issues-feature-from-implementation-plan/SKILL.md) |
| Pull Requests | [create a PR from a specification](.agents/skills/create-github-pull-request-from-specification/SKILL.md) |
| GitHub Actions | [security hardening](.agents/skills/github-actions-hardening/SKILL.md), [efficiency](.agents/skills/github-actions-efficiency/SKILL.md), [workflow specification](.agents/skills/create-github-action-workflow-specification/SKILL.md) |

See the [Skills index](docs/SKILLS.md) (Chinese) for source revisions, licenses, usage constraints, and known limitations.

Skills are stored under `.agents/skills/`. **Automatic discovery depends on your AI coding tool.** External GitHub access, permissions, and compatibility may require additional setup. Some upstream content is historical; review compatibility before use.

## 📁 Repository guide

| Path | Purpose |
| --- | --- |
| [Initialization prompt (English)](prompts/project-initialization.en.md) / [中文版本](prompts/project-initialization.zh-CN.md) | Complete instructions for project setup and continuous development in either language |
| [AGENTS.md](AGENTS.md) | Rules for agents working on this toolkit (Chinese) |
| [Skills index](docs/SKILLS.md) | Skill sources, usage, and maintenance (Chinese) |
| [Quality checks](docs/QUALITY.md) | Local checks, CI, and validation scope (Chinese) |
| [CLI installation](docs/INSTALLATION.md) | Dry-run, languages, Skills, and collision-safe copying (Chinese) |
| [Examples and acceptance](docs/EXAMPLES.md) | Greenfield and runnable existing-project samples (Chinese) |
| [Agent compatibility](docs/COMPATIBILITY.md) | Codex, OpenCode, and Claude Code validation status (Chinese) |
| [Real-agent acceptance](docs/AGENT_ACCEPTANCE.md) | Client discovery, Skill invocation and initialization checklist (Chinese) |
| [Acceptance workspace preparer](scripts/prepare_agent_acceptance.py) | Prepare disposable Codex/OpenCode/Claude Code test projects without launching agents |
| [Security policy](SECURITY.md) | Private vulnerability reporting and supply-chain guidance |
| [Repository safeguards](docs/MAINTENANCE.md) | Branch rules, required checks, release approvals (Chinese) |
| [Contributing guide](CONTRIBUTING.md) | Emoji and Chinese Conventional Commits (Chinese) |
| [Release guide](docs/RELEASING.md) | Versioning and release process (Chinese) |
| [Changelog](CHANGELOG.md) | Released versions and unreleased changes (Chinese) |
| `.agents/skills/` | Task-specific Skills and references |
| `scripts/` and `tests/` | Repository validation scripts and tests |

This is a **navigation guide**, not an exhaustive repository tree.

## ✅ Quality checks

To contribute to this repository, use **Python 3.10+**. No extra Python packages are required:

```bash
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

Checks cover version consistency, relative Markdown links, basic Skill metadata, and license files. GitHub Actions runs the checks for pushes and pull requests. These structural checks **do not replace** application tests, tool compatibility testing, or a comprehensive security audit.

## 📦 Releases, contributions, and license

- **Active development branch:** `main`. **Latest stable release:** [V1.1 / v1.1.0](https://github.com/adui-dev/agent-engineering-kit/releases/tag/v1.1.0). **First release:** [V1.0 / v1.0.0](https://github.com/adui-dev/agent-engineering-kit/releases/tag/v1.0.0).
- **Version distinction:** `main` continues to evolve, while the `v1.1.0` and `v1.0.0` source snapshots remain unchanged.
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md). Commit messages follow `type(scope): emoji 中文描述`.
- **License:** [MIT License](LICENSE). Third-party Skills retain their respective copyright and license notices.

For questions, bug reports, or ideas, open a [GitHub Issue](https://github.com/adui-dev/agent-engineering-kit/issues).
