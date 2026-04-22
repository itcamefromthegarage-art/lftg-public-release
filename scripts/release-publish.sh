#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

pass() { echo -e "${GREEN}PASS${NC} - $1"; }
warn() { echo -e "${YELLOW}WARN${NC} - $1"; }
fail() { echo -e "${RED}FAIL${NC} - $1"; exit 1; }

usage() {
  cat <<EOF
LFTG RELEASE PUBLISH SCRIPT

Usage:
  ./scripts/release-publish.sh [options]

Options:
  --sync            Run both data sync scripts before checks.
  -m "message"      Commit message (non-interactive mode).
  --yes             Skip push confirmation prompt.
  -h, --help        Show this help.

Examples:
  ./scripts/release-publish.sh --sync
  ./scripts/release-publish.sh --sync -m "Update April 2026 LFTG data" --yes
EOF
}

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DO_SYNC=0
ASSUME_YES=0
COMMIT_MSG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --sync)
      DO_SYNC=1
      shift
      ;;
    -m)
      COMMIT_MSG="${2:-}"
      if [[ -z "$COMMIT_MSG" ]]; then
        fail "-m requires a commit message"
      fi
      shift 2
      ;;
    --yes)
      ASSUME_YES=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "Unknown option: $1 (use --help)"
      ;;
  esac
done

echo "LFTG RELEASE PUBLISH"
echo "Repo: $ROOT"

if [[ ! -d .git ]]; then
  fail "Not a git repository. Expected lftg-public-release root."
fi

if [[ $DO_SYNC -eq 1 ]]; then
  echo
  echo "Running data sync..."
  python3 lftg-data/sync-from-sheet.py
  python3 lftg-data/sync-video-database.py
  pass "Data sync complete"
fi

echo
echo "Running preflight checks..."
./scripts/release-check.sh

if [[ -z "$(git status --porcelain)" ]]; then
  warn "No file changes detected. Nothing to commit/push."
  exit 0
fi

if [[ -z "$COMMIT_MSG" ]]; then
  if [[ -t 0 ]]; then
    echo
    read -r -p "Enter commit message: " COMMIT_MSG
  fi
fi

if [[ -z "$COMMIT_MSG" ]]; then
  fail "Commit message is required. Use -m \"message\" or run interactively."
fi

echo
echo "Committing changes..."
git add -A
git commit -m "$COMMIT_MSG"

if [[ $ASSUME_YES -eq 1 ]]; then
  DO_PUSH="y"
else
  if [[ -t 0 ]]; then
    echo
    read -r -p "Push to origin/main now? [y/N]: " DO_PUSH
  else
    DO_PUSH="n"
  fi
fi

if [[ "${DO_PUSH,,}" == "y" || "${DO_PUSH,,}" == "yes" ]]; then
  git push origin main
  pass "Pushed to origin/main"
else
  warn "Commit created locally but not pushed. Run: git push origin main"
fi

echo
pass "Release publish flow complete"
