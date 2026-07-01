import base64
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "DATA CURAH HUJAN KMP1(4).xlsx"
LOGO_FILE = APP_DIR / "assets" / "karyamas_logo.jpg"

EMBEDDED_LOGO_DATA_URI = "data:image/jpeg;base64,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"

try:
    _page_icon = Image.open(LOGO_FILE) if LOGO_FILE.exists() else "🌴"
except Exception:
    _page_icon = "🌴"

st.set_page_config(
    page_title="Dashboard Curah Hujan KMP1 - KARYAMAS PLANTATION",
    page_icon=_page_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)

MONTH_ORDER = ["April", "Mei", "Juni"]
MONTH_MAP = {4: "April", 5: "Mei", 6: "Juni"}
MONTH_NO = {m: i for i, m in enumerate(MONTH_ORDER, start=1)}
WEEK_ORDER = ["W1", "W2", "W3", "W4"]
WEEK_PERIODS = [f"{m}-{w}" for m in MONTH_ORDER for w in WEEK_ORDER]
PIE_COLORS = {"Hari Hujan": "#2563eb", "Tidak Hujan": "#f59e0b"}


def image_to_data_uri(path: Path) -> str:
    """Return data URI for image; safely fallback to embedded company logo if file is missing."""
    try:
        if path.exists():
            mime = "image/jpeg" if path.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
            return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("utf-8")
    except Exception:
        pass
    return EMBEDDED_LOGO_DATA_URI


def palm_background_uri() -> str:
    svg = """
    <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 900'>
      <defs>
        <linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'>
          <stop offset='0' stop-color='#02070b'/><stop offset='.5' stop-color='#061a16'/><stop offset='1' stop-color='#03100d'/>
        </linearGradient>
        <radialGradient id='glow' cx='.55' cy='.15' r='.65'>
          <stop offset='0' stop-color='#0ea5a6' stop-opacity='.30'/><stop offset='1' stop-color='#02070b' stop-opacity='0'/>
        </radialGradient>
      </defs>
      <rect width='1600' height='900' fill='url(#bg)'/>
      <rect width='1600' height='900' fill='url(#glow)'/>
      <g opacity='.20' fill='none' stroke='#22c55e' stroke-width='11' stroke-linecap='round'>
        <path d='M1370 900 C1300 630 1325 405 1450 180'/>
        <path d='M1450 180 C1340 210 1240 270 1160 370'/>
        <path d='M1450 180 C1375 95 1265 70 1130 90'/>
        <path d='M1450 180 C1510 70 1600 20 1700 0'/>
        <path d='M1450 180 C1545 180 1620 230 1685 320'/>
        <path d='M1450 180 C1435 85 1465 20 1535 -35'/>
        <path d='M160 920 C115 665 155 485 275 310'/>
        <path d='M275 310 C180 345 85 415 10 525'/>
        <path d='M275 310 C205 230 95 205 -35 225'/>
        <path d='M275 310 C360 210 465 165 585 150'/>
        <path d='M275 310 C405 310 505 365 590 455'/>
      </g>
      <g opacity='.12' fill='#bbf7d0'>
        <circle cx='280' cy='180' r='2'/><circle cx='590' cy='95' r='2'/><circle cx='910' cy='185' r='2'/>
        <circle cx='1280' cy='120' r='2'/><circle cx='1420' cy='650' r='2'/><circle cx='790' cy='760' r='2'/>
      </g>
    </svg>
    """
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode("utf-8")


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 10, 12, .72), rgba(0, 7, 8, .90)), url('{palm_background_uri()}');
            background-size: cover;
            background-attachment: fixed;
        }}
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(2, 16, 22, .98), rgba(2, 32, 22, .95));
            border-right: 1px solid rgba(66, 220, 180, .24);
        }}
        div[data-testid="stSidebarContent"] {{ padding-top: 1rem; }}
        .block-container {{ padding-top: 1.3rem; padding-bottom: 1rem; max-width: 1600px; }}
        .hero {{
            padding: 18px 22px;
            border-radius: 22px;
            background: linear-gradient(135deg, rgba(0, 22, 36, .92), rgba(0, 65, 45, .63));
            border: 1px solid rgba(66, 220, 180, .25);
            box-shadow: 0 16px 40px rgba(0,0,0,.34);
            margin-bottom: 16px;
        }}
        .hero-inner {{ display:flex; align-items:center; gap:24px; }}
        .hero-logo {{ width:170px; border-radius:8px; background:#fff; padding:6px; box-shadow: 0 8px 24px rgba(0,0,0,.35); }}
        .hero h1 {{ color:#f8fafc; font-size:34px; line-height:1.15; margin:0; font-weight:950; letter-spacing:.2px; }}
        .hero p {{ color:#86efac; font-size:16px; margin:.45rem 0 0; font-weight:700; }}
        .last-card {{
            padding: 11px 14px; border-radius: 12px; background: rgba(10, 36, 58, .78);
            border: 1px solid rgba(56, 189, 248, .28); color:#dbeafe; text-align:center; font-weight:800;
        }}
        .sidebar-logo {{ text-align:center; margin: 2px 0 18px; }}
        .sidebar-logo img {{ width: 185px; border-radius:8px; background:white; padding:5px; }}
        .side-title {{ color:#86efac; font-weight:950; font-size:18px; margin: 15px 0 10px; }}
        .metric-card {{
            display:flex; align-items:center; gap:14px; min-height:94px; padding: 16px 18px; border-radius:18px;
            background: linear-gradient(135deg, rgba(5, 27, 38, .92), rgba(8, 50, 42, .72));
            border: 1px solid rgba(59, 130, 246, .35); box-shadow: 0 8px 26px rgba(0,0,0,.22);
        }}
        .metric-icon {{ width:52px; height:52px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:34px; background: rgba(56,189,248,.13); }}
        .metric-label {{ color:#dbeafe; font-size:13px; font-weight:800; }}
        .metric-value {{ color:#f8fafc; font-size:29px; font-weight:950; line-height:1.05; margin-top:4px; }}
        .metric-sub {{ color:#86efac; font-size:12px; margin-top:2px; }}
        .chart-card-title {{
            font-size:17px; font-weight:950; color:#f8fafc; margin: 30px 0 18px 0; padding-top: 6px; line-height:1.4;
        }}
        .section-title {{ font-size:20px; font-weight:950; color:#86efac; margin: 12px 0 16px; }}
        div[data-testid="stPlotlyChart"] {{
            background: rgba(2, 16, 22, .72); border: 1px solid rgba(148, 163, 184, .20); border-radius: 18px; padding: 10px;
        }}
        div[data-testid="stDataFrame"] {{ border-radius:14px; overflow:hidden; border: 1px solid rgba(148, 163, 184, .18); }}
        .footer {{ text-align:center; color:#bbf7d0; padding:16px; opacity:.9; font-size:13px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    raw = pd.read_excel(DATA_FILE, header=None)
    header_candidates = raw.index[
        raw.apply(lambda r: r.astype(str).str.contains("Estate", case=False, na=False).any(), axis=1)
    ].tolist()
    header_idx = header_candidates[0] if header_candidates else 0
    df = pd.read_excel(DATA_FILE, header=header_idx)
    df = df.rename(columns=lambda c: str(c).strip())

    aliases = {
        "Document date": "Document Date",
        "document date": "Document Date",
        "Document number": "Document No",
        "Document Number": "Document No",
        "Document No": "Document No",
        "Quantity": "quantity",
        "quantity": "quantity",
        "Estate": "Estate",
        "Divisi": "Divisi",
        "Division": "Divisi",
        "UM": "UM",
        "User Name": "User Name",
        "Created on": "Created on",
        "Time": "Time",
        "StatKF": "StatKF",
    }
    df = df.rename(columns={c: aliases.get(c, c) for c in df.columns})
    needed = ["Document Date", "Estate", "Divisi", "quantity", "UM"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"Kolom tidak ditemukan: {', '.join(missing)}")

    keep = [c for c in ["Document Date", "Estate", "Divisi", "quantity", "UM", "Document No", "StatKF", "Created on", "Time", "User Name"] if c in df.columns]
    df = df[keep].copy()
    df["Document Date"] = pd.to_datetime(df["Document Date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["Estate"] = df["Estate"].astype(str).str.strip()
    df["Divisi"] = df["Divisi"].astype(str).str.strip()
    df["UM"] = df["UM"].fillna("MM").astype(str).str.strip()
    df = df.dropna(subset=["Document Date"])
    df = df[(df["Estate"] != "") & (df["Estate"].str.lower() != "nan") & (df["Divisi"] != "") & (df["Divisi"].str.lower() != "nan")]
    df["Tanggal"] = df["Document Date"].dt.date
    df["Bulan"] = df["Document Date"].dt.month.map(MONTH_MAP)
    df["Bulan"] = pd.Categorical(df["Bulan"], categories=MONTH_ORDER, ordered=True)
    df["Minggu"] = pd.cut(df["Document Date"].dt.day, bins=[0, 7, 14, 21, 31], labels=WEEK_ORDER, include_lowest=True)
    return df.sort_values(["Document Date", "Estate", "Divisi"]).reset_index(drop=True)


def condition_status(mm: float) -> str:
    if mm < 100:
        return "Kering"
    if mm <= 300:
        return "Normal"
    return "Tinggi"


def status_badge(status: str) -> str:
    icon = {"Kering": "🟠", "Normal": "🟢", "Tinggi": "🔴"}.get(status, "⚪")
    return f"{icon} {status}"


def chart_layout(fig: go.Figure, height: int = 300, show_legend: bool = True) -> go.Figure:
    """Standarisasi tampilan grafik agar label, legenda, dan sumbu jelas terbaca."""
    fig.update_layout(
        height=height,
        template="plotly_dark",
        margin=dict(l=58, r=26, t=74, b=72),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=(
            dict(
                orientation="h",
                yanchor="bottom",
                y=1.18,
                xanchor="center",
                x=0.5,
                font=dict(size=14, color="#f8fafc"),
                bgcolor="rgba(2, 6, 23, .55)",
                bordercolor="rgba(148,163,184,.25)",
                borderwidth=1,
            )
            if show_legend
            else None
        ),
        font=dict(color="#f8fafc", size=14),
        hoverlabel=dict(font_size=14, font_color="#f8fafc", bgcolor="#0f172a"),
        uniformtext_minsize=12,
        uniformtext_mode="show",
    )
    fig.update_xaxes(
        gridcolor="rgba(148,163,184,.18)",
        zerolinecolor="rgba(148,163,184,.20)",
        title_font=dict(size=15, color="#f8fafc"),
        tickfont=dict(size=13, color="#f8fafc"),
        automargin=True,
    )
    fig.update_yaxes(
        gridcolor="rgba(148,163,184,.18)",
        zerolinecolor="rgba(148,163,184,.20)",
        title_font=dict(size=15, color="#f8fafc"),
        tickfont=dict(size=13, color="#f8fafc"),
        automargin=True,
    )
    return fig


def fmt_int(value: float) -> str:
    """Format angka menjadi bulat dengan pemisah ribuan."""
    try:
        return f"{int(round(float(value))):,}"
    except Exception:
        return "0"

def metric_card(col, icon: str, label: str, value: str, sub: str) -> None:
    col.markdown(
        f"""
        <div class='metric-card'>
          <div class='metric-icon'>{icon}</div>
          <div>
            <div class='metric-label'>{label}</div>
            <div class='metric-value'>{value}</div>
            <div class='metric-sub'>{sub}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_box(text: str = "Tidak ada data pada filter ini.") -> None:
    st.info(text)


inject_css()
df = load_data()
logo_uri = image_to_data_uri(LOGO_FILE)

with st.sidebar:
    st.markdown(f"<div class='sidebar-logo'><img src='{logo_uri}'></div>", unsafe_allow_html=True)
    st.markdown("<div class='side-title'>PENCARIAN</div>", unsafe_allow_html=True)

    estates = sorted(df["Estate"].dropna().astype(str).unique().tolist())
    min_date = df["Document Date"].min().date()
    max_date = df["Document Date"].max().date()

    estate_choice = st.multiselect(
        "Estate",
        options=estates,
        default=estates,
        placeholder="Pilih satu atau lebih Estate",
        help="Dapat memilih lebih dari satu Estate. Kosongkan pilihan untuk menampilkan semua Estate.",
    )

    if estate_choice:
        divisi_options = sorted(
            df.loc[df["Estate"].isin(estate_choice), "Divisi"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    else:
        divisi_options = sorted(df["Divisi"].dropna().astype(str).unique().tolist())

    divisi_choice = st.multiselect(
        "Divisi",
        options=divisi_options,
        default=divisi_options,
        placeholder="Pilih satu atau lebih Divisi",
        help="Dapat memilih lebih dari satu Divisi. Kosongkan pilihan untuk menampilkan semua Divisi pada Estate terpilih.",
    )
    date_range = st.date_input("Rentang Document Date", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    st.markdown("<div class='side-title'>INFORMASI LENGKAP</div>", unsafe_allow_html=True)

mask = (df["Tanggal"] >= start_date) & (df["Tanggal"] <= end_date)
if estate_choice:
    mask &= df["Estate"].isin(estate_choice)
if divisi_choice:
    mask &= df["Divisi"].isin(divisi_choice)
filtered = df.loc[mask].copy()

# Header
h1, h2 = st.columns([5.3, 1])
with h1:
    st.markdown(
        f"""
        <div class='hero'>
          <div class='hero-inner'>
            <img class='hero-logo' src='{logo_uri}' />
            <div>
              <h1>Dashboard Curah Hujan KMP1 - KARYAMAS PLANTATION</h1>
              <p>Monitoring Curah Hujan per Estate - Analisis Rata-rata Mingguan, Bulanan, Trend, dan Kondisi</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with h2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='last-card'>📅 Data Terakhir<br><span style='color:#86efac'>{df['Document Date'].max().strftime('%d %B %Y')}</span></div>",
        unsafe_allow_html=True,
    )

# Sidebar detail table after filtering
with st.sidebar:
    detail_cols = ["Document Date", "Estate", "Divisi", "quantity", "UM"]
    detail = filtered[detail_cols].rename(columns={"Estate": "Kebun", "quantity": "Quantity"}).copy()
    detail["Document Date"] = detail["Document Date"].dt.strftime("%d/%m/%Y")
    st.dataframe(detail, hide_index=True, use_container_width=True, height=310)
    st.caption(f"Total Data: {len(detail):,} baris")
    st.download_button(
        "📥 Export CSV",
        data=detail.to_csv(index=False).encode("utf-8"),
        file_name="hasil_pencarian_curah_hujan.csv",
        mime="text/csv",
        use_container_width=True,
    )

# Metrics
unique_days = filtered["Tanggal"].nunique() if not filtered.empty else 0
rain_days = filtered.groupby("Tanggal")["quantity"].mean().gt(0).sum() if not filtered.empty else 0
mcols = st.columns(5)
metric_card(mcols[0], "🌧️", "Total Curah Hujan", f"{fmt_int(filtered['quantity'].sum())} mm" if not filtered.empty else "0 mm", "Total seluruh data")
metric_card(mcols[1], "💧", "Rata-rata Curah Hujan", f"{fmt_int(filtered['quantity'].mean())} mm" if not filtered.empty else "0 mm", "Rata-rata per record")
metric_card(mcols[2], "🌴", "Jumlah Estate", f"{filtered['Estate'].nunique():,}", "Total Estate")
metric_card(mcols[3], "🌿", "Jumlah Divisi", f"{filtered['Divisi'].nunique():,}", "Total Divisi")
metric_card(mcols[4], "☔", "Hari Hujan", f"{int(rain_days):,}", f"dari {unique_days:,} hari")

# Aggregations
if filtered.empty:
    weekly = monthly = ranking = pie_data = pd.DataFrame()
else:
    daily_estate = filtered.groupby(["Estate", "Tanggal"], as_index=False)["quantity"].mean()
    daily_estate["Document Date"] = pd.to_datetime(daily_estate["Tanggal"])
    daily_estate["Bulan"] = daily_estate["Document Date"].dt.month.map(MONTH_MAP)
    daily_estate["Minggu"] = pd.cut(daily_estate["Document Date"].dt.day, bins=[0, 7, 14, 21, 31], labels=WEEK_ORDER, include_lowest=True)
    weekly = daily_estate.groupby(["Estate", "Bulan", "Minggu"], observed=True, as_index=False)["quantity"].mean()
    weekly["Periode"] = weekly["Bulan"].astype(str) + "-" + weekly["Minggu"].astype(str)
    weekly["Periode"] = pd.Categorical(weekly["Periode"], categories=WEEK_PERIODS, ordered=True)
    weekly = weekly.dropna(subset=["Periode"]).sort_values(["Periode", "Estate"])
    weekly["Curah Hujan (mm)"] = weekly["quantity"].round(0).astype(int)

    month_div = filtered.copy()
    month_div["Bulan"] = month_div["Document Date"].dt.month.map(MONTH_MAP)
    month_div = month_div[month_div["Bulan"].isin(MONTH_ORDER)]
    monthly_div_sum = month_div.groupby(["Estate", "Divisi", "Bulan"], observed=True, as_index=False)["quantity"].sum()
    monthly = monthly_div_sum.groupby(["Estate", "Bulan"], observed=True, as_index=False)["quantity"].mean()
    monthly["Bulan"] = pd.Categorical(monthly["Bulan"], categories=MONTH_ORDER, ordered=True)
    monthly["MonthNo"] = monthly["Bulan"].astype(str).map(MONTH_NO)
    monthly = monthly.sort_values(["MonthNo", "Estate"])
    monthly["Curah Hujan Bulat"] = monthly["quantity"].round(0).astype(int)
    monthly["Label Curah"] = monthly["Curah Hujan Bulat"].astype(str) + " mm"
    monthly["Status"] = monthly["quantity"].apply(condition_status)
    monthly["Status Kondisi"] = monthly["Status"].map(status_badge)

    ranking = monthly.groupby("Estate", as_index=False)["quantity"].sum().sort_values("quantity", ascending=False).head(3)
    ranking["Curah Hujan"] = ranking["quantity"].round(0).astype(int)

    rain_by_estate_day = filtered.groupby(["Estate", "Tanggal"], as_index=False)["quantity"].mean()
    rain_by_estate_day["Kategori"] = rain_by_estate_day["quantity"].apply(lambda x: "Hari Hujan" if x > 0 else "Tidak Hujan")
    pie_data = rain_by_estate_day.groupby(["Estate", "Kategori"], as_index=False).size().rename(columns={"size": "Jumlah Hari"})

# Charts
c1, c2 = st.columns([1, 1])
with c1:
    st.markdown("<div class='chart-card-title'>1. Grafik Curah Hujan Rata-rata Mingguan per Estate</div>", unsafe_allow_html=True)
    if weekly.empty:
        empty_box()
    else:
        fig = px.line(
            weekly,
            x="Periode",
            y="quantity",
            color="Estate",
            markers=True,
            category_orders={"Periode": WEEK_PERIODS},
            labels={"quantity": "Curah Hujan (mm)", "Periode": "April - Mei - Juni"},
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=9), hovertemplate="Estate: %{fullData.name}<br>Periode: %{x}<br>Curah hujan: %{y:.0f} mm<extra></extra>")
        st.plotly_chart(chart_layout(fig, 360), use_container_width=True)

with c2:
    st.markdown("<div class='chart-card-title'>2. Grafik Curah Hujan Rata-rata Bulanan per Estate</div>", unsafe_allow_html=True)
    if monthly.empty:
        empty_box()
    else:
        fig = px.bar(
            monthly,
            x="Bulan",
            y="quantity",
            color="Estate",
            barmode="group",
            category_orders={"Bulan": MONTH_ORDER},
            labels={"quantity": "Curah Hujan (mm)", "Bulan": "Bulan"},
            text="Curah Hujan Bulat",
        )
        fig.update_traces(
            texttemplate="%{text:.0f} mm",
            textposition="outside",
            textangle=-90,
            textfont=dict(size=13, color="#f8fafc", family="Arial"),
            cliponaxis=False,
            hovertemplate="Estate: %{fullData.name}<br>Bulan: %{x}<br>Curah hujan: %{y:.0f} mm<extra></extra>",
        )
        fig.update_layout(margin=dict(l=60, r=35, t=80, b=70), uniformtext_minsize=11, uniformtext_mode="show")
        st.plotly_chart(chart_layout(fig, 360), use_container_width=True)

c3, c4 = st.columns([1, 1])
with c3:
    st.markdown("<div class='chart-card-title'>3. Trend Curah Hujan Rata-rata per Estate per Bulan</div>", unsafe_allow_html=True)
    if monthly.empty:
        empty_box()
    else:
        fig = px.line(
            monthly,
            x="Bulan",
            y="quantity",
            color="Estate",
            markers=True,
            category_orders={"Bulan": MONTH_ORDER},
            labels={"quantity": "Curah Hujan (mm)", "Bulan": "Bulan"},
        )
        fig.update_traces(
            connectgaps=True,
            line=dict(width=4),
            marker=dict(size=10),
            hovertemplate="Estate: %{fullData.name}<br>Bulan: %{x}<br>Curah hujan: %{y:.0f} mm<extra></extra>",
        )
        st.plotly_chart(chart_layout(fig, 350), use_container_width=True)

with c4:
    st.markdown("<div class='chart-card-title'>4. Ranking 3 Besar Curah Hujan per Estate</div>", unsafe_allow_html=True)
    if ranking.empty:
        empty_box()
    else:
        fig = px.bar(ranking, x="Estate", y="Curah Hujan", text="Curah Hujan", labels={"Curah Hujan": "mm"})
        fig.update_traces(texttemplate="%{text:.0f} mm", textposition="outside", textfont=dict(size=15, color="#f8fafc"), cliponaxis=False, hovertemplate="Estate: %{x}<br>Total rata-rata: %{y:.0f} mm<extra></extra>")
        st.plotly_chart(chart_layout(fig, 350, show_legend=False), use_container_width=True)

st.markdown("<div class='chart-card-title'>5. Diagram Pie Hari Hujan versus Tidak Hujan per Estate</div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="pie-legend-box">
        <div class="pie-legend-item"><span class="pie-legend-color" style="background:{PIE_COLORS['Hari Hujan']};"></span>Hari Hujan</div>
        <div class="pie-legend-item"><span class="pie-legend-color" style="background:{PIE_COLORS['Tidak Hujan']};"></span>Tidak Hujan</div>
    </div>
    """,
    unsafe_allow_html=True,
)
pie_estates = sorted(pie_data["Estate"].dropna().unique().tolist()) if not pie_data.empty else []
if not pie_estates:
    empty_box()
else:
    for start in range(0, len(pie_estates), 5):
        cols = st.columns(5)
        for col, estate in zip(cols, pie_estates[start:start + 5]):
            with col:
                estate_pie = pd.DataFrame({"Kategori": ["Hari Hujan", "Tidak Hujan"]}).merge(
                    pie_data.loc[pie_data["Estate"] == estate, ["Kategori", "Jumlah Hari"]], on="Kategori", how="left"
                )
                estate_pie["Jumlah Hari"] = estate_pie["Jumlah Hari"].fillna(0).astype(int)
                if estate_pie["Jumlah Hari"].sum() == 0:
                    empty_box(f"{estate}: tidak ada data")
                else:
                    fig = go.Figure(
                        data=[go.Pie(
                            labels=estate_pie["Kategori"],
                            values=estate_pie["Jumlah Hari"],
                            hole=0.36,
                            sort=False,
                            marker=dict(colors=[PIE_COLORS[k] for k in estate_pie["Kategori"]], line=dict(color="#ffffff", width=2)),
                            textinfo="none",
                            textposition="inside",
                            insidetextorientation="horizontal",
                            textfont=dict(size=14, color="#ffffff", family="Arial Black"),
                            hovertemplate="<b>%{label}</b><br>%{value} hari<br>%{percent}<extra></extra>",
                        )]
                    )
                    fig.update_layout(
                        title={"text": f"<b>{estate}</b>", "x": .5, "xanchor": "center", "font": {"size": 19, "color": "#ffffff"}},
                        margin=dict(l=8, r=8, t=50, b=8),
                        font=dict(color="#ffffff", size=15),
                    )
                    st.plotly_chart(chart_layout(fig, 255, show_legend=False), use_container_width=True)
                    total_hari = int(estate_pie["Jumlah Hari"].sum())
                    hari_hujan = int(estate_pie.loc[estate_pie["Kategori"] == "Hari Hujan", "Jumlah Hari"].iloc[0])
                    tidak_hujan = int(estate_pie.loc[estate_pie["Kategori"] == "Tidak Hujan", "Jumlah Hari"].iloc[0])
                    pct_hujan = round((hari_hujan / total_hari) * 100) if total_hari else 0
                    pct_tidak = round((tidak_hujan / total_hari) * 100) if total_hari else 0
                    st.markdown(
                        f"""
                        <div class="pie-percent-card">
                            <div><span class="pie-dot rain"></span><b>Hari Hujan</b>: {pct_hujan}% <span>({hari_hujan} hari)</span></div>
                            <div><span class="pie-dot dry"></span><b>Tidak Hujan</b>: {pct_tidak}% <span>({tidak_hujan} hari)</span></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

st.markdown("<div class='chart-card-title'>6. Status Kondisi per Estate per Bulan</div>", unsafe_allow_html=True)
if monthly.empty:
    empty_box()
else:
    status = monthly[["Estate", "Bulan", "Curah Hujan Bulat", "Status Kondisi", "MonthNo"]].sort_values(["Estate", "MonthNo"])
    status = status.drop(columns=["MonthNo"]).rename(columns={"Curah Hujan Bulat": "Curah Hujan (mm)"})
    st.dataframe(status, hide_index=True, use_container_width=True, height=260)
    st.caption("Keterangan status: <100 mm = Kering, 100–300 mm = Normal, >300 mm = Tinggi.")

st.markdown("<div class='footer'>🌿 KARYAMAS PLANTATION • Monitoring Curah Hujan untuk Pengelolaan Perkebunan yang Lebih Baik</div>", unsafe_allow_html=True)
