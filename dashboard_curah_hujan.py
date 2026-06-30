
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Karyamas Rainfall Dashboard",
    page_icon="🌧️",
    layout="wide"
)

@st.cache_data
def load_data():

    df = pd.read_excel(
        "DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1)(5).xlsx",
        header=1
    )

    df.columns = [
        "Estate",
        "Divisi",
        "Document Number",
        "Document Date",
        "Statkf",
        "Quantity",
        "UM",
        "Created On",
        "Created By",
        "Time",
        "User Name"
    ]

    # perbaikan tanggal
    df["Document Date"] = pd.to_datetime(
        df["Document Date"],
        errors="coerce"
    )

    df = df.dropna(subset=["Document Date"])

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    return df


# WAJIB: df dibuat sebelum dipakai
df = load_data()


st.title("🌧️ Dashboard Monitoring Curah Hujan")
st.write("Karyamas Plantation")


# rentang tanggal aman
date_series = df["Document Date"].dropna()

if len(date_series) > 0:

    min_date = date_series.min().date()
    max_date = date_series.max().date()

else:

    min_date = pd.Timestamp("2026-04-01").date()
    max_date = pd.Timestamp("2026-06-30").date()


tanggal = st.date_input(
    "Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


hasil = df.copy()

if len(tanggal) == 2:

    hasil = hasil[
        (hasil["Document Date"] >= pd.to_datetime(tanggal[0])) &
        (hasil["Document Date"] <= pd.to_datetime(tanggal[1]))
    ]


st.metric(
    "Total Curah Hujan",
    f"{hasil['Quantity'].sum():.0f} mm"
)

st.dataframe(
    hasil[
        [
            "Document Date",
            "Estate",
            "Divisi",
            "Quantity",
            "UM"
        ]
    ],
    use_container_width=True
)
