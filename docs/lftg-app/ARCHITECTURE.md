LFTG APP ARCHITECTURE

LAST UPDATED
- 2026-03-28

PURPOSE
- Canonical architecture reference for the Streamlit LFTG app.
- Durable context outside chat history.

SYSTEM OVERVIEW
- UI app: lftg-app/app.py
- Runtime: Streamlit (Python)
- Data source model: Google Sheets -> sync scripts -> local CSV snapshots
- Asset model: local image folders under lftg-app/assets

CORE DATA FILES
- lftg-data/data/shows.clean.csv
- lftg-data/data/bands.clean.csv
- lftg-data/data/appearances.normalized.csv
- lftg-data/data/performers.clean.csv
- lftg-data/data/setlists.clean.csv
- lftg-data/data/videos.clean.csv

SYNC PIPELINE
- Main dataset sync: lftg-data/sync-from-sheet.py
- Video dataset sync: lftg-data/sync-video-database.py

APP SECTIONS
- Show Explorer
- Performer
- Band
- Leaderboards
- What Is LFTG?

DESIGN CONVENTION
- Visual story content and layout changes should be tracked in CHANGELOG.md.
- Operational commands and recovery live in TOOLS.md.
- Planned improvements live in ROADMAP.md.

REFERENCE
- Legacy/expanded ops docs still available:
  - docs/LFTG-APP-OPERATIONS.md
  - docs/LFTG-APP-QUICKSTART.md
  - docs/LFTG-APP-RECOVERY-CHECKLIST.md
