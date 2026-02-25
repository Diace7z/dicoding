import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("Bike Sharing Dashboard")

df_day= pd.read_csv("https://drive.usercontent.google.com/download?id=1LIJpFWNiOE9SmS3i-om7DsGhcCCfLGuL&export=download&authuser=0&confirm=t&uuid=f485c1b3-a2f8-401b-8af7-e41f6da3595c&at=APcXIO2jRizjjEvUp8Xtz96IyHlT:1772003092241",
                    index_col=0)
df_day["dteday"] = pd.to_datetime(df_day["dteday"])

st.subheader("Bike Sharing Data by UC Irvine Machine Learning Repository")
st.dataframe(df_day.head())

st.sidebar.header("Filter")


min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

start_date = st.sidebar.date_input(
    "Tanggal Mulai",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "Tanggal Akhir",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)
season_options = list(df_day["season"].unique())+ ["All season"]
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim:",
    options= season_options,
    default=[]
)

if selected_seasons:
    if selected_seasons == "All season":
      df_day = df_day.copy()
    else:
      df_day = df_day[df_day["season"].isin(selected_seasons)]

time_range = ((df_day["dteday"] >= pd.to_datetime(start_date)) &
        (df_day["dteday"] <= pd.to_datetime(end_date))
)

filtered_df = df_day.loc[time_range]

total_rentals = filtered_df["cnt"].sum()
avg_rentals = filtered_df["cnt"].mean()

col1, col2 = st.columns(2)
col1.metric("Total Peminjaman", f"{total_rentals:,.0f}")
col2.metric("Rata-Rata Peminjaman Harian", f"{avg_rentals:,.0f}")


st.subheader("Tren Peminjaman Sepeda 2011-2012")
fig, ax = plt.subplots()
ax.plot(filtered_df["dteday"], filtered_df ["cnt"], linewidth=1, marker="o", markersize=2)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Peminjaman")
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Rata-Rata Peminjaman Berdasarkan Musim")
season_avg = df_day.groupby("season")["cnt"].mean()
fig2, ax2 = plt.subplots()
season_avg.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Rata-Rata Peminjaman")
plt.xticks(rotation=45)
st.pyplot(fig2)

st.subheader("Heatmap Korelasi Peminjaman vs Iklim")

corr_matrix = filtered_df.corr(numeric_only=True)
plt.figure(figsize=(10, 8))
fig3, ax3 = plt.subplots()
sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
)
plt.xticks(rotation=45)

st.pyplot(fig3)




