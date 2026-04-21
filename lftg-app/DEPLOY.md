LFTG APP DEPLOYMENT GUIDE

GOAL
Publish the Streamlit app so it is viewable on the web.

APP ENTRY FILE
- lftg-app/app.py

DEPENDENCIES
- Root requirements.txt includes lftg-app requirements.

RECOMMENDED FIRST DEPLOY (FASTEST): STREAMLIT COMMUNITY CLOUD

1) Push this workspace to a GitHub repo
2) Go to https://share.streamlit.io/
3) New app -> select repo/branch
4) Set main file path to:
   lftg-app/app.py
5) Deploy

DATA STRATEGY (CURRENT)
- App reads local CSV snapshots in:
  lftg-data/data/
- This is good for a stable public MVP.
- To update data, regenerate/sync locally, commit CSV changes, and redeploy.

UPDATE WORKFLOW FOR LIVE APP
1) Sync latest sheets locally:
   python3 lftg-data/sync-from-sheet.py
   python3 lftg-data/sync-video-database.py
2) Commit updated CSV files in lftg-data/data/
3) Push to GitHub
4) Streamlit Cloud redeploys automatically (or click Reboot).

ASSETS REQUIRED
- Posters:
  lftg-app/assets/posters/
- Band photos:
  lftg-app/assets/bands/
- Theme background:
  lftg-app/assets/theme/icftg-bg.jpg

PRE-LAUNCH CHECKLIST
- App loads without local-only assumptions
- All tabs render
- Random performer/band/show checks pass
- Video links open correctly (embed may fail for some videos due YouTube policy)
- Large media folders are present in repo (or hosted externally)

OPTIONAL NEXT STEP (AFTER MVP)
- Add live Google Sheets fetch in production via service account and Streamlit secrets,
  so web app updates without git commits.
