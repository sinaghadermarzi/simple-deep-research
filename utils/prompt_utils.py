"""
Prompt loader — reads all .md files from the prompts/ directory and exposes
them as module-level string attributes. The filename (without extension) becomes
the attribute name, so existing callers like:

    prompts.agent_system_prompt.format(date=...)

continue to work without any changes.
"""

import pathlib

_PROMPTS_DIR = pathlib.Path(__file__).parent.parent / "prompts"

def _load_prompts(directory: pathlib.Path) -> dict:
    return {
        p.stem: p.read_text(encoding="utf-8")
        for p in sorted(directory.glob("*.md"))
    }

globals().update(_load_prompts(_PROMPTS_DIR))
