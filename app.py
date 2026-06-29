
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Curah Hujan", page_icon="🌧️", layout="wide")

st.title("🌧️ Dashboard Monitoring Curah Hujan")
st.caption("Database: DATA CURAH HUJAN APRIL-JUNI 2026")


@st.cache_data
def load_data():
    df = pd.read_excel(
        "DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1).xlsx",
        header=1
    )

    df.columns = [str(c).strip() for c in df.columns]

    df["Document Date"] = pd.to_datetime(
        df["Document Date"],
        errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    return df


df = load_data()


# =============================
# MENU PENCARIAN DI ATAS
# =============================

st.subheader("🔎 Menu Pencarian Data")

a,b = st.columns(2)

with a:
    estate = st.multiselect(
        "🏡 Estate",
        sorted(df["Estate"].dropna().astype(str).unique())
    )

with b:
    divisi = st.multiselect(
        "🏢 Divisi",
        sorted(df["Divisi"].dropna().astype(str).unique())
    )


c,d = st.columns(2)

with c:
    tanggal_awal = st.date_input(
        "📅 Document Date Mulai",
        df["Document Date"].min().date()
    )

with d:
    tanggal_akhir = st.date_input(
        "📅 Document Date Sampai",
        df["Document Date"].max().date()
    )


hasil = df.copy()

if estate:
    hasil = hasil[
        hasil["Estate"].astype(str).isin(estate)
    ]

if divisi:
    hasil = hasil[
        hasil["Divisi"].astype(str).isin(divisi)
    ]

hasil = hasil[
    (hasil["Document Date"].dt.date >= tanggal_awal) &
    (hasil["Document Date"].dt.date <= tanggal_akhir)
]


st.divider()


# =============================
# HASIL PENCARIAN DETAIL
# =============================

st.subheader("📋 Informasi Lengkap Hasil Pencarian")

kolom = [
    "Document Date",
    "Estate",
    "Divisi",
    "quantity",
    "UM"
]

st.dataframe(
    hasil[kolom],
    use_container_width=True
)


x1,x2,x3 = st.columns(3)

x1.metric("Jumlah Data", len(hasil))

x2.metric(
    "Total Curah Hujan",
    f"{hasil['quantity'].sum():,.0f} mm"
)

x3.metric(
    "Periode",
    f"{tanggal_awal} - {tanggal_akhir}"
)


st.divider()


# =============================
# GRAFIK ANALISIS
# =============================

st.subheader("📊 Analisis Curah Hujan")


# 1 Harian Estate
st.write("### 1. Curah Hujan Harian per Estate")

harian = hasil.groupby(
    ["Document Date","Estate"],
    as_index=False
)["quantity"].sum()

st.plotly_chart(
    px.line(
        harian,
        x="Document Date",
        y="quantity",
        color="Estate",
        markers=True
    ),
    use_container_width=True
)


# 2 Bulanan Estate
st.write("### 2. Curah Hujan Bulanan per Estate")

bulanan = hasil.copy()

bulanan["Bulan"] = (
    bulanan["Document Date"]
    .dt.to_period("M")
    .astype(str)
)

bulanan = bulanan.groupby(
    ["Bulan","Estate"],
    as_index=False
)["quantity"].sum()


st.plotly_chart(
    px.bar(
        bulanan,
        x="Bulan",
        y="quantity",
        color="Estate",
        barmode="group"
    ),
    use_container_width=True
)


# 3 Trend
st.write("### 3. Trend Curah Hujan per Estate")

st.plotly_chart(
    px.line(
        bulanan,
        x="Bulan",
        y="quantity",
        color="Estate",
        markers=True
    ),
    use_container_width=True
)


# 4 Ranking
st.write("### 4. Ranking 3 Besar Curah Hujan Estate")

ranking = (
    bulanan.groupby("Estate", as_index=False)["quantity"]
    .sum()
    .sort_values(
        "quantity",
        ascending=False
    )
    .head(3)
)

st.dataframe(
    ranking,
    use_container_width=True
)


# 5 Status
st.write("### 5. Status Kondisi Estate per Bulan")


def kondisi(nilai):
    if nilai < 100:
        return "Kering"
    elif nilai <= 300:
        return "Normal"
    else:
        return "Tinggi"


status = bulanan.copy()

status["Status"] = status["quantity"].apply(kondisi)


st.dataframe(
    status[
        [
            "Bulan",
            "Estate",
            "quantity",
            "Status"
        ]
    ],
    use_container_width=True
)

st.info(
    "Kriteria: <100 mm Kering | 100-300 mm Normal | >300 mm Tinggi"
)
