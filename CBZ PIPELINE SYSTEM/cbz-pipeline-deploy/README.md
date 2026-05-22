# CBZ Bank — Disbursement Pipeline System

Pilot test deployment via **GitHub Pages**.  
Live URL (after setup): `https://<your-username>.github.io/<repo-name>/`

---

## Repository Structure

```
cbz-pipeline-deploy/
├── docs/
│   └── index.html          ← The full single-file application
├── .github/
│   └── workflows/
│       └── deploy.yml      ← Auto-deploys to GitHub Pages on every push to main
├── updates/                ← Drop new versions here before replacing docs/index.html
│   └── README.md
└── README.md
```

---

## One-Time GitHub Pages Setup

1. Push this repo to GitHub (new repository, any name e.g. `cbz-pipeline`)
2. Go to **Settings → Pages**
3. Under *Source*, select **Deploy from a branch**
4. Branch: `main` | Folder: `/docs`
5. Click **Save**

GitHub will publish your app at:
```
https://<your-github-username>.github.io/cbz-pipeline/
```

> **Alternative (recommended):** Use the included GitHub Actions workflow.  
> Go to Settings → Pages → Source → **GitHub Actions**.  
> Every push to `main` will auto-redeploy in ~30 seconds.

---

## How to Push Updates

### Using PyCharm (recommended — see `pycharm_updater/`)

Open the `pycharm_updater/` project in PyCharm, edit your data in
`cbz_pipeline_data/data.py`, run `build.py`, and it will regenerate
`docs/index.html` automatically. Then commit and push.

### Manual update

1. Replace `docs/index.html` with your new version
2. Commit: `git add docs/index.html && git commit -m "Update: <description>"`
3. Push: `git push origin main`
4. GitHub Pages redeploys in ~30 seconds

---

## Test Credentials

| Username | Password | Role |
|---|---|---|
| `admin` | admin123 | System Admin |
| `exec1` | exec123 | Executive |
| `treasury1` | treas123 | Treasury |
| `tf1` | tf123 | Trade Finance |
| `rm1` – `rm8` | rm123 | Relationship Managers |
| `head-cib`, `head-bb`, `head-ib`, `head-agri`, `head-south`, `head-mani`, `cluster-mfg`, `cluster-svc` | head123 | Department Heads |

---

## Notes

- The app is a **self-contained single HTML file** — no server, no database, no backend required.
- All data lives in the `let _DB = { ... }` block inside `docs/index.html`.
- For structured data editing, use the `pycharm_updater/` package which keeps data in clean Python dicts and regenerates the HTML on demand.
