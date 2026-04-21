LFTG APP ROADMAP

LAST UPDATED
- 2026-03-28

PLANNING MODEL
- NOW = stability and polish for active use
- NEXT = UX quality and maintainability
- LATER = scaling and automation

NOW
- Keep What Is LFTG visual story stable and editable
- Keep teacher/photo layout consistent
- Keep leaderboards clean and readable
- Keep docs/lftg-app as canonical state

NEXT
- Add a small visual settings panel (photo border width, frame style, font preset)
- Add optional caption editor for story images
- Add data freshness stamp (last sync date/time)
- Add reusable component helpers to reduce inline HTML/CSS blocks in app.py

LATER
- Split monolithic app.py into modular sections
- Add test/check script for CSV schema drift
- Add automated backup snapshot for lftg-data/data and lftg-app/assets

OPERATING PRINCIPLE
- Prefer durable files over chat-only decisions.
- Every meaningful UI or content change gets logged in CHANGELOG.md.
