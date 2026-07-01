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

st.set_page_config(
    page_title="Dashboard Curah Hujan KMP1 - KARYAMAS PLANTATION",
    page_icon=Image.open(LOGO_FILE) if LOGO_FILE.exists() else "🌴",
    layout="wide",
    initial_sidebar_state="expanded",
)

MONTH_ORDER = ["April", "Mei", "Juni"]
MONTH_MAP = {4: "April", 5: "Mei", 6: "Juni"}
MONTH_NO = {m: i for i, m in enumerate(MONTH_ORDER, start=1)}
WEEK_ORDER = ["W1", "W2", "W3", "W4"]
WEEK_PERIODS = [f"{m}-{w}" for m in MONTH_ORDER for w in WEEK_ORDER]


def image_to_data_uri(path: Path) -> str:
    mime = "image/jpeg" if path.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("utf-8")


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
    fig.update_layout(
        height=height,
        template="plotly_dark",
        margin=dict(l=22, r=18, t=30, b=34),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1) if show_legend else None,
        font=dict(color="#e5e7eb", size=12),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,.14)", zerolinecolor="rgba(148,163,184,.18)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,.14)", zerolinecolor="rgba(148,163,184,.18)")
    return fig


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
    divisis = sorted(df["Divisi"].dropna().astype(str).unique().tolist())
    min_date = df["Document Date"].min().date()
    max_date = df["Document Date"].max().date()

    estate_choice = st.selectbox("Estate", ["Semua Estate"] + estates)
    divisi_choice = st.selectbox("Divisi", ["Semua Divisi"] + divisis)
    date_range = st.date_input("Rentang Document Date", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    st.markdown("<div class='side-title'>INFORMASI LENGKAP</div>", unsafe_allow_html=True)

mask = (df["Tanggal"] >= start_date) & (df["Tanggal"] <= end_date)
if estate_choice != "Semua Estate":
    mask &= df["Estate"] == estate_choice
if divisi_choice != "Semua Divisi":
    mask &= df["Divisi"] == divisi_choice
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
              <p>Monitoring Curah Hujan per Estate - Analisis Rata-rata Harian, Bulanan, Trend, dan Kondisi</p>
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
metric_card(mcols[0], "🌧️", "Total Curah Hujan", f"{round(filtered['quantity'].sum()):,} mm" if not filtered.empty else "0 mm", "Total seluruh data")
metric_card(mcols[1], "💧", "Rata-rata Curah Hujan", f"{round(filtered['quantity'].mean()):,} mm" if not filtered.empty else "0 mm", "Rata-rata per record")
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

    month_div = filtered.copy()
    month_div["Bulan"] = month_div["Document Date"].dt.month.map(MONTH_MAP)
    month_div = month_div[month_div["Bulan"].isin(MONTH_ORDER)]
    monthly_div_sum = month_div.groupby(["Estate", "Divisi", "Bulan"], observed=True, as_index=False)["quantity"].sum()
    monthly = monthly_div_sum.groupby(["Estate", "Bulan"], observed=True, as_index=False)["quantity"].mean()
    monthly["Bulan"] = pd.Categorical(monthly["Bulan"], categories=MONTH_ORDER, ordered=True)
    monthly["MonthNo"] = monthly["Bulan"].astype(str).map(MONTH_NO)
    monthly = monthly.sort_values(["MonthNo", "Estate"])
    monthly["Curah Hujan Bulat"] = monthly["quantity"].round(0).astype(int)
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
    st.markdown("<div class='chart-card-title'>1. Grafik Curah Hujan Rata-rata Harian per Estate per Minggu</div>", unsafe_allow_html=True)
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
        st.plotly_chart(chart_layout(fig, 330), use_container_width=True)

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
        )
        st.plotly_chart(chart_layout(fig, 330), use_container_width=True)

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
        fig.update_traces(connectgaps=True, line=dict(width=3), marker=dict(size=8))
        st.plotly_chart(chart_layout(fig, 320), use_container_width=True)

with c4:
    st.markdown("<div class='chart-card-title'>4. Ranking 3 Besar Curah Hujan per Estate</div>", unsafe_allow_html=True)
    if ranking.empty:
        empty_box()
    else:
        fig = px.bar(ranking, x="Estate", y="Curah Hujan", text="Curah Hujan", labels={"Curah Hujan": "mm"})
        fig.update_traces(texttemplate="%{text:.0f} mm", textposition="outside", cliponaxis=False)
        st.plotly_chart(chart_layout(fig, 320, show_legend=False), use_container_width=True)

st.markdown("<div class='chart-card-title'>5. Diagram Pie Hari Hujan versus Tidak Hujan per Estate</div>", unsafe_allow_html=True)
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
                        data=[go.Pie(labels=estate_pie["Kategori"], values=estate_pie["Jumlah Hari"], hole=0.35, textinfo="percent+label")]
                    )
                    fig.update_layout(title={"text": f"<b>{estate}</b>", "x": .5, "xanchor": "center"})
                    st.plotly_chart(chart_layout(fig, 265, show_legend=False), use_container_width=True)

st.markdown("<div class='chart-card-title'>6. Status Kondisi per Estate per Bulan</div>", unsafe_allow_html=True)
if monthly.empty:
    empty_box()
else:
    status = monthly[["Estate", "Bulan", "Curah Hujan Bulat", "Status Kondisi", "MonthNo"]].sort_values(["Estate", "MonthNo"])
    status = status.drop(columns=["MonthNo"]).rename(columns={"Curah Hujan Bulat": "Curah Hujan (mm)"})
    st.dataframe(status, hide_index=True, use_container_width=True, height=260)
    st.caption("Keterangan status: <100 mm = Kering, 100–300 mm = Normal, >300 mm = Tinggi.")

st.markdown("<div class='footer'>🌿 KARYAMAS PLANTATION • Monitoring Curah Hujan untuk Pengelolaan Perkebunan yang Lebih Baik</div>", unsafe_allow_html=True)
