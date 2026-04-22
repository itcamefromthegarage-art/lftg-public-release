LFTG APP PUBLIC RELEASE CHECKLIST

PURPOSE
- Quick safety + quality gate before every public push.
- Prevent accidental data leaks, broken deploys, and stale app content.

USE THIS WHEN
- You are about to push to main on the public repo.
- You updated code, data CSV files, or public-facing assets.

QUICK AUTOMATED CHECK
- Run this first:
  - ./scripts/release-check.sh
- Then use the checklist below for manual review points.

PRE-PUSH CHECKS
1) WORK IN THE CORRECT REPO
- Repo path should be: /Users/ndgms/.openclaw/workspace/lftg-public-release
- Run: git status
- Confirm only intended LFTG files changed.

2) SENSITIVE FILE CHECK
- Confirm you are NOT committing:
  - API keys
  - tokens
  - passwords
  - service account JSON files
  - private/internal docs not meant for public view
- Run a quick search before commit for terms like:
  - key
  - token
  - secret
  - password

3) APP ENTRY + STRUCTURE CHECK
- Confirm app entry file exists: lftg-app/app.py
- Confirm requirements files exist:
  - requirements.txt
  - lftg-app/requirements.txt

4) DATA CHECK
- If data changed, run:
  - python3 lftg-data/sync-from-sheet.py
  - python3 lftg-data/sync-video-database.py
- Confirm CSV files exist in lftg-data/data/ and look reasonable.

5) LOCAL VALIDATION
- Run: python3 -m py_compile lftg-app/app.py
- Optional visual test:
  - python3 -m streamlit run lftg-app/app.py --server.port 8501 --server.headless true
  - Check key tabs and sample records.

6) DOCS CHECK
- For meaningful change, add entry to docs/lftg-app/CHANGELOG.md
- If operations changed, update docs/lftg-app/TOOLS.md
- If architecture changed, update docs/lftg-app/ARCHITECTURE.md

PUSH + DEPLOY
1) COMMIT
- git add .
- git commit -m "clear message"

2) PUSH
- git push origin main

3) STREAMLIT VERIFY
- Wait for auto redeploy on Streamlit Cloud
- Open public URL in normal browser and private window
- Verify:
  - app loads
  - tabs work
  - posters/band photos load
  - video links work

ROLLBACK (IF NEEDED)
- Revert latest commit:
  - git revert <bad_commit_hash>
  - git push origin main
- Streamlit will redeploy the reverted version.
