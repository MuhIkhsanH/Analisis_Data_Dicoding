import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_number
import numpy as np

sns.set(style='dark')

try:
    df = pd.read_csv("dashboard/gabungan_imputed.csv")
except FileNotFoundError:
    st.error("File 'gabungan_imputed.csv' tidak ditemukan. Pastikan file berada di direktori yang benar.")
    st.stop()

df["dteday"] = pd.to_datetime(df["dteday"])

df.sort_values(by="dteday", inplace=True)
df.reset_index(drop=True, inplace=True)

min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/MuhIkhsanH/Analisis_Data_Dicoding/main/dashboard/logo.png")
    date_range = st.date_input("Rentang Waktu", min_value=min_date, max_value=max_date, value=[min_date, max_date])
    
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

main_df = df[(df["dteday"] >= str(start_date)) & (df["dteday"] <= str(end_date))]

st.title("🚲 Bike-Sharing Dashboard")

total_rentals = main_df["cnt_day"].sum()
st.metric("Total Rentals", value=format_number(total_rentals, locale="id_ID"))

monthly_weather_df_hour = main_df.groupby([
    main_df['dteday'].dt.to_period('M'),
    'weathersit_hour'
]).agg({'cnt_hour': 'sum'}).reset_index()

monthly_weather_df_hour.rename(columns={'dteday': 'month_period'}, inplace=True)
monthly_weather_df_hour_pivot = monthly_weather_df_hour.pivot_table(
    index='month_period',
    columns='weathersit_hour',
    values='cnt_hour',
    aggfunc='sum'
).fillna(0)

tick_labels = monthly_weather_df_hour_pivot.index.to_timestamp().strftime('%B %Y')

weather_labels = {
    1: "Cerah / Berawan ringan",
    2: "Berkabut / Mendung",
    3: "Hujan ringan / Salju ringan",
    4: "Hujan lebat / Badai / Salju deras"
}

fig, ax = plt.subplots(figsize=(12, 6))
colors = {1: '#72BCD4', 2: '#FFC107', 3: '#FF5733', 4: '#4CAF50'}
for weather_type in monthly_weather_df_hour_pivot.columns:
    ax.plot(
        tick_labels,
        monthly_weather_df_hour_pivot[weather_type],
        marker='o',
        label=weather_labels.get(weather_type, f'Weather {weather_type}'),
        color=colors.get(weather_type),
        linewidth=2
    )

ax.set_title("Penyewaan Berdasarkan Cuaca", fontsize=20)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Number of Rentals (cnt_hour)", fontsize=12)
ax.legend(title='Kondisi Cuaca', loc='upper left')
ax.grid(True)
plt.xticks(rotation=45, ha='right', fontsize=10)
st.pyplot(fig)

monthly_workingday_df = main_df.groupby([
    main_df['dteday'].dt.to_period('M'),
    'workingday_day'
]).agg({'cnt_day': 'sum'}).reset_index()

monthly_workingday_df.rename(columns={'dteday': 'month_period'}, inplace=True)

monthly_workingday_df_pivot = monthly_workingday_df.pivot_table(
    index='month_period',
    columns='workingday_day',
    values='cnt_day',
    aggfunc='sum'
).fillna(0)

tick_labels = monthly_workingday_df_pivot.index.to_timestamp().strftime('%B %Y')

workingday_labels = {0: "Akhir Pekan / Hari Libur", 1: "Hari Kerja"}

fig, ax = plt.subplots(figsize=(12, 6))
colors = {0: '#FF5733', 1: '#72BCD4'}

for wd in monthly_workingday_df_pivot.columns:
    ax.plot(
        tick_labels,
        monthly_workingday_df_pivot[wd],
        marker='o',
        label=workingday_labels.get(wd, f'Workingday {wd}'),
        color=colors.get(wd, None),
        linewidth=2
    )

ax.set_title("Penyewaan Berdasarkan Hari Kerja", fontsize=20)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan (cnt_day)", fontsize=12)
ax.legend(title='Jenis Hari', loc='upper left')
ax.grid(True)

y_min, y_max = ax.get_ylim()
y_ticks = np.linspace(y_min, y_max, num=5)
y_ticks = np.round(y_ticks, -2)
y_ticks = np.unique(y_ticks)
ax.set_yticks(y_ticks)
ax.set_yticklabels([format_number(int(y), locale="id_ID") for y in y_ticks])

plt.xticks(rotation=45, ha='right', fontsize=10)
st.pyplot(fig)

st.caption("© 2025 Bike Rental Dashboard")
