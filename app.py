
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Curah Hujan Estate",
    page_icon="🌴",
    layout="wide"
)

# Background foto perkebunan kelapa sawit
st.markdown("""
<style>
.stApp {
    background-image:
    linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
    url("https://images.unsplash.com/photo-1595841696677-6489ff3f8cd1");
    background-size: cover;
    background-attachment: fixed;
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


# ======================
# FILTER
# ======================

st.subheader("🔎 Menu Pencarian")

c1,c2 = st.columns(2)

with c1:
    estate = st.multiselect(
        "Estate",
        sorted(df["Estate"].dropna().astype(str).unique())
    )

with c2:
    divisi = st.multiselect(
        "Divisi",
        sorted(df["Divisi"].dropna().astype(str).unique())
    )


hasil = df.copy()

if estate:
    hasil = hasil[hasil["Estate"].astype(str).isin(estate)]

if divisi:
    hasil = hasil[hasil["Divisi"].astype(str).isin(divisi)]


# ======================
# HASIL
# ======================

st.subheader("📋 Informasi Lengkap Hasil Pencarian")

st.dataframe(
    hasil[
        [
            "Document Date",
            "Estate",
            "Divisi",
            "quantity",
            "UM"
        ]
    ],
    use_container_width=True
)


st.divider()

st.header("📊 Analisis Curah Hujan")


data = hasil.copy()

data["Bulan"] = data["Document Date"].dt.month_name()

data["Minggu"] = (
    "W" +
    (((data["Document Date"].dt.day-1)//7)+1).astype(str)
)


bulan_order = ["April","May","June"]
minggu_order = ["W1","W2","W3","W4"]


# 1 Rata-rata harian mingguan semua divisi
st.subheader("1. Rata-rata Curah Hujan Harian per Estate per Minggu")


weekly = data.groupby(
    ["Bulan","Minggu","Estate"],
    as_index=False
)["quantity"].mean().round(0)


weekly["Bulan"] = pd.Categorical(
    weekly["Bulan"],
    categories=bulan_order,
    ordered=True
)

weekly["Minggu"] = pd.Categorical(
    weekly["Minggu"],
    categories=minggu_order,
    ordered=True
)


st.plotly_chart(
    px.bar(
        weekly,
        x="Minggu",
        y="quantity",
        color="Estate",
        facet_col="Bulan",
        category_orders={
            "Bulan":bulan_order,
            "Minggu":minggu_order
        }
    ),
    use_container_width=True
)



# 2 Rata-rata bulanan
st.subheader("2. Rata-rata Curah Hujan Bulanan per Estate")


monthly_avg = data.groupby(
    ["Bulan","Estate"],
    as_index=False
)["quantity"].mean().round(0)


monthly_avg["Bulan"] = pd.Categorical(
    monthly_avg["Bulan"],
    categories=bulan_order,
    ordered=True
)


st.plotly_chart(
    px.bar(
        monthly_avg,
        x="Bulan",
        y="quantity",
        color="Estate",
        barmode="group",
        category_orders={"Bulan":bulan_order}
    ),
    use_container_width=True
)



# 3 Trend
st.subheader("3. Trend Rata-rata Curah Hujan Estate per Bulan")


st.plotly_chart(
    px.bar(
        monthly_avg,
        x="Bulan",
        y="quantity",
        color="Estate",
        category_orders={"Bulan":bulan_order}
    ),
    use_container_width=True
)



# 4 Pie
st.subheader("4. Hari Hujan vs Tidak Hujan per Estate")


pie = data.copy()

pie["Status Hari"] = pie["quantity"].apply(
    lambda x: "Hari Hujan" if x > 0 else "Tidak Hujan"
)

pie = pie.groupby(
    ["Estate","Status Hari"]
).size().reset_index(name="Jumlah Hari")


st.plotly_chart(
    px.pie(
        pie,
        names="Status Hari",
        values="Jumlah Hari",
        facet_col="Estate"
    ),
    use_container_width=True
)



# 5 Ranking
st.subheader("5. Ranking 3 Besar Curah Hujan Estate")


ranking = monthly_avg.groupby(
    "Estate",
    as_index=False
)["quantity"].sum().round(0)


ranking = ranking.sort_values(
    "quantity",
    ascending=False
).head(3)


st.dataframe(
    ranking,
    use_container_width=True
)



# 6 Status menggunakan total curah hujan rata-rata divisi x 1 bulan

st.subheader("6. Status Kondisi Estate per Bulan")


status = monthly_avg.copy()

# total bulanan dari rata-rata harian
status["Curah Hujan Bulanan"] = (
    status["quantity"] * 30
).round(0)


def kondisi(x):
    if x < 100:
        return "Kering"
    elif x <= 300:
        return "Normal"
    else:
        return "Tinggi"


status["Status"] = status["Curah Hujan Bulanan"].apply(kondisi)


st.dataframe(
    status[
        [
            "Bulan",
            "Estate",
            "Curah Hujan Bulanan",
            "Status"
        ]
    ],
    use_container_width=True
)


st.info(
    "Status: <100 mm Kering | 100-300 mm Normal | >300 mm Tinggi"
)
