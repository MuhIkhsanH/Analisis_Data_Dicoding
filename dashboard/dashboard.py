import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load dataset
df = pd.read_csv("gabungan_imputed.csv")

# Pastikan kolom datetime sudah dalam format datetime
datetime_columns = ["dteday"]
df["dteday"] = pd.to_datetime(df["dteday"])

# Urutkan data berdasarkan tanggal
df.sort_values(by="dteday", inplace=True)
df.reset_index(drop=True, inplace=True)

# Menentukan rentang tanggal
min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    st.image("logo.png")  # Logo perusahaan
    date_range = st.date_input("Rentang Waktu", min_value=min_date, max_value=max_date, value=[min_date, max_date])
    
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

# Filter data berdasarkan rentang waktu
main_df = df[(df["dteday"] >= str(start_date)) & (df["dteday"] <= str(end_date))]

# Helper functions
def create_grouped_df(df, group_col, count_col):
    return df.groupby(group_col)[count_col].sum().reset_index()

# Generate DataFrames
daily_rentals_df = create_grouped_df(main_df, "dteday", "cnt_day")
weather_rentals_df = create_grouped_df(main_df, "weathersit_day", "cnt_day")
user_type_df = pd.DataFrame({
    "user_type": ["Casual", "Registered"],
    "count": [main_df["casual_day"].sum(), main_df["registered_day"].sum()]
})

season_hour_df = create_grouped_df(main_df, "season_hour", "cnt_hour")
weathersit_hour_df = create_grouped_df(main_df, "weathersit_hour", "cnt_hour")
workingday_hour_df = create_grouped_df(main_df, "workingday_hour", "cnt_hour")

season_day_df = create_grouped_df(main_df, "season_day", "cnt_day")
weathersit_day_df = create_grouped_df(main_df, "weathersit_day", "cnt_day")
workingday_day_df = create_grouped_df(main_df, "workingday_day", "cnt_day")

season_casual_hour_df = create_grouped_df(main_df, "season_hour", "casual_day")
season_casual_day_df = create_grouped_df(main_df, "season_day", "casual_day")
season_registered_hour_df = create_grouped_df(main_df, "season_hour", "registered_day")
season_registered_day_df = create_grouped_df(main_df, "season_day", "registered_day")

# Dashboard Header
st.header("Bike Rental Dashboard 🚴")

# Daily Rentals Visualization
st.subheader("Daily Bike Rentals")
col1, col2 = st.columns(2)

with col1:
    total_rentals = daily_rentals_df["cnt_day"].sum()
    st.metric("Total Rentals", value=total_rentals)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_rentals_df["dteday"], daily_rentals_df["cnt_day"], marker='o', linewidth=2, color="#90CAF9")
ax.set_xlabel("Date")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# Rentals by Category
st.subheader("Rentals by Different Categories")
def plot_bar_chart(df, x_col, y_col, x_label, y_label, palette):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=x_col, y=y_col, data=df, palette=palette, ax=ax)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    st.pyplot(fig)

plot_bar_chart(weather_rentals_df, "weathersit_day", "cnt_day", "Weather Condition", "Total Rentals", "Blues")
plot_bar_chart(season_hour_df, "season_hour", "cnt_hour", "Season (Hourly)", "Total Rentals", "Greens")
plot_bar_chart(weathersit_hour_df, "weathersit_hour", "cnt_hour", "Weather (Hourly)", "Total Rentals", "Purples")
plot_bar_chart(workingday_hour_df, "workingday_hour", "cnt_hour", "Working Day (Hourly)", "Total Rentals", "Oranges")
plot_bar_chart(season_day_df, "season_day", "cnt_day", "Season (Daily)", "Total Rentals", "Reds")
plot_bar_chart(weathersit_day_df, "weathersit_day", "cnt_day", "Weather (Daily)", "Total Rentals", "Blues")
plot_bar_chart(workingday_day_df, "workingday_day", "cnt_day", "Working Day (Daily)", "Total Rentals", "Oranges")

# Casual vs Registered Users
st.subheader("Casual vs Registered Users")
plot_bar_chart(user_type_df, "user_type", "count", "User Type", "Count", ["#90CAF9", "#F48FB1"])

# Season vs Casual & Registered Users
st.subheader("Season vs Casual & Registered Users")
plot_bar_chart(season_casual_hour_df, "season_hour", "casual_day", "Season (Hourly)", "Casual Rentals", "Greens")
plot_bar_chart(season_casual_day_df, "season_day", "casual_day", "Season (Daily)", "Casual Rentals", "Blues")
plot_bar_chart(season_registered_hour_df, "season_hour", "registered_day", "Season (Hourly)", "Registered Rentals", "Purples")
plot_bar_chart(season_registered_day_df, "season_day", "registered_day", "Season (Daily)", "Registered Rentals", "Oranges")

st.caption("© 2025 Bike Rental Dashboard")
