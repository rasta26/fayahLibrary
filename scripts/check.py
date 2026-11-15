#!/usr/bin/env python3
"""Offline structural checks for fayahLibrary (no network, no deps).

- every JSON file parses
- every skills/*/SKILL.md has frontmatter with name (== dir) and description
- every agents/*.md and commands/*.md has frontmatter with description
- marketplace.json plugin sources exist and contain plugin.json
- light static safety pass: flags patterns SkillSpector would also flag, so the
  real scan has nothing obvious to find (curl|bash, eval of remote content,
  secrets, destructive rm, encoded payloads, instructions to ignore prior rules)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors, warnings = [], []

def frontmatter(p: Path):
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text

for jp in ROOT.rglob("*.json"):
    if ".git" in jp.parts:
        continue
    try:
        json.loads(jp.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"{jp.relative_to(ROOT)}: invalid JSON: {e}")

mk = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
for pl in mk["plugins"]:
    src = ROOT / pl["source"]
    if not (src / ".claude-plugin/plugin.json").exists():
        errors.append(f"marketplace plugin {pl['name']}: missing {pl['source']}/.claude-plugin/plugin.json")

SUSPICIOUS = [
    (r"curl[^\n|]*\|\s*(ba)?sh", "pipe-to-shell"),
    (r"wget[^\n|]*\|\s*(ba)?sh", "pipe-to-shell"),
    (r"\beval\s*\(", "eval"),
    (r"base64\s+(-d|--decode)", "base64 decode"),
    (r"rm\s+-rf\s+(/|~|\$HOME)\b", "destructive rm"),
    (r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})", "secret-looking token"),
    (r"ignore (all )?(previous|prior) instructions", "prompt-injection phrase"),
    (r"(exfiltrat|send .* to http)", "exfiltration phrase"),
]

def scan_text(p: Path, text: str):
    for pat, label in SUSPICIOUS:
        for m in re.finditer(pat, text, re.I):
            line = text.count("\n", 0, m.start()) + 1
            warnings.append(f"{p.relative_to(ROOT)}:{line}: {label}: {m.group(0)[:60]!r}")

for plugin_dir in (ROOT / "plugins").iterdir():
    for sk in (plugin_dir / "skills").glob("*/SKILL.md"):
        fm, text = frontmatter(sk)
        if fm is None:
            errors.append(f"{sk.relative_to(ROOT)}: missing frontmatter"); continue
        if fm.get("name") != sk.parent.name:
            errors.append(f"{sk.relative_to(ROOT)}: name '{fm.get('name')}' != dir '{sk.parent.name}'")
        if len(fm.get("description", "")) < 40:
            errors.append(f"{sk.relative_to(ROOT)}: description too short")
        scan_text(sk, text)
    for kind in ("agents", "commands"):
        for md in (plugin_dir / kind).glob("*.md"):
            fm, text = frontmatter(md)
            if fm is None or "description" not in fm:
                errors.append(f"{md.relative_to(ROOT)}: missing description frontmatter")
            scan_text(md, text)
    for sh in (plugin_dir / "hooks").glob("*.sh"):
        scan_text(sh, sh.read_text())
    for cfg in ("hooks/hooks.json", ".mcp.json"):
        f = plugin_dir / cfg
        if f.exists():
            scan_text(f, f.read_text())

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"check: {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
