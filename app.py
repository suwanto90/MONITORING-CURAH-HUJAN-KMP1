
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Curah Hujan", page_icon="🌧️", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1).xlsx", header=1)
    df.columns = [str(c).strip() for c in df.columns]
    return df

df = load_data()

st.title("🌧️ Dashboard Pencarian Data Curah Hujan")
st.caption("Pencarian berdasarkan Estate, Divisi, dan Document Date")

# Normalize date
if "Document Date" in df.columns:
    df["Document Date"] = pd.to_datetime(df["Document Date"], errors="coerce")

# Search menu
c1, c2, c3 = st.columns(3)

with c1:
    estate = st.selectbox("🏡 Estate", ["Semua"] + sorted(df["Estate"].dropna().astype(str).unique()))

with c2:
    divisi_col = "Divisi" if "Divisi" in df.columns else None
    divisi = st.selectbox("🏢 Divisi", ["Semua"] + sorted(df[divisi_col].dropna().astype(str).unique())) if divisi_col else "Semua"

with c3:
    tanggal = st.date_input("📅 Document Date")

result = df.copy()

if estate != "Semua":
    result = result[result["Estate"].astype(str) == estate]

if divisi_col and divisi != "Semua":
    result = result[result["Divisi"].astype(str) == divisi]

if tanggal:
    result = result[result["Document Date"].dt.date == tanggal]

st.divider()

# Result
st.subheader("📋 Hasil Pencarian")

show_cols = [c for c in ["Document Date","Estate","Divisi","Quantity","UM"] if c in result.columns]

if len(result):
    st.dataframe(result[show_cols], use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Data", len(result))
    if "Quantity" in result.columns:
        col2.metric("Total Curah Hujan", f'{pd.to_numeric(result["Quantity"], errors="coerce").sum():,.0f}')
    col3.metric("Satuan", result["UM"].iloc[0] if "UM" in result.columns else "-")

    st.subheader("📊 Grafik Curah Hujan")

    if "Estate" in result.columns and "Quantity" in result.columns:
        chart = px.bar(
            result,
            x="Estate",
            y="Quantity",
            title="Curah Hujan per Estate"
        )
        st.plotly_chart(chart, use_container_width=True)

    if "Document Date" in result.columns and "Quantity" in result.columns:
        trend = px.line(
            result.sort_values("Document Date"),
            x="Document Date",
            y="Quantity",
            markers=True,
            title="Trend Curah Hujan"
        )
        st.plotly_chart(trend, use_container_width=True)

else:
    st.warning("Data tidak ditemukan. Silakan ubah filter pencarian.")

st.sidebar.header("🌱 Informasi")
st.sidebar.write("Dashboard menggunakan database Excel curah hujan April-Juni 2026.")
