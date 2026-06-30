
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Karyamas Plantation Rainfall Dashboard",
    page_icon="🌧️",
    layout="wide"
)

st.image("pt_karyamas_adinusantara_logo.jpg", width=240)

st.title("🌧️ Rainfall Monitoring Dashboard")
st.subheader("Karyamas Plantation - Estate Rainfall System")

@st.cache_data
def load_data():
    df = pd.read_excel(
        "DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1)(5).xlsx",
        header=1
    )

    df.columns = [
        "Estate","Divisi","Document Number",
        "Document Date","Statkf","Quantity",
        "UM","Created On","Created By",
        "Time","User Name"
    ]

    df["Document Date"] = pd.to_datetime(
        df["Document Date"], errors="coerce"
    )
    df["Quantity"] = pd.to_numeric(
        df["Quantity"], errors="coerce"
    )

    df["Bulan"] = df["Document Date"].dt.month_name()
    df["Minggu"] = (
        "W" + df["Document Date"].dt.day.sub(1).floordiv(7).add(1).astype(str)
    )

    return df


df = load_data()

st.divider()

st.subheader("🔎 Filter Data")

a,b,c = st.columns(3)

with a:
    estate = st.selectbox(
        "🏝️ Estate",
        ["Semua"] + sorted(df.Estate.dropna().unique())
    )

with b:
    divisi = st.selectbox(
        "🌱 Divisi",
        ["Semua"] + sorted(df.Divisi.dropna().unique())
    )

with c:
    periode = st.date_input(
        "📅 Rentang Document Date",
        []
    )

hasil = df.copy()

if estate != "Semua":
    hasil = hasil[hasil.Estate == estate]

if divisi != "Semua":
    hasil = hasil[hasil.Divisi == divisi]

if len(periode)==2:
    hasil = hasil[
        (hasil["Document Date"] >= pd.to_datetime(periode[0])) &
        (hasil["Document Date"] <= pd.to_datetime(periode[1]))
    ]


x1,x2,x3,x4 = st.columns(4)

x1.metric("Jumlah Record", len(hasil))
x2.metric("Total Rainfall", f"{hasil.Quantity.sum():,.1f} mm")
x3.metric("Average", f"{hasil.Quantity.mean():,.1f} mm")
x4.metric("Estate", hasil.Estate.nunique())


st.divider()

if not hasil.empty:

    st.subheader("📊 Grafik Curah Hujan")

    daily = hasil.groupby(
        "Document Date"
    )["Quantity"].mean().reset_index()

    st.plotly_chart(
        px.line(
            daily,
            x="Document Date",
            y="Quantity",
            markers=True,
            title="Trend Curah Hujan Harian"
        ),
        use_container_width=True
    )


    weekly = hasil.groupby(
        ["Bulan","Minggu"]
    )["Quantity"].mean().reset_index()

    st.plotly_chart(
        px.bar(
            weekly,
            x="Minggu",
            y="Quantity",
            color="Bulan",
            title="Curah Hujan Mingguan W1-W4"
        ),
        use_container_width=True
    )


    estate_rank = hasil.groupby(
        "Estate"
    )["Quantity"].sum().reset_index()

    st.plotly_chart(
        px.bar(
            estate_rank,
            x="Estate",
            y="Quantity",
            title="Ranking Curah Hujan Estate"
        ),
        use_container_width=True
    )


    st.subheader("📋 Detail Data")

    detail = hasil[
        [
            "Document Date",
            "Estate",
            "Divisi",
            "Quantity",
            "UM"
        ]
    ]

    st.dataframe(
        detail,
        use_container_width=True,
        hide_index=True
    )

    csv = detail.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Export Excel/CSV",
        csv,
        "laporan_curah_hujan.csv"
    )

else:
    st.warning("Tidak ada data")


st.sidebar.image(
    "pt_karyamas_adinusantara_logo.jpg",
    width=180
)

st.sidebar.success(
    "Karyamas Plantation\nRainfall Monitoring"
)
