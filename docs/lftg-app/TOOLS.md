LFTG APP TOOLS

LAST UPDATED
- 2026-04-21

PURPOSE
- Canonical runbook for day-to-day edits and maintenance.

COMMON COMMANDS
- Sync main data:
  - python3 lftg-data/sync-from-sheet.py
- Sync video data:
  - python3 lftg-data/sync-video-database.py
- Run public release preflight check:
  - ./scripts/release-check.sh
- Run end-to-end release flow (optional):
  - ./scripts/release-publish.sh --sync
- Restart app:
  - pkill -f "python3 -m streamlit run /Users/ndgms/.openclaw/workspace/lftg-app/app.py" || true
  - python3 -m streamlit run /Users/ndgms/.openclaw/workspace/lftg-app/app.py --server.port 8501 --server.headless true

ACCESS
- Local: http://localhost:8501
- LAN: http://192.168.1.31:8501

EDIT PATHS
- Main app file: lftg-app/app.py
- Story photos: lftg-app/assets/what-is-lftg-final/
- Teacher photos: lftg-app/assets/ndgms-teachers/
- Posters: lftg-app/assets/posters/
- Band photos: lftg-app/assets/bands/

SAFE EDIT HABITS
- Make one visual change at a time.
- Restart app + hard refresh when UI looks stale.
- Commit each accepted tweak with a clear message.
- Update docs/lftg-app/CHANGELOG.md for every meaningful shipped change.
- If operations/architecture changed, update TOOLS.md and/or ARCHITECTURE.md in the same session.

REFERENCE
- Architecture: docs/lftg-app/ARCHITECTURE.md
- Roadmap: docs/lftg-app/ROADMAP.md
- Change history: docs/lftg-app/CHANGELOG.md
- Public release safety checklist: docs/lftg-app/PUBLIC-RELEASE-CHECKLIST.md
