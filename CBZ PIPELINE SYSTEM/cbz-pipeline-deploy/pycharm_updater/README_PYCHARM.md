# CBZ Pipeline — PyCharm Updater

This package is the **single source of truth** for all pipeline data.
Edit data here → run `build.py` → commit & push → GitHub Pages updates automatically.

---

## One-Time Setup in PyCharm

1. **Open project**: File → Open → select the `pycharm_updater/` folder
2. **Set interpreter**: File → Settings → Project → Python Interpreter  
   Select Python 3.8+ (no extra packages needed — stdlib only)
3. **Mark as Sources Root** (optional): right-click `pycharm_updater/` → Mark Directory as → Sources Root

That's it. No pip installs required.

---

## Workflow for Every Update

### Step 1 — Edit your data
Open `cbz_pipeline_data/data.py` and modify any list or dict.

```
cbz_pipeline_data/
└── data.py      ← ONLY FILE YOU EVER EDIT
```

Each section is clearly labelled:
- `users`               → add/remove/edit users
- `its`                 → Indicative Term Sheet entries
- `pipeline`            → Assessment / Near Drawdown / Ready
- `tobacco`             → Tobacco merchants
- `nonfunded`           → Non-funded facilities
- `ntb`                 → New-to-Bank clients
- `loc`                 → Lines of Credit
- `disbursements`       → Disbursement records
- `tobacco_repayments`  → Schedule dict (key: `"merchantId:YYYY-MM"`)
- `tobacco_drawdowns`   → Schedule dict
- `finance`             → Division-wide finance records
- `finance_by_role`     → Per-head finance (dict keyed by username)
- `audit`               → Audit log
- `targets`             → Monthly + annual disbursement targets

### Step 2 — Build
Run `build.py` from within PyCharm (right-click → Run 'build') or terminal:

```bash
python build.py
```

Optional flags:
```bash
python build.py --preview      # auto-opens in your browser after build
python build.py --dry-run      # preview JS output only, don't write files
python build.py --output PATH  # write to a custom path
```

The script:
1. Imports all data from `cbz_pipeline_data/data.py`
2. Serialises it into a JavaScript `let _DB = { ... };` block
3. Injects it into `template/shell.html` (replacing `/* @@DB_BLOCK@@ */`)
4. Archives the previous `docs/index.html` to `updates/` with a date stamp
5. Writes the new `docs/index.html` (served by GitHub Pages)

### Step 3 — Commit & push
```bash
git add docs/index.html
git commit -m "data: <describe what changed>"
git push origin main
```

GitHub Pages redeploys in ~30 seconds. Your live URL updates automatically.

---

## Adding a New Pipeline Entry (example)

In `cbz_pipeline_data/data.py`, find the `pipeline` list and append:

```python
{
    "id": 136,
    "stage": "assessment",
    "category": "ccc",
    "client": "My New Client Ltd",
    "rm_code": "RM003",
    "rm_name": "Rudo Chigumba",
    "department": "Agribusiness",
    "facility_type": "Working Capital",
    "currency": "USD",
    "facility_limit": 1_500_000,
    "drawdown_pending": 1_500_000,
    "interest_rate": 12.5,
    "commission": 1.25,
    "funding_type": "Bank Funding",
    "date_approved": "2025-07-01",
    "expected_date": "2025-09-30",
    "comments": "New facility notes here.",
    "created_at": "2025-07-01",
},
```

Then run `build.py` and push.

---

## File Map

```
pycharm_updater/
├── build.py                        ← Run this to regenerate docs/index.html
├── README_PYCHARM.md               ← This file
├── cbz_pipeline_data/
│   ├── __init__.py                 ← Package exports
│   └── data.py                     ← ★ ALL DATA LIVES HERE ★
└── template/
    └── shell.html                  ← HTML app with /* @@DB_BLOCK@@ */ sentinel
                                       (edit only for UI/layout changes)
```

---

## Updating the HTML Shell (UI changes)

If CBZ provides a new version of the HTML app:

1. Copy the new `.html` file to `template/shell.html`
2. Find the `let _DB = { ... };` block in it
3. Replace the entire block (from `let _DB = {` to the closing `};`) with exactly:
   ```
   /* @@DB_BLOCK@@ */
   ```
4. Run `build.py` — it will inject the current data into the new shell
5. Verify in browser with `python build.py --preview`
6. Commit & push

---

## Stage / Category Reference

| stage | category | Meaning |
|---|---|---|
| `assessment` | `ccc` | Credit Committee |
| `assessment` | `exco` | Executive Committee |
| `assessment` | `board` | Board Approval |
| `near` | `signed` | Signed Offer Letters |
| `near` | `security` | Awaiting Security Perfection |
| `near` | `util` | Awaiting Utilization Request |
| `ready` | `None` | Ready for Drawdown |
