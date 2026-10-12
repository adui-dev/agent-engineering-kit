#!/usr/bin/env bash
# Reproducible CLI smoke check. Creates only temporary test directories.
set -euo pipefail
cd "$(dirname "$0")/.."

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/empty"
cp -R examples/existing-python "$tmp/existing"

python3 scripts/init.py --target "$tmp/empty" --lang en --skill git-commit
test ! -e "$tmp/empty/.agents"
python3 scripts/init.py --target "$tmp/empty" --lang en --skill git-commit --apply
cmp prompts/project-initialization.en.md "$tmp/empty/.agents/prompts/project-initialization.md"
cmp .agents/skills/git-commit/SKILL.md "$tmp/empty/.agents/skills/git-commit/SKILL.md"
test -f "$tmp/empty/.agents/skills/git-commit/THIRD_PARTY_LICENSE.md"

python3 scripts/init.py --target "$tmp/existing" --lang zh-CN --apply
cmp prompts/project-initialization.zh-CN.md "$tmp/existing/.agents/prompts/project-initialization.md"
python3 -m unittest discover -s "$tmp/existing/tests" -v

# A second install must fail rather than overwrite files.
if python3 scripts/init.py --target "$tmp/existing" --apply >/dev/null 2>&1; then
  echo "ERROR: existing output was not rejected" >&2
  exit 1
fi
echo "Smoke check passed: preview, safe install, copy integrity, existing code, and conflicts."
