"""
build.py — CBZ Pipeline HTML Builder
=====================================
Reads data from cbz_pipeline_data/data.py, serialises it to a JavaScript
_DB block, injects it into the HTML template, and writes the output to
../docs/index.html (the GitHub Pages source).

Run from the pycharm_updater/ directory:
    python build.py

Options:
    python build.py --preview      Open the result in your default browser
    python build.py --output PATH  Write to a custom path instead
    python build.py --dry-run      Print the generated _DB block, don't write
"""

import json
import os
import re
import sys
import webbrowser
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
THIS_DIR   = Path(__file__).parent
TEMPLATE   = THIS_DIR / "template" / "shell.html"
OUTPUT     = THIS_DIR.parent / "docs" / "index.html"
UPDATES    = THIS_DIR.parent / "updates"

# ── CLI flags ─────────────────────────────────────────────────────────────────
PREVIEW  = "--preview"  in sys.argv
DRY_RUN  = "--dry-run"  in sys.argv
CUSTOM_OUT = next((sys.argv[i+1] for i, a in enumerate(sys.argv)
                   if a == "--output" and i+1 < len(sys.argv)), None)

if CUSTOM_OUT:
    OUTPUT = Path(CUSTOM_OUT)


# ── Import data ───────────────────────────────────────────────────────────────
sys.path.insert(0, str(THIS_DIR))
from cbz_pipeline_data.data import (
    users, its, pipeline, tobacco, nonfunded, ntb, loc,
    disbursements, tobacco_repayments, tobacco_drawdowns,
    tobacco_disbursements, nf_disbursements,
    finance, finance_by_role, audit, targets,
)


# ── Helpers ───────────────────────────────────────────────────────────────────
def _js(obj) -> str:
    """Compact JSON — valid JavaScript literal."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def build_db_block() -> str:
    """Return the full `let _DB = { ... };` JavaScript string."""
    lines = ["let _DB = {"]

    def section(name: str, value):
        return f"  {name}:{_js(value)},"

    lines.append(section("its",                   its))
    lines.append(section("users",                 users))
    lines.append(section("pipeline",              pipeline))
    lines.append(section("tobacco",               tobacco))
    lines.append(section("nonfunded",             nonfunded))
    lines.append(section("ntb",                   ntb))
    lines.append(section("loc",                   loc))
    lines.append(section("disbursements",         disbursements))
    lines.append(section("tobaccoRepayments",     tobacco_repayments))
    lines.append(section("tobaccoDrawdowns",      tobacco_drawdowns))
    lines.append(section("tobaccoDisbursements",  tobacco_disbursements))
    lines.append(section("nfDisbursements",       nf_disbursements))
    lines.append(section("finance",               finance))
    lines.append(section("financeByRole",         finance_by_role))
    lines.append(section("audit",                 audit))
    lines.append(section("targets",               targets))
    lines.append('  "hiddenDisbIds":[],')
    lines.append("};")

    return "\n".join(lines)


def inject_into_template(db_block: str) -> str:
    """
    Read shell.html and replace the sentinel comment with the live _DB block.
    The sentinel in shell.html is exactly:

        /* @@DB_BLOCK@@ */

    wrapped inside a <script> tag.
    """
    html = TEMPLATE.read_text(encoding="utf-8")
    sentinel = "/* @@DB_BLOCK@@ */"
    if sentinel not in html:
        raise ValueError(
            f"Sentinel '{sentinel}' not found in template.\n"
            f"Make sure template/shell.html contains exactly: {sentinel}"
        )
    return html.replace(sentinel, db_block)


def archive_previous():
    """Copy the current docs/index.html into updates/ before overwriting."""
    if OUTPUT.exists():
        import time
        stamp = time.strftime("%Y-%m-%d")
        dest  = UPDATES / f"CBZ_Pipeline_backup_{stamp}.html"
        UPDATES.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(OUTPUT.read_bytes())
        print(f"  ✓ Archived previous version → updates/{dest.name}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("CBZ Pipeline Builder")
    print("=" * 40)

    # 1. Generate the _DB block
    db_block = build_db_block()
    print(f"  ✓ _DB block built  ({len(db_block):,} chars)")

    if DRY_RUN:
        print("\n── DRY RUN: _DB block preview (first 2000 chars) ──")
        print(db_block[:2000])
        print("...\n(use without --dry-run to write output)")
        return

    # 2. Inject into template
    html = inject_into_template(db_block)
    print(f"  ✓ Injected into template  ({len(html):,} chars total)")

    # 3. Archive previous version
    archive_previous()

    # 4. Write output
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"  ✓ Written → {OUTPUT.resolve()}")

    # 5. Optionally open in browser
    if PREVIEW:
        url = OUTPUT.resolve().as_uri()
        webbrowser.open(url)
        print(f"  ✓ Opened in browser: {url}")

    print("\nDone. Commit and push to deploy to GitHub Pages.")
    print("  git add docs/index.html")
    print('  git commit -m "data: update pipeline data"')
    print("  git push origin main")


if __name__ == "__main__":
    main()
