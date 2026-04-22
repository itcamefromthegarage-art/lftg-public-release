#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}PASS${NC} - $1"; }
warn() { echo -e "${YELLOW}WARN${NC} - $1"; }
fail() { echo -e "${RED}FAIL${NC} - $1"; exit 1; }

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "LFTG PUBLIC RELEASE CHECK"
echo "Repo: $ROOT"
echo

if [ ! -d .git ]; then
  fail "Not a git repo. Run this from lftg-public-release."
fi

REMOTE_URL="$(git remote get-url origin 2>/dev/null || true)"
if [[ "$REMOTE_URL" == *"lftg-public-release"* ]]; then
  pass "Origin remote looks correct: $REMOTE_URL"
else
  warn "Origin remote is unusual: $REMOTE_URL"
fi

CHANGED_COUNT="$(git status --porcelain | wc -l | tr -d ' ')"
if [ "$CHANGED_COUNT" -eq 0 ]; then
  pass "Working tree clean"
else
  warn "Working tree has $CHANGED_COUNT changed file(s). Review with: git status"
fi

required_files=(
  "requirements.txt"
  "lftg-app/app.py"
  "lftg-app/requirements.txt"
  "lftg-data/sync-from-sheet.py"
  "lftg-data/sync-video-database.py"
  "lftg-data/data/shows.clean.csv"
  "lftg-data/data/bands.clean.csv"
  "lftg-data/data/appearances.normalized.csv"
  "lftg-data/data/performers.clean.csv"
  "lftg-data/data/setlists.clean.csv"
  "lftg-data/data/videos.clean.csv"
  "docs/lftg-app/CHANGELOG.md"
)

missing=0
for f in "${required_files[@]}"; do
  if [ -f "$f" ]; then
    pass "Required file exists: $f"
  else
    fail "Missing required file: $f"
    missing=1
  fi
done

python3 -m py_compile lftg-app/app.py >/dev/null 2>&1 && pass "Python compile check passed: lftg-app/app.py" || fail "Python compile check failed"

# Sensitive-content scan (higher-signal patterns)
scan_pattern='(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|gho_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----|"(api[_-]?key|token|password|secret)"\s*:\s*"[^"]{8,}|(api[_-]?key|token|password|secret)\s*=\s*[^\s]{8,})'
if rg -n -i --hidden -g '!.git/*' -g '!*.jpg' -g '!*.jpeg' -g '!*.png' -g '!*.webp' -g '!*.gif' -g '!*.mp4' -g '!scripts/release-check.sh' "$scan_pattern" . >/tmp/lftg_sensitive_scan.txt 2>/dev/null; then
  warn "Possible credential-like strings found. Review /tmp/lftg_sensitive_scan.txt before pushing."
else
  pass "No credential-like strings found in text files"
fi

echo
echo "Release check complete."
echo "If all PASS/WARN items look acceptable, proceed with commit and push."
