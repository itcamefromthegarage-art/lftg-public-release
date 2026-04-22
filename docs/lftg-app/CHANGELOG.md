LFTG APP CHANGELOG

FORMAT
- DATE
- CHANGE
- IMPACT
- COMMIT

2026-04-21
- Added scripts/release-check.sh for one-command preflight (repo check, required files, compile test, credential-like scan)
- Makes each public release faster and safer with a repeatable automated gate before push
- pending

2026-04-21
- Added PUBLIC-RELEASE-CHECKLIST.md and linked it in TOOLS.md for repeatable pre-push safety and deployment verification
- Reduces accidental public exposure risk and standardizes release QA before every live update
- be0145a

2026-04-21
- Hid Streamlit top chrome in the public app (Fork/menu/header/footer links) using CSS selectors in global theme styling
- Public viewers now see only app content without Streamlit branding controls at the top edge
- aebb905

2026-04-21
- Removed the left sidebar debug panel (Look & Feel, Data Status) from the public app and set initial sidebar state to collapsed
- Public users now land directly in the full app view without the developer-facing side panel
- 6fe765a

2026-03-28
- Added reusable THREAD-STARTER.txt for fast new-thread continuity and correct file targeting
- New threads can bootstrap LFTG context in seconds with canonical docs + paths + run commands
- f87d3ec

2026-03-28
- Added docs governance policy (README) and made changelog updates mandatory per meaningful change
- Keeps durable docs current by default instead of ad hoc updates
- d399f96

2026-03-28
- Created canonical durable doc set under docs/lftg-app (ARCHITECTURE, TOOLS, ROADMAP, CHANGELOG)
- App context and operational knowledge now lives in one stable location outside chat history
- 9e29f01

NOTES
- Existing historical notes remain in:
  - docs/LFTG-APP-CHANGELOG.md
- Going forward, log new LFTG app changes here first.
