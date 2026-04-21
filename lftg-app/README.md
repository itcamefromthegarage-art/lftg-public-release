LFTG APP V1

What this is
- A local Streamlit app to explore LFTG data quickly.
- Search by performer and band.
- See unique show counts, related shows, bands, and roles.
- View top performers and top bands by unique shows.

Data source
- Reads local CSVs from:
  - lftg-data/data/appearances.normalized.csv
  - lftg-data/data/shows.clean.csv
  - lftg-data/data/bands.clean.csv

Before running
1) Sync latest sheet edits to local CSVs:
   python3 lftg-data/sync-from-sheet.py

2) Install dependencies:
   pip3 install -r lftg-app/requirements.txt

Run
- streamlit run lftg-app/app.py

Then open the local URL shown in terminal (usually http://localhost:8501).

V1 features
- Performer tab:
  - select performer
  - unique shows count
  - bands count
  - appearance row count
  - chronological show list
  - band list
  - roles and detailed rows

- Band tab:
  - select band
  - unique shows count
  - unique performer count
  - show list + performer list

- Leaderboards tab:
  - top performers by unique shows
  - top bands by unique shows

Notes
- Counts use unique show logic where appropriate.
- If data changes in Google Sheets, rerun sync command before opening/refeshing app.
