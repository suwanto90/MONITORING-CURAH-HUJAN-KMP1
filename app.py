import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Curah Hujan Sawit", page_icon="🌴", layout="wide")

st.markdown("""
<style>
.stApp{
background:#06131b;
background-image:linear-gradient(rgba(0,0,0,.85),rgba(0,0,0,.85)),
url('https://images.unsplash.com/photo-1595841696677-6489ff3f8cd1');
background-size:cover;
background-attachment:fixed;
color:white;
}
</style>
""", unsafe_allow_html=True)

st.title("🌴 DASHBOARD SISTEM MONITORING TERPADU CURAH HUJAN")

@st.cache_data
def load_data():
    df=pd.read_excel("DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1).xlsx",header=1)
    df.columns=[str(c).strip() for c in df.columns]
    df["Document Date"]=pd.to_datetime(df["Document Date"],errors="coerce")
    df["quantity"]=pd.to_numeric(df["quantity"],errors="coerce")
    return df

df=load_data()

st.subheader("🔎 Menu Pencarian")

c1,c2,c3=st.columns(3)

with c1:
    estate=st.multiselect("🏡 Estate",sorted(df["Estate"].dropna().astype(str).unique()))
with c2:
    divisi=st.multiselect("🏢 Divisi",sorted(df["Divisi"].dropna().astype(str).unique()))
with c3:
    tanggal=st.date_input("📅 Rentang Document Date",
    [df["Document Date"].min().date(),df["Document Date"].max().date()])

data=df.copy()

if estate:
    data=data[data["Estate"].astype(str).isin(estate)]
if divisi:
    data=data[data["Divisi"].astype(str).isin(divisi)]

data=data[(data["Document Date"].dt.date>=tanggal[0])&(data["Document Date"].dt.date<=tanggal[1])]

st.subheader("📋 Informasi Lengkap Hasil Pencarian")
st.dataframe(data[["Document Date","Estate","Divisi","quantity","UM"]],use_container_width=True)

data["Bulan"]=data["Document Date"].dt.month_name()
data["Minggu"]="W"+(((data["Document Date"].dt.day-1)//7)+1).astype(str)

bulan=["April","May","June"]

st.subheader("1. Rata-rata Curah Hujan Harian per Estate per Minggu")
weekly=data.groupby(["Bulan","Minggu","Estate"],as_index=False)["quantity"].mean().round(0)
st.plotly_chart(px.line(weekly,x="Minggu",y="quantity",color="Estate",facet_col="Bulan",markers=True),use_container_width=True)

st.subheader("2. Rata-rata Curah Hujan Bulanan per Estate")
monthly=data.groupby(["Bulan","Estate"],as_index=False)["quantity"].mean().round(0)
st.plotly_chart(px.line(monthly,x="Bulan",y="quantity",color="Estate",markers=True,category_orders={"Bulan":bulan}),use_container_width=True)

st.subheader("3. Trend Rata-rata Curah Hujan Estate per Bulan")
st.plotly_chart(px.bar(monthly,x="Bulan",y="quantity",color="Estate",category_orders={"Bulan":bulan}),use_container_width=True)

st.subheader("4. Hari Hujan vs Tidak Hujan")
pie=data.copy()
pie["Status Hari"]=pie["quantity"].apply(lambda x:"Hari Hujan" if x>0 else "Tidak Hujan")
pie=pie.groupby(["Estate","Status Hari"]).size().reset_index(name="Jumlah Hari")
st.plotly_chart(px.pie(pie,names="Status Hari",values="Jumlah Hari",facet_col="Estate"),use_container_width=True)

st.subheader("5. Ranking 3 Besar Curah Hujan Estate")
rank=monthly.groupby("Estate",as_index=False)["quantity"].sum().round(0).sort_values("quantity",ascending=False).head(3)
st.dataframe(rank)

st.subheader("6. Status Kondisi Estate per Bulan")
status=monthly.copy()
status["Total Curah Hujan Bulanan"]=(status["quantity"]*30).round(0)
status["Status"]=status["Total Curah Hujan Bulanan"].apply(lambda x:"Kering" if x<100 else ("Normal" if x<=300 else "Tinggi"))
st.dataframe(status[["Estate","Bulan","Total Curah Hujan Bulanan","Status"]])
