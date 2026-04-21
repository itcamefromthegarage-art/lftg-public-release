#!/usr/bin/env python3
import csv
import json
import subprocess
from pathlib import Path

VIDEO_SHEET_ID = "1Rvrx2sm5JGlVJUEq_Z-L7zfTFDAxPBU3bUZwHHL_zQw"
ROOT = Path('/Users/ndgms/.openclaw/workspace')
DATA_DIR = ROOT / 'lftg-data' / 'data'
OUT = DATA_DIR / 'videos.clean.csv'
BANDS_CSV = DATA_DIR / 'bands.clean.csv'

DATA_DIR.mkdir(parents=True, exist_ok=True)


def gog_get(range_a1: str):
    out = subprocess.check_output([
        'gog', 'sheets', 'get', VIDEO_SHEET_ID, range_a1, '--json', '--no-input'
    ])
    return json.loads(out.decode('utf-8')).get('values', [])


# Build known show_id prefixes from bands.clean.csv for robust parsing
show_ids = set()
if BANDS_CSV.exists():
    with BANDS_CSV.open(encoding='utf-8') as f:
        for r in csv.DictReader(f):
            sid = (r.get('show_id') or '').strip()
            if sid:
                show_ids.add(sid)

show_ids_sorted = sorted(show_ids, key=len, reverse=True)


def infer_show_id(band_id: str, show_label: str):
    b = (band_id or '').strip()
    if b:
        for sid in show_ids_sorted:
            if b.startswith(sid + '-') or b == sid:
                return sid

    # fallback by show label parsing
    import re
    m = re.search(r'LFTG\s+([0-9]+(?:\.[0-9]+)?)\s*\((\d{4})\)', show_label or '')
    if m:
        num = m.group(1).replace('.', '-')
        year = m.group(2)
        return f'lftg-{num}-{year}'
    return ''


rows = gog_get('Sheet1!A:Z')
if not rows:
    raise SystemExit('Video sheet is empty')

header = [h.strip() for h in rows[0]]
idx = {h: i for i, h in enumerate(header)}

required = ['show_label', 'Band', 'Song', 'url']
for col in required:
    if col not in idx:
        raise SystemExit(f'Missing required column in video sheet: {col}')

out_rows = []
for r in rows[1:]:
    rr = r + [''] * (len(header) - len(r))
    show_label = rr[idx['show_label']].strip()
    band_id = rr[idx['Band']].strip()
    song = rr[idx['Song']].strip()
    url = rr[idx['url']].strip()

    if not (show_label or band_id or song or url):
        continue

    show_id = infer_show_id(band_id, show_label)
    out_rows.append({
        'show_id': show_id,
        'show_label': show_label,
        'band_id': band_id,
        'song': song,
        'url': url,
    })

with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['show_id', 'show_label', 'band_id', 'song', 'url'])
    w.writeheader()
    w.writerows(out_rows)

print(f'Wrote {len(out_rows)} rows to {OUT}')
