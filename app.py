
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Curah Hujan Sawit", page_icon="🌴", layout="wide")

st.markdown("""
<style>
.stApp{
background-image:linear-gradient(rgba(255,255,255,0.85),rgba(255,255,255,0.85)),
url("https://images.unsplash.com/photo-1595841696677-6489ff3f8cd1");
background-size:cover;
background-attachment:fixed;
}
</style>
""", unsafe_allow_html=True)

st.title("🌴 Dashboard Monitoring Curah Hujan Perkebunan Kelapa Sawit")

@st.cache_data
def load_data():
    df = pd.read_excel(
        "DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1).xlsx",
        header=1
    )
    df.columns = [str(c).strip() for c in df.columns]
    df["Document Date"] = pd.to_datetime(df["Document Date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    return df

df = load_data()

# =========================
# MENU PENCARIAN
# =========================
st.subheader("🔎 Menu Pencarian Data")

col1, col2 = st.columns(2)

with col1:
    pilih_estate = st.multiselect(
        "🏡 Estate",
        sorted(df["Estate"].dropna().astype(str).unique())
    )

with col2:
    pilih_divisi = st.multiselect(
        "🏢 Divisi",
        sorted(df["Divisi"].dropna().astype(str).unique())
    )

col3, col4 = st.columns(2)

with col3:
    tanggal_awal = st.date_input(
        "📅 Document Date Mulai",
        df["Document Date"].min().date()
    )

with col4:
    tanggal_akhir = st.date_input(
        "📅 Document Date Sampai",
        df["Document Date"].max().date()
    )


data = df.copy()

if pilih_estate:
    data = data[data["Estate"].astype(str).isin(pilih_estate)]

if pilih_divisi:
    data = data[data["Divisi"].astype(str).isin(pilih_divisi)]

data = data[
    (data["Document Date"].dt.date >= tanggal_awal) &
    (data["Document Date"].dt.date <= tanggal_akhir)
]


# HASIL PENCARIAN
st.subheader("📋 Informasi Lengkap Hasil Pencarian")

st.dataframe(
    data[["Document Date","Estate","Divisi","quantity","UM"]],
    use_container_width=True
)


st.divider()

# ANALISIS
st.subheader("📊 Grafik Analisis")

data["Bulan"] = data["Document Date"].dt.month_name()
data["Minggu"] = "W" + (((data["Document Date"].dt.day-1)//7)+1).astype(str)

bulan = ["April","May","June"]

weekly = data.groupby(
    ["Bulan","Minggu","Estate"],
    as_index=False
)["quantity"].mean().round(0)

st.plotly_chart(
    px.bar(
        weekly,
        x="Minggu",
        y="quantity",
        color="Estate",
        facet_col="Bulan"
    ),
    use_container_width=True
)

monthly = data.groupby(
    ["Bulan","Estate"],
    as_index=False
)["quantity"].mean().round(0)

st.plotly_chart(
    px.bar(
        monthly,
        x="Bulan",
        y="quantity",
        color="Estate",
        category_orders={"Bulan":bulan}
    ),
    use_container_width=True
)

trend = monthly.copy()

st.plotly_chart(
    px.bar(
        trend,
        x="Bulan",
        y="quantity",
        color="Estate",
        category_orders={"Bulan":bulan}
    ),
    use_container_width=True
)

pie = data.copy()
pie["Status Hari"] = pie["quantity"].apply(lambda x:"Hari Hujan" if x>0 else "Tidak Hujan")

pie = pie.groupby(["Estate","Status Hari"]).size().reset_index(name="Jumlah Hari")

st.plotly_chart(
    px.pie(
        pie,
        names="Status Hari",
        values="Jumlah Hari",
        facet_col="Estate"
    ),
    use_container_width=True
)

ranking = monthly.groupby("Estate",as_index=False)["quantity"].sum().round(0)
ranking = ranking.sort_values("quantity",ascending=False).head(3)

st.subheader("🏆 Ranking 3 Besar Estate")
st.dataframe(ranking)

status = monthly.copy()
status["Curah Hujan Bulanan"] = (status["quantity"]*30).round(0)

def kondisi(x):
    if x < 100:
        return "Kering"
    elif x <= 300:
        return "Normal"
    else:
        return "Tinggi"

status["Status"] = status["Curah Hujan Bulanan"].apply(kondisi)

st.subheader("🌧️ Status Kondisi Estate")
st.dataframe(status)
