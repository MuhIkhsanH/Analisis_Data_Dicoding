import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


gabungan_imputed = pd.read_csv("gabungan_imputed.csv")
gabungan_imputed['dteday'] = pd.to_datetime(gabungan_imputed['dteday'])

st.title("Analisis Data Bike Sharing")
tab1, tab2, tab3 = st.tabs(["Pertanyaan Bisnis", "EDA", "Visualisasi & Explanatory Analysis"])

with tab1:
    st.subheader("Pertanyaan Bisnis")
    st.write("1. Bagaimana pengaruh jeni cuaca (clear, cloudy, rainy, snow) terhadap jumlah penyewaan sepeda selama setahun?")
    st.write("2. Bagaimana status hari kerja atau hari libur mempengaruhi jumlah penyewaan sepeda sepanjang tahun?")

with tab2:
    st.subheader("Exploratory Data Analysis")
    st.write("### Contoh Data")
    st.write(gabungan_imputed.sample(5))
    st.write("### Statistik Deskriptif")
    st.write(gabungan_imputed.describe(include="all"))
    st.write("### Cek Unique Value di 'instant'")
    st.write(gabungan_imputed.instant.is_unique)
    
    def display_stats(df, group_col, agg_col):
        stats = df.groupby(by=group_col).agg({agg_col: ["sum", "mean", "max", "min", "std"]}).reset_index()
        stats.columns = [' '.join(col).strip() for col in stats.columns.values]
        st.write(stats)
    
    st.write("### Statistik Berdasarkan Season Hour")
    display_stats(gabungan_imputed, "season_hour", "cnt_hour")
    
    st.write("### Statistik Berdasarkan Weather Hour")
    display_stats(gabungan_imputed, "weathersit_hour", "cnt_hour")
    
    st.write("### Statistik Berdasarkan Working Day Hour")
    display_stats(gabungan_imputed, "workingday_hour", "cnt_hour")
    
    st.write("### Statistik Berdasarkan Season Day")
    display_stats(gabungan_imputed, "season_day", "cnt_day")
    
    st.write("### Statistik Berdasarkan Weathersit Day")
    display_stats(gabungan_imputed, "weathersit_day", "cnt_day")
    
    st.write("### Statistik Berdasarkan Working Day Day")
    display_stats(gabungan_imputed, "workingday_day", "cnt_day")
    
with tab3:
    st.subheader("Visualisasi Data")
    
    st.write("### Penyewaan Berdasarkan Cuaca")
    monthly_weather_df_hour = gabungan_imputed.groupby([
        gabungan_imputed['dteday'].dt.to_period('M'), 'weathersit_hour'
    ]).agg({'cnt_hour': 'sum'}).reset_index()
    monthly_weather_df_hour.rename(columns={'dteday': 'month_period'}, inplace=True)
    monthly_weather_df_hour_pivot = monthly_weather_df_hour.pivot_table(
        index='month_period',
        columns='weathersit_hour',
        values='cnt_hour',
        aggfunc='sum'
    ).fillna(0)
    tick_labels = monthly_weather_df_hour_pivot.index.to_timestamp().strftime('%B %Y')
    colors = {1: '#72BCD4', 2: '#FFC107', 3: '#FF5733', 4: '#4CAF50'}
    plt.figure(figsize=(12, 6))
    for weather_type in monthly_weather_df_hour_pivot.columns:
        plt.plot(
            tick_labels, monthly_weather_df_hour_pivot[weather_type],
            marker='o', label=f'Weather {weather_type}',
            color=colors.get(weather_type), linewidth=2
        )
    plt.title("Penyewaan Berdasarkan Cuaca", fontsize=20)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Number of Rentals (cnt_hour)", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.legend(title='Weather Type', loc='upper left')
    plt.grid(True)
    st.pyplot(plt)
    
    st.write("### Penyewaan Berdasarkan Hari Kerja")
    monthly_workingday_df = gabungan_imputed.groupby([
        gabungan_imputed['dteday'].dt.to_period('M'), 'workingday_day'
    ]).agg({'cnt_day': 'sum'}).reset_index()
    monthly_workingday_df.rename(columns={'dteday': 'month_period'}, inplace=True)
    monthly_workingday_df_pivot = monthly_workingday_df.pivot_table(
        index='month_period',
        columns='workingday_day',
        values='cnt_day',
        aggfunc='sum'
    ).fillna(0)
    tick_labels = monthly_workingday_df_pivot.index.to_timestamp().strftime('%B %Y')
    colors = {0: '#FF5733', 1: '#72BCD4'}
    plt.figure(figsize=(12, 6))
    for wd in monthly_workingday_df_pivot.columns:
        plt.plot(
            tick_labels, monthly_workingday_df_pivot[wd],
            marker='o', label=f'Workingday {wd}',
            color=colors.get(wd, None), linewidth=2
        )
    plt.title("Penyewaan Berdasarkan Hari Kerja", fontsize=20)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Jumlah Penyewaan (cnt_day)", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.ylim(0, 4_000_000)
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1_000_000))
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{int(x):,}".replace(",", ".")))
    plt.legend(title='Status Hari Kerja', loc='upper left')
    plt.grid(True)
    st.pyplot(plt)