#!/usr/bin/env python3
import csv
import json
import subprocess
from pathlib import Path

SHEET_ID = "1J0ek4EMkzbF-SioEiuIIAKryJt_EyUo1fJj5Dc1S6cc"
ROOT = Path('/Users/ndgms/.openclaw/workspace/lftg-data')
DATA = ROOT / 'data'
DATA.mkdir(parents=True, exist_ok=True)

# Sheet tab -> local csv path
TAB_MAP = {
    'Shows': DATA / 'shows.clean.csv',
    'Bands': DATA / 'bands.clean.csv',
    'Appearances': DATA / 'appearances.normalized.csv',
    'Performers': DATA / 'performers.clean.csv',
    'Setlists': DATA / 'setlists.clean.csv',
}


def gog_get(range_a1: str):
    out = subprocess.check_output([
        'gog', 'sheets', 'get', SHEET_ID, range_a1, '--json', '--no-input'
    ])
    return json.loads(out.decode('utf-8')).get('values', [])


def write_csv(path: Path, rows):
    if not rows:
        path.write_text('', encoding='utf-8')
        return

    header = rows[0]
    width = len(header)

    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows[1:]:
            rr = list(r) + [''] * max(0, width - len(r))
            w.writerow(rr[:width])


def main():
    counts = {}
    for tab, out_path in TAB_MAP.items():
        rows = gog_get(f'{tab}!A:ZZ')
        write_csv(out_path, rows)
        counts[tab] = max(0, len(rows) - 1)

    print('Synced from Google Sheet (sheet-first mode):')
    for tab, n in counts.items():
        print(f'- {tab}: {n} rows')


if __name__ == '__main__':
    main()
