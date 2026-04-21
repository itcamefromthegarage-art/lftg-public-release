LFTG APP DOCS GOVERNANCE

PURPOSE
- Keep durable docs current as changes happen.
- Prevent knowledge from living only in chat history.

CANONICAL FILES
- ARCHITECTURE.md = structure, data model, major design conventions
- TOOLS.md = runbook, commands, operational procedures
- ROADMAP.md = planned work and priority buckets
- CHANGELOG.md = chronological record of meaningful changes

UPDATE RULE (DEFAULT)
- Any meaningful app/data/UX change must include:
  - code/data commit
  - CHANGELOG.md entry in same working session

WHEN TO UPDATE EACH FILE
- Update ARCHITECTURE.md when:
  - app sections change
  - data flow changes
  - storage model changes
- Update TOOLS.md when:
  - commands change
  - restart/sync/recovery process changes
- Update ROADMAP.md when:
  - priorities or sequencing changes
  - a NEXT item is completed or replaced
- Update CHANGELOG.md when:
  - any user-visible or operationally meaningful change ships

COMMIT DISCIPLINE
- Prefer one of these patterns:
  1) Single commit containing code + docs update
  2) Two commits in sequence:
     - commit A: code change
     - commit B: docs sync

MINIMUM CHANGELOG ENTRY FORMAT
- DATE
- CHANGE
- IMPACT
- COMMIT

QUALITY BAR
- If a future session asks "what changed?" the answer should be in CHANGELOG.md without searching chat.
