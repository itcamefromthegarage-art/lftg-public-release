import re
import base64
from pathlib import Path
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="20 ans de Live From The Garage !", page_icon="🎵", layout="wide", initial_sidebar_state="collapsed")

ROOT = Path(__file__).resolve().parents[1]

THEMES = {
    "Vintage Poster": {
        "bg": "#f3ebdc",
        "card": "#fffaf0",
        "text": "#2f2620",
        "accent": "#9b2c2c",
        "muted": "#7a5d4f",
        "hero": "linear-gradient(120deg, #d9b38c 0%, #f2d7b5 100%)",
    },
}
DATA_DIR = ROOT / "lftg-data" / "data"

APPEARANCES_CSV = DATA_DIR / "appearances.normalized.csv"
SHOWS_CSV = DATA_DIR / "shows.clean.csv"
BANDS_CSV = DATA_DIR / "bands.clean.csv"
VIDEOS_CSV = DATA_DIR / "videos.clean.csv"
POSTERS_DIR = Path(__file__).resolve().parent / "assets" / "posters"
BAND_PHOTOS_DIR = Path(__file__).resolve().parent / "assets" / "bands"
THEME_BG_IMAGE = Path(__file__).resolve().parent / "assets" / "theme" / "icftg-bg.jpg"


def show_sort_key(show_label: str):
    m = re.search(r"LFTG\s+([0-9]+(?:\.[0-9]+)?)", str(show_label))
    return float(m.group(1)) if m else 999.0


def _image_data_uri(path: Path):
    if not path.exists():
        return None
    mime = "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def apply_theme(theme_name: str):
    t = THEMES.get(theme_name, THEMES["Vintage Poster"])
    bg_uri = _image_data_uri(THEME_BG_IMAGE)
    bg_css = (
        f"background-image: linear-gradient(rgba(18,8,2,0.62), rgba(18,8,2,0.62)), url('{bg_uri}');"
        "background-size: cover; background-position: center; background-attachment: fixed;"
        if bg_uri
        else f"background: {t['bg']};"
    )
    st.markdown(
        f"""
        <style>
        .stApp {{
            {bg_css}
            color: {t['text']};
        }}
        h1, h2, h3, p, label, span, div {{
            color: #ffffff;
            text-shadow: 0 1px 2px rgba(0,0,0,0.9);
        }}
        .hero-box h1 {{
            color: #ffd84d !important;
            font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif !important;
            letter-spacing: 0.5px;
            text-shadow: 0 2px 0 rgba(0,0,0,0.95), 0 0 10px rgba(0,0,0,0.45);
        }}
        .hero-box .hero-sub {{
            color: #ffd84d !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.9);
        }}
        .hero-box {{
            background: rgba(20,12,8,0.78);
            border: 1px solid {t['accent']};
            border-radius: 14px;
            padding: 18px 22px;
            margin-bottom: 14px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.35);
        }}
        .hero-sub {{ color: #f1d9b2; font-size: 0.95rem; }}
        div[data-testid="stMetric"] {{
            background: rgba(20,12,8,0.72);
            border: 1px solid {t['accent']};
            border-radius: 10px;
            padding: 8px 12px;
        }}
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] div,
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricLabel"] {{
            color: #ffd84d !important;
        }}
        .stDataFrame, [data-testid="stDataFrame"], [data-testid="stTable"] {{
            background: rgba(0,0,0,0.92) !important;
            border: 1px solid #ffd84d55;
            border-radius: 8px;
            --gdg-bg-cell: #000000;
            --gdg-bg-header: #0f0f0f;
            --gdg-bg-header-has-focus: #1a1a1a;
            --gdg-header-font-style: 600 13px;
            --gdg-fg-cell: #ffffff;
            --gdg-fg-header: #ffd84d;
            --gdg-fg-icon-header: #ffd84d;
            --gdg-bg-search-result: #1f1f1f;
            --gdg-bg-search-result-selected: #2a2a2a;
        }}
        [data-testid="stDataFrame"] > div,
        [data-testid="stDataFrame"] [data-testid="stDataFrameResizable"],
        [data-testid="stDataFrame"] [data-testid="stDataFrameGlideDataEditor"],
        [data-testid="stDataFrame"] canvas,
        [data-testid="stDataFrame"] [role="grid"],
        [data-testid="stDataFrame"] [role="row"],
        [data-testid="stDataFrame"] [role="gridcell"],
        [data-testid="stDataFrame"] [role="columnheader"],
        [data-testid="stTable"] > div,
        [data-testid="stTable"] table,
        [data-testid="stTable"] thead,
        [data-testid="stTable"] tbody,
        [data-testid="stTable"] tr,
        [data-testid="stTable"] th,
        [data-testid="stTable"] td {{
            background: rgba(0,0,0,0.92) !important;
        }}
        .stDataFrame * , [data-testid="stDataFrame"] *, [data-testid="stTable"] * {{
            color: #ffffff !important;
            text-shadow: none !important;
        }}
        .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            border: 1px solid {t['accent']};
            padding: 8px 12px;
            background: rgba(20,12,8,0.62);
            color: #ffd84d !important;
        }}
        .stTabs [data-baseweb="tab"] * {{
            color: #ffd84d !important;
        }}

        /* Dropdowns: black backgrounds with white text */
        [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] [data-baseweb="select"] > div,
        [data-testid="stSelectbox"] [data-baseweb="select"] input,
        [data-testid="stMultiSelect"] [data-baseweb="select"] input,
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        ul[role="listbox"],
        div[role="listbox"] {{
            background: rgba(0,0,0,0.92) !important;
            border: 1px solid #ffd84d88 !important;
        }}
        div[data-baseweb="popover"] li,
        div[data-baseweb="popover"] ul,
        div[data-baseweb="popover"] [role="option"],
        ul[role="listbox"] li {{
            background: rgba(0,0,0,0.92) !important;
        }}
        [data-testid="stSelectbox"],
        [data-testid="stSelectbox"] *,
        [data-testid="stMultiSelect"],
        [data-testid="stMultiSelect"] *,
        div[data-baseweb="select"],
        div[data-baseweb="select"] *,
        div[role="listbox"],
        div[role="listbox"] *,
        div[role="option"],
        div[role="option"] * {{
            color: #ffffff !important;
            text-shadow: none !important;
        }}
        div[role="option"]:hover {{
            background: rgba(255,216,77,0.22) !important;
        }}

        /* Hide Streamlit chrome on public app (top bar, menu, footer, badges) */
        header[data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        #MainMenu,
        footer,
        .viewerBadge_container__1QSob,
        .viewerBadge_link__1S137,
        .viewerBadge_text__1JaDK {{
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def poster_for_show(show_id: str):
    if not show_id:
        return None
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        p = POSTERS_DIR / f"{show_id}{ext}"
        if p.exists():
            return p
    return None


def band_photo_for_band_id(band_id: str):
    if not band_id:
        return None
    for ext in [".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"]:
        p = BAND_PHOTOS_DIR / f"{band_id}{ext}"
        if p.exists():
            return p
    return None


def render_poster(poster_path, caption: str):
    # Center posters at ~2/3 content width and trim a tiny outer edge
    _left, center, _right = st.columns([1, 2, 1])
    with center:
        img_b64 = base64.b64encode(Path(poster_path).read_bytes()).decode("utf-8")
        st.markdown(
            f"""
            <div style='text-align:center;'>
              <img src='data:image/jpeg;base64,{img_b64}' style='width:100%; display:block; margin:0 auto; clip-path: inset(0.9% 0.9% 0.9% 0.9%);' />
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_data_table(df: pd.DataFrame, key: str = "", height: int = 460):
    table_html = df.to_html(index=False, escape=True)
    st.markdown(
        f"""
        <div id="tbl_{key}" style="max-height:{height}px; overflow-y:auto; overflow-x:auto; border:1px solid #ffd84d66; border-radius:8px; background:rgba(0,0,0,0.92); padding:0; position:relative;">
          <style>
            #tbl_{key} table {{ width:100%; border-collapse: collapse; background: transparent; margin:0; }}
            #tbl_{key} thead {{ position: sticky; top: 0; z-index: 6; }}
            #tbl_{key} th {{ position: sticky; top: 0; z-index: 7; background:#111; color:#ffd84d; border-bottom:1px solid #ffd84d66; padding:8px; text-align:left; box-shadow: 0 2px 0 #111; }}
            #tbl_{key} td {{ background: transparent; color:#fff; border-bottom:1px solid #333; padding:7px; text-align:left; }}
            #tbl_{key} tr:hover td {{ background:#1b1b1b; }}
            #tbl_{key}::before {{ content:''; position: sticky; top:0; display:block; height:2px; background:#111; z-index:8; }}
          </style>
          {table_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _youtube_embed_url(url: str):
    m = re.search(r"youtu\.be/([A-Za-z0-9_-]{6,})", url)
    if m:
        return f"https://www.youtube.com/embed/{m.group(1)}"
    m = re.search(r"[?&]v=([A-Za-z0-9_-]{6,})", url)
    if m:
        return f"https://www.youtube.com/embed/{m.group(1)}"
    m = re.search(r"youtube\.com/embed/([A-Za-z0-9_-]{6,})", url)
    if m:
        return f"https://www.youtube.com/embed/{m.group(1)}"
    return url


def render_video_player(video_df: pd.DataFrame, key_prefix: str):
    if video_df.empty:
        return

    opts = video_df.copy()
    if "song" in opts.columns and "show_label" in opts.columns:
        opts["video_label"] = opts["show_label"] + " — " + opts["song"]
    else:
        opts["video_label"] = opts.iloc[:, 0].astype(str)

    labels = opts["video_label"].tolist()
    selected_label = st.selectbox("Choisir une vidéo", labels, key=f"video_pick_{key_prefix}")
    selected_row = opts.loc[opts["video_label"] == selected_label].iloc[0]
    selected_url = selected_row.get("url", "")
    if selected_url:
        embed_url = _youtube_embed_url(selected_url)
        iframe_html = f'''
        <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;">
          <iframe src="{embed_url}" 
                  style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowfullscreen>
          </iframe>
        </div>
        '''
        _left, center, _right = st.columns([1, 4, 1])
        with center:
            components.html(iframe_html, height=700)
        st.link_button("Regarder sur YouTube", selected_url)
        st.caption("Si l’intégration est indisponible, ouvrez directement sur YouTube.")


def get_query_param(name: str):
    try:
        return st.query_params.get(name)
    except Exception:
        qp = st.experimental_get_query_params()
        v = qp.get(name)
        if isinstance(v, list):
            return v[0] if v else None
        return v


@st.cache_data(show_spinner=False)
def load_data():
    appearances = pd.read_csv(APPEARANCES_CSV)
    shows = pd.read_csv(SHOWS_CSV)
    bands = pd.read_csv(BANDS_CSV)
    videos = pd.read_csv(VIDEOS_CSV) if VIDEOS_CSV.exists() else pd.DataFrame(columns=["show_id", "show_label", "band_id", "song", "url"])

    # Defensive cleanup
    for col in ["performer_name", "band_name", "show_label", "roles", "show_id", "band_id"]:
        if col in appearances.columns:
            appearances[col] = appearances[col].fillna("").astype(str).str.strip()

    if "show_label" in shows.columns:
        shows["show_label"] = shows["show_label"].fillna("").astype(str).str.strip()

    for col in ["show_id", "show_label", "band_id", "song", "url"]:
        if col in videos.columns:
            videos[col] = videos[col].fillna("").astype(str).str.strip()

    return appearances, shows, bands, videos


def render_performer_profile(appearances: pd.DataFrame, videos: pd.DataFrame, performer: str, key_prefix: str = "perf"):
    df = appearances[appearances["performer_name"] == performer].copy()
    if df.empty:
        st.info("Aucune donnée trouvée pour cet artiste.")
        return

    df["show_order"] = df["show_label"].apply(show_sort_key)

    unique_shows = sorted(df["show_label"].unique().tolist(), key=show_sort_key)
    unique_bands = sorted(df["band_name"].unique().tolist(), key=lambda x: x.casefold())
    c1, c2 = st.columns(2)
    c1.metric("Spectacles uniques", len(unique_shows))
    c2.metric("Groupes distincts", len(unique_bands))

    st.markdown("PHOTO DU GROUPE")
    band_opts = df[["band_name", "show_label", "band_id"]].drop_duplicates().copy()
    band_opts["show_order"] = band_opts["show_label"].apply(show_sort_key)
    band_opts = band_opts.sort_values(["show_order", "show_label", "band_name"])
    band_opts["band_show_label"] = band_opts["show_label"] + " — " + band_opts["band_name"]

    selected_band_show = st.selectbox(
        "Choisir une photo du groupe",
        band_opts["band_show_label"].tolist(),
        key=f"band_photo_{key_prefix}_{performer}",
    )
    selected_row = band_opts.loc[band_opts["band_show_label"] == selected_band_show].iloc[0]
    selected_band_id = selected_row["band_id"]
    selected_band_name = selected_row["band_name"]
    selected_show_label = selected_row["show_label"]

    band_photo = band_photo_for_band_id(selected_band_id)
    if band_photo:
        render_poster(band_photo, f"{selected_band_name} • {selected_show_label} • {selected_band_id}")
    else:
        st.caption(f"Aucune photo de groupe trouvée pour {selected_band_id}")
    st.markdown("DÉTAIL")
    detail = (
        df.sort_values(by=["show_order", "band_name"])  # chronological then band
        [["show_label", "band_name"]]
        .rename(columns={"show_label": "Spectacle", "band_name": "Groupe"})
        .reset_index(drop=True)
    )
    render_data_table(detail, key=f"perf_detail_{key_prefix}", height=420)

    # Keep player only (no full video data table)
    perf_videos = videos[videos["band_id"].isin(df["band_id"].unique())]
    if not perf_videos.empty:
        st.markdown("LECTEUR VIDÉO")
        player_view = perf_videos[["show_label", "song", "url"]].drop_duplicates().copy()
        player_view["_order"] = player_view["show_label"].apply(show_sort_key)
        player_view = player_view.sort_values(["_order", "show_label", "song"]).drop(columns=["_order"])
        render_video_player(player_view, key_prefix=f"perf_{key_prefix}_{performer}")



def performer_view(appearances: pd.DataFrame, videos: pd.DataFrame):
    st.subheader("Recherche d’artiste")

    all_performers = sorted(
        [p for p in appearances["performer_name"].dropna().unique().tolist() if str(p).strip()],
        key=lambda x: x.casefold(),
    )

    options = [""] + all_performers
    performer = st.selectbox("Choisir un artiste", options, index=0, key="performer_select")
    if not performer:
        st.info("Choisissez un artiste pour voir les statistiques.")
        return

    render_performer_profile(appearances, videos, performer, key_prefix="perf")


def render_band_profile(appearances: pd.DataFrame, videos: pd.DataFrame, band: str, key_prefix: str = "band"):
    df = appearances[appearances["band_name"] == band].copy()
    if df.empty:
        st.info("Aucune donnée trouvée pour ce groupe.")
        return

    df["show_order"] = df["show_label"].apply(show_sort_key)

    # Match performer-page style: metrics -> photo -> detail -> video player
    unique_shows = sorted(df["show_label"].unique().tolist(), key=show_sort_key)
    unique_performers = sorted(df["performer_name"].unique().tolist(), key=lambda x: x.casefold())

    c1, c2 = st.columns(2)
    c1.metric("Spectacles uniques", len(unique_shows))
    c2.metric("Artistes uniques", len(unique_performers))

    st.markdown("PHOTO DU GROUPE")
    band_photo_opts = df[["show_label", "band_id"]].drop_duplicates().copy()
    band_photo_opts["show_order"] = band_photo_opts["show_label"].apply(show_sort_key)
    band_photo_opts = band_photo_opts.sort_values(["show_order", "show_label", "band_id"])
    band_photo_opts["band_photo_label"] = band_photo_opts["show_label"] + " • " + band_photo_opts["band_id"]

    selected_band_photo_label = st.selectbox(
        "Choisir une photo du groupe",
        band_photo_opts["band_photo_label"].tolist(),
        key=f"band_photo_pick_{key_prefix}_{band}",
    )
    selected_band_row = band_photo_opts.loc[band_photo_opts["band_photo_label"] == selected_band_photo_label].iloc[0]
    band_id = selected_band_row["band_id"]

    band_photo = band_photo_for_band_id(band_id)
    if band_photo:
        render_poster(band_photo, f"{band} • {band_id}")
    else:
        st.caption(f"Aucune photo de groupe trouvée pour {band_id}")
    st.markdown("DÉTAIL")
    detail = df[["show_label", "performer_name"]].copy()
    detail["_order"] = detail["show_label"].apply(show_sort_key)
    detail = (
        detail.sort_values(by=["_order", "show_label", "performer_name"], ascending=[True, True, True])
        .drop(columns=["_order"])
        .rename(columns={"show_label": "Spectacle", "performer_name": "Artiste"})
        .reset_index(drop=True)
    )
    render_data_table(detail, key=f"band_detail_{key_prefix}", height=420)

    band_videos = videos[videos["band_id"].isin(df["band_id"].unique())]
    if not band_videos.empty:
        st.markdown("LECTEUR VIDÉO")
        player_view = band_videos[["show_label", "song", "url"]].drop_duplicates().sort_values(["show_label", "song"])
        render_video_player(player_view, key_prefix=f"band_{key_prefix}_{band}")


def band_view(appearances: pd.DataFrame, videos: pd.DataFrame):
    st.subheader("Recherche de groupe")
    all_bands = sorted(
        [b for b in appearances["band_name"].dropna().unique().tolist() if str(b).strip()],
        key=lambda x: x.casefold(),
    )

    options = [""] + all_bands
    band = st.selectbox("Choisir un groupe", options, index=0, key="band_select")
    if not band:
        st.info("Choisissez un groupe pour voir la formation et l’historique.")
        return

    render_band_profile(appearances, videos, band, key_prefix="band")


def leaderboard_view(appearances: pd.DataFrame, videos: pd.DataFrame):
    st.subheader("Classements")

    total_shows = appearances[["show_id"]].drop_duplicates().shape[0]
    total_bands = appearances[["band_id"]].drop_duplicates().shape[0]
    total_performers = appearances[["performer_name"]].drop_duplicates().shape[0]

    m1, m2, m3 = st.columns(3)
    m1.metric("Total des spectacles", total_shows)
    m2.metric("Total des groupes", total_bands)
    m3.metric("Total des artistes", total_performers)

    # Performer leaderboard by unique show participation
    perf_show = (
        appearances[["performer_name", "show_id", "show_label"]]
        .drop_duplicates()
        .groupby("performer_name", as_index=False)
        .agg(show_count=("show_id", "count"))
        .sort_values(by=["show_count", "performer_name"], ascending=[False, True])
    )

    # Band leaderboard by unique show count
    band_show = (
        appearances[["band_name", "show_id", "show_label"]]
        .drop_duplicates()
        .groupby("band_name", as_index=False)
        .agg(show_count=("show_id", "count"))
        .sort_values(by=["show_count", "band_name"], ascending=[False, True])
    )

    _left, c1, c2, _right = st.columns([1, 3, 3, 1])
    with c1:
        st.markdown("MEILLEURS ARTISTES (PAR SPECTACLES UNIQUES)")
        perf_view = perf_show.head(40).rename(columns={"performer_name": "Artiste", "show_count": "Spectacles"})
        perf_view["Spectacles"] = perf_view["Spectacles"].astype(str)
        render_data_table(perf_view, key="lb_perf", height=700)

    with c2:
        st.markdown("MEILLEURS GROUPES (PAR SPECTACLES UNIQUES)")
        band_view = band_show.head(40).rename(columns={"band_name": "Groupe", "show_count": "Spectacles"})
        band_view["Spectacles"] = band_view["Spectacles"].astype(str)
        render_data_table(band_view, key="lb_band", height=700)

    if not videos.empty and "song" in videos.columns:
        vid = videos.copy()
        # Parse "Song by Artist" pattern
        parsed = vid["song"].str.extract(r"^(?P<song_title>.*?)\s+by\s+(?P<artist>.*)$", expand=True)
        vid["song_title"] = parsed["song_title"].fillna(vid["song"]).str.strip()
        vid["artist"] = parsed["artist"].fillna("").str.strip()

        top_songs = (
            vid[vid["song_title"] != ""]
            .groupby("song_title", as_index=False)
            .size()
            .rename(columns={"song_title": "Chanson", "size": "Nombre"})
            .sort_values(["Nombre", "Chanson"], ascending=[False, True])
            .head(10)
        )

        top_artists = (
            vid[vid["artist"] != ""]
            .groupby("artist", as_index=False)
            .size()
            .rename(columns={"artist": "Artiste", "size": "Nombre"})
            .sort_values(["Nombre", "Artiste"], ascending=[False, True])
            .head(10)
        )

        _l2, s1, s2, _r2 = st.columns([1, 3, 3, 1])
        with s1:
            st.markdown("TOP 10 CHANSONS INTERPRÉTÉES")
            render_data_table(top_songs, key="top_songs", height=360)
        with s2:
            st.markdown("TOP 10 ARTISTES/GROUPES REPRIS")
            render_data_table(top_artists, key="top_artists", height=360)


def what_is_lftg_view():
    st.subheader("Qu’est-ce que LFTG ?")

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Libre+Baskerville:wght@400;700&display=swap');
        .lftg-article {
            max-width: 940px;
            margin: 0 auto 1.4rem auto;
            background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(252,247,239,0.95) 100%);
            border: 1px solid #2b1d16;
            border-left: 6px solid #9b2c2c;
            border-radius: 8px;
            padding: 1.35rem 1.55rem 1.15rem 1.55rem;
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }
        .lftg-title {
            font-family: 'Oswald', Arial, sans-serif;
            font-size: 2.25rem;
            letter-spacing: 1.2px;
            line-height: 1.05;
            margin: 0 0 0.8rem 0;
            color: #111;
            text-transform: uppercase;
            border-bottom: 3px solid #9b2c2c;
            padding-bottom: 0.3rem;
        }
        .lftg-text {
            font-family: 'Libre Baskerville', Georgia, serif;
            font-size: 1.03rem;
            line-height: 1.78;
            text-align: justify;
            text-justify: inter-word;
            color: #1f1b18;
            margin: 0.55rem 0;
        }
        .lftg-text.lead::first-letter {
            font-family: 'Oswald', Arial, sans-serif;
            float: left;
            font-size: 3.4rem;
            line-height: 0.9;
            margin: 0.15rem 0.42rem 0 0;
            color: #9b2c2c;
        }
        .lftg-break {
            max-width: 940px;
            margin: 0.25rem auto 1.05rem auto;
            border-top: 1px solid #231711;
            border-bottom: 2px solid #9b2c2c;
            height: 6px;
            opacity: 0.85;
        }
        .teachers-frame {
            max-width: 940px;
            margin: 0.3rem auto 1.1rem auto;
            border: 1px solid #2b1d16;
            border-radius: 8px;
            background: rgba(0,0,0,0.62);
            padding: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.22);
        }
        .teachers-row {
            width: 100%;
        }
        .teachers-row-top {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
        }
        .teachers-row-bottom {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            width: 66.5%;
            margin: 12px auto 0 auto;
        }
        .teacher-card {
            border: 1px solid #2b1d16;
            border-radius: 6px;
            overflow: hidden;
            background: transparent;
        }
        .teacher-photo {
            width: 100%;
            aspect-ratio: 954 / 838;
            object-fit: cover;
            object-position: center;
            display: block;
            background: transparent;
        }
        .teacher-name {
            font-family: 'Oswald', Arial, sans-serif;
            font-size: 0.84rem;
            letter-spacing: 0.3px;
            text-align: center;
            padding: 6px 4px 7px 4px;
            color: #2b1d16;
            background: rgba(255,255,255,0.7);
            border-top: 1px solid #2b1d16;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    story_dir = Path(__file__).resolve().parent / "assets" / "what-is-lftg-final"

    image_sequence = [
        ("IMG_0068.JPG", "Les débuts"),
        ("Lftg23.jpg", "Live From The Garage — ère moderne"),
        ("IMG_3736.JPG", "Répétitions Rock Band et préparation de scène"),
        ("it came from the garage tristans frist show 019.jpg", "Grandir grâce à la scène"),
        ("IMG_2555.JPG", "LFTG à travers les années"),
        ("energy_momentum_3x2.jpg", "Sur scène, en temps réel"),
        ("IMG_6993.JPG", "Énergie et élan"),
        ("individual_growth_3x2.jpg", "Un vrai moment de déclic"),
        ("community_continuity_3x2.jpg", "Communauté et continuité"),
    ]

    teachers_dir = Path(__file__).resolve().parent / "assets" / "ndgms-teachers"
    teachers_sequence = ["Jay.jpg", "Jon.jpg", "Mike.jpg", "Jorge.jpg", "Carly.jpg"]
    teacher_names = {
        "Jon.jpg": "Jonathan Stein",
        "Carly.jpg": "Carly Leblanc",
        "Mike.jpg": "Mike Fitch",
        "Jay.jpg": "Jay Blumenstein",
        "Jorge.jpg": "Jorge Flores",
    }

    def show_story_image(index: int):
        if 0 <= index < len(image_sequence):
            fname, caption = image_sequence[index]
            p = story_dir / fname
            if p.exists():
                # Scale all story photos to ~1.25x the original first-photo layout width
                _left, center, _right = st.columns([1.4, 2.25, 1.4])
                with center:
                    with st.container(border=True):
                        img_b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
                        if index in [6, 7, 8]:
                            width_style = "700px"
                        elif index == 5:
                            width_style = "760px"
                        else:
                            width_style = "100%"

                        st.markdown(
                            f"""
                            <div style='text-align:center;'>
                              <img src='data:image/jpeg;base64,{img_b64}' style='width:{width_style}; max-width:100%; height:auto; display:block; margin:0 auto; border:8px solid #000;' />
                              <div style='font-size:0.82rem; color:#ffffff; text-shadow:0 1px 2px rgba(0,0,0,0.9); margin-top:0.35rem;'>{caption}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

    def show_teachers_row():
        cards = []
        for name in teachers_sequence:
            p = teachers_dir / name
            if not p.exists():
                continue
            img_b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
            display_name = teacher_names.get(name, name.rsplit('.', 1)[0])
            cards.append(f'<div class="teacher-card"><img class="teacher-photo" src="data:image/jpeg;base64,{img_b64}" alt="{display_name}"/><div class="teacher-name">{display_name}</div></div>')
        if cards:
            top = "".join(cards[:3])
            bottom = "".join(cards[3:5])
            st.markdown(
                f'<div class="teachers-frame"><div class="teachers-row"><div class="teachers-row-top">{top}</div><div class="teachers-row-bottom">{bottom}</div></div><div style="text-align:center; color:#f1d9b2; font-size:0.88rem; margin-top:6px;">Enseignement et mentorat — NDG Music School</div></div>',
                unsafe_allow_html=True,
            )

    def story_block(paragraphs, title=None, lead=False):
        html = ['<div class="lftg-article">']
        if title:
            html.append(f'<div class="lftg-title">{title}</div>')
        for i, p in enumerate(paragraphs):
            klass = "lftg-text"
            if lead and i == 0:
                klass += " lead"
            html.append(f'<p class="{klass}">{p}</p>')
        html.append('</div><div class="lftg-break"></div>')
        st.markdown("".join(html), unsafe_allow_html=True)

    show_story_image(0)

    story_block(
        [
            "Quand j’ai commencé la musique, ce que je voulais avant tout, c’était jouer avec d’autres et monter un groupe.",
            "Pratiquer seul à la maison, c’était important, mais pour moi, ça a toujours été un moyen, pas une fin. Le vrai plaisir commençait quand je jouais avec d’autres.",
        ],
        title="Qu’est-ce que Live From The Garage ?",
        lead=True,
    )

    show_story_image(1)

    story_block(
        [
            "Live From The Garage est né d’une idée simple. Je voulais que les élèves aient un espace pour faire plus que pratiquer seuls. Les cours sont importants, bien sûr, mais il y a un autre niveau qui apparaît seulement quand on joue avec d’autres, qu’on trouve le groove, qu’on écoute, qu’on s’ajuste et qu’on apprend à faire vivre une chanson du début à la fin en groupe.",
            "C’est le cœur de LFTG.",
            "Au fil des ans, c’est devenu une série de spectacles qui dure, liée au programme Rock Band de l’École de musique NDG. Les élèves répètent en groupe, travaillent les arrangements, apprennent leurs parties, s’entraident et montent sur scène.",
        ],
    )

    show_story_image(2)

    story_block(
        [
            "La scène, c’est là que tout change.",
            "Quand on joue devant du monde, tout devient réel. On apprend à se relever après les erreurs. On apprend à rester calme quand le stress monte. On apprend à mieux écouter et à faire confiance aux personnes à côté de soi. On commence à comprendre que la musicalité, ce n’est pas seulement la technique. C’est le timing, la communication, le ressenti et la présence.",
            "Certains des meilleurs moments sont ceux que personne ne peut planifier.",
            "Un élève timide prend un solo et surprend tout le monde. Un chanteur trouve sa voix devant le public. Un groupe qui peinait en répétition se met soudainement à cliquer sur scène. Parents, amis, enseignants et membres de la communauté ressentent tous cette énergie dans la salle.",
            "Ce sont ces moments dont on se souvient.",
        ],
    )

    show_story_image(3)
    show_story_image(4)

    story_block(
        [
            "LFTG a aussi toujours été une histoire de communauté. Ça réunit élèves, enseignants, familles, amis et passionnés de musique du quartier autour de quelque chose de vrai et de partagé. Il ne s’agit pas de perfection. Il s’agit de progression, de connexion et de l’expérience de faire de la musique ensemble.",
            "Pour l’École de musique NDG, Live From The Garage est une partie essentielle de notre identité. Notre programme Rock Band est construit autour de la pratique musicale réelle. Nous voulons que les élèves apprennent la musique d’une façon qui reflète ce qui se passe vraiment dans les groupes et sur scène. LFTG, c’est là que cet apprentissage prend vie.",
        ],
    )

    show_story_image(5)
    show_story_image(6)

    story_block(
        [
            "Vingt ans plus tard, je suis encore porté par la même chose qui a lancé tout ça : voir des musiciens grandir quand ils jouent ensemble.",
            "C’est ça, Live From The Garage.",
            "Jon",
        ],
    )

    show_story_image(7)
    show_teachers_row()
    show_story_image(8)


def show_explorer_view(appearances: pd.DataFrame, videos: pd.DataFrame):
    st.subheader("Explorateur de spectacles")

    show_df = appearances[["show_id", "show_label"]].drop_duplicates().copy()
    show_df["show_order"] = show_df["show_label"].apply(show_sort_key)
    show_df = show_df.sort_values("show_order")
    show_labels = show_df["show_label"].tolist()

    if "show_explorer_selected" not in st.session_state and show_labels:
        st.session_state["show_explorer_selected"] = show_labels[0]

    selected_label = st.session_state.get("show_explorer_selected", show_labels[0] if show_labels else "")
    selected_id = show_df.loc[show_df["show_label"] == selected_label, "show_id"].iloc[0]

    df = appearances[appearances["show_id"] == selected_id].copy()
    bands = sorted(df["band_name"].dropna().unique().tolist(), key=lambda x: x.casefold())
    performers = sorted(df["performer_name"].dropna().unique().tolist(), key=lambda x: x.casefold())

    # Large dynamic show heading
    import re
    m = re.search(r"LFTG\s+([0-9]+(?:\.[0-9]+)?)", selected_label)
    show_num = m.group(1) if m else selected_label
    st.markdown(f"## Live From The Garage {show_num}")

    # Metrics first (requested)
    c1, c2 = st.columns(2)
    c1.metric("Groupes", len(bands))
    c2.metric("Artistes", len(performers))

    st.selectbox("Choisir un spectacle", show_labels, key="show_explorer_selected")

    poster = poster_for_show(selected_id)
    if poster:
        render_poster(poster, f"{selected_label} • {selected_id}")
    else:
        st.caption(f"Aucune affiche trouvée pour {selected_id}")

    st.markdown("GROUPES")
    render_data_table(pd.DataFrame({"Groupe": bands}), key=f"show_bands_{selected_id}", height=260)

    st.markdown("PHOTO DU GROUPE")
    band_opts = df[["band_name", "band_id"]].drop_duplicates().sort_values("band_name")
    band_opts["band_option"] = band_opts["band_name"] + " • " + band_opts["band_id"]

    options = band_opts["band_option"].tolist()
    default_index = 0
    # Custom default for LFTG 1: prefer Warped Verdict photo first
    if selected_id == "lftg-1-2006":
        for i, opt in enumerate(options):
            if "warped-verdict" in opt:
                default_index = i
                break

    selected_band_option = st.selectbox(
        "Choisir une photo du groupe",
        options,
        index=default_index,
        key=f"show_band_photo_{selected_id}",
    )
    selected_row = band_opts.loc[band_opts["band_option"] == selected_band_option].iloc[0]
    selected_band_name = selected_row["band_name"]
    selected_band_id = selected_row["band_id"]
    band_photo = band_photo_for_band_id(selected_band_id)
    if band_photo:
        render_poster(band_photo, f"{selected_band_name} • {selected_band_id}")
    else:
        st.caption(f"Aucune photo de groupe trouvée pour {selected_band_id}")

    st.markdown("ARTISTES")
    render_data_table(pd.DataFrame({"Artiste": performers}), key=f"show_performers_{selected_id}", height=360)

    show_videos = videos[videos["show_id"] == selected_id]
    if not show_videos.empty:
        st.markdown("LECTEUR VIDÉO")
        player_df = show_videos[["show_label", "song", "url"]].drop_duplicates().sort_values(["show_label", "song"])
        render_video_player(player_df, key_prefix=f"show_{selected_id}")


def main():
    apply_theme("Vintage Poster")

    st.markdown(
        """
        <div class="hero-box">
            <h1 style="margin:0;">20 ans de Live From The Garage !</h1>
            <div class="hero-sub">Explorateur d’archives • Recherche d’artiste • Recherche de groupe • Affiches</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not APPEARANCES_CSV.exists() or not SHOWS_CSV.exists() or not BANDS_CSV.exists():
        st.error("Fichiers de données introuvables. Lancez d’abord la synchronisation : python3 lftg-data/sync-from-sheet.py")
        return

    appearances, shows, bands, videos = load_data()

    _, tabs_row_right = st.columns([5, 2])
    with tabs_row_right:
        st.markdown(
            """
            <div style="display:flex; justify-content:flex-end; align-items:center; margin-top:6px; margin-bottom:-44px; position:relative; z-index:5;">
                <a href="https://ndgmusicschool.com/fr/" target="_self" style="
                    display:inline-block;
                    text-decoration:none;
                    border-radius:8px;
                    border:1px solid #9b2c2c;
                    padding:8px 12px;
                    background: rgba(20,12,8,0.62);
                    color:#ffd84d;
                    font-weight:600;
                    text-align:center;
                    width:50%;
                    min-width:180px;
                ">Retour au site de NDG Music School</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Explorateur de spectacles", "Artiste", "Groupe", "Classements", "Qu’est-ce que LFTG ?"])
    with tab1:
        show_explorer_view(appearances, videos)
    with tab2:
        performer_view(appearances, videos)
    with tab3:
        band_view(appearances, videos)
    with tab4:
        leaderboard_view(appearances, videos)
    with tab5:
        what_is_lftg_view()


if __name__ == "__main__":
    main()
