import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ---------------------------
# Setup Path dan Load Dataset
# ---------------------------
# Dapatkan direktori tempat script ini berada (folder dashboard)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load dataset gabungan_imputed.csv (pastikan nama file sesuai dengan yang ada)
gabungan_path = os.path.join(BASE_DIR, "gabungan_imputed.csv")
gabungan_imputed = pd.read_csv(gabungan_path)
gabungan_imputed['dteday'] = pd.to_datetime(gabungan_imputed['dteday'])

# Path ke dataset day dan hour (folder data berada satu level di atas folder dashboard)
DAY_CSV_PATH = os.path.join(BASE_DIR, "..", "data", "day.csv")
HOUR_CSV_PATH = os.path.join(BASE_DIR, "..", "data", "hour.csv")

# Load dataset day dan hour
day_df = pd.read_csv(DAY_CSV_PATH)
hour_df = pd.read_csv(HOUR_CSV_PATH)
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# ---------------------------
# Tampilan Utama dengan Streamlit
# ---------------------------
st.title("Analisis Data Bike Sharing")

# Membuat 5 tab: Pertanyaan Bisnis, EDA, Visualisasi, Lihat Dataset, Filter Data
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Pertanyaan Bisnis", 
    "EDA", 
    "Visualisasi & Explanatory Analysis", 
    "Lihat Dataset", 
    "Filter Data"
])

# ----------------------
# Tab 1: Pertanyaan Bisnis
# ----------------------
with tab1:
    st.subheader("Pertanyaan Bisnis")
    st.write("1. Bagaimana pengaruh jenis cuaca (clear, cloudy, rainy, snow) terhadap jumlah penyewaan sepeda selama setahun?")
    st.write("2. Bagaimana status hari kerja atau hari libur mempengaruhi jumlah penyewaan sepeda sepanjang tahun?")

# ----------------------
# Tab 2: Exploratory Data Analysis (EDA)
# ----------------------
with tab2:
    st.subheader("Exploratory Data Analysis - Gabungan Imputed Data")
    st.write("#### Contoh Data")
    st.write(gabungan_imputed.sample(5))
    st.write("#### Statistik Deskriptif")
    st.write(gabungan_imputed.describe(include="all"))
    st.write("#### Cek Unique Value di kolom 'instant'")
    st.write(gabungan_imputed.instant.is_unique)
    
    def display_stats(df, group_col, agg_col):
        stats = df.groupby(by=group_col).agg({agg_col: ["sum", "mean", "max", "min", "std"]}).reset_index()
        stats.columns = [' '.join(col).strip() for col in stats.columns.values]
        st.write(stats)
    
    st.write("##### Statistik Berdasarkan Season Hour")
    display_stats(gabungan_imputed, "season_hour", "cnt_hour")
    
    st.write("##### Statistik Berdasarkan Weather Hour")
    display_stats(gabungan_imputed, "weathersit_hour", "cnt_hour")
    
    st.write("##### Statistik Berdasarkan Working Day Hour")
    display_stats(gabungan_imputed, "workingday_hour", "cnt_hour")
    
    st.write("##### Statistik Berdasarkan Season Day")
    display_stats(gabungan_imputed, "season_day", "cnt_day")
    
    st.write("##### Statistik Berdasarkan Weathersit Day")
    display_stats(gabungan_imputed, "weathersit_day", "cnt_day")
    
    st.write("##### Statistik Berdasarkan Working Day Day")
    display_stats(gabungan_imputed, "workingday_day", "cnt_day")
    
    st.markdown("---")
    
    st.subheader("Exploratory Data Analysis - Day Data")
    st.write("#### Contoh Data")
    st.write(day_df.sample(5))
    st.write("#### Statistik Deskriptif")
    st.write(day_df.describe(include="all"))

# ----------------------
# Tab 3: Visualisasi & Explanatory Analysis
# ----------------------
with tab3:
    st.subheader("Visualisasi Data - Gabungan Imputed")
    # Visualisasi Penyewaan Berdasarkan Cuaca (data per jam)
    st.write("##### Penyewaan Berdasarkan Cuaca (Hour Data)")
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
    plt.title("Penyewaan Berdasarkan Cuaca (Gabungan Imputed)", fontsize=20)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Number of Rentals (cnt_hour)", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.legend(title='Weather Type', loc='upper left')
    plt.grid(True)
    st.pyplot(plt)
    
    # Visualisasi Penyewaan Berdasarkan Hari Kerja (data per hari)
    st.write("##### Penyewaan Berdasarkan Hari Kerja (Day Data)")
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
    plt.title("Penyewaan Berdasarkan Hari Kerja (Gabungan Imputed)", fontsize=20)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Jumlah Penyewaan (cnt_day)", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.ylim(0, 4_000_000)
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1_000_000))
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{int(x):,}".replace(",", ".")))
    plt.legend(title='Status Hari Kerja', loc='upper left')
    plt.grid(True)
    st.pyplot(plt)
    
    st.markdown("---")
    st.subheader("Visualisasi Data - Day Data")
    # Visualisasi Penyewaan Berdasarkan Cuaca (day_df)
    st.write("##### Penyewaan Berdasarkan Cuaca (Day Data)")
    monthly_weather_df = day_df.groupby([
        day_df['dteday'].dt.to_period('M'), 'weathersit'
    ]).agg({'cnt': 'sum'}).reset_index()
    monthly_weather_df.rename(columns={'dteday': 'month_period'}, inplace=True)
    monthly_weather_df_pivot = monthly_weather_df.pivot_table(
        index='month_period',
        columns='weathersit',
        values='cnt',
        aggfunc='sum'
    ).fillna(0)
    tick_labels = monthly_weather_df_pivot.index.to_timestamp().strftime('%B %Y')
    colors = {1: '#72BCD4', 2: '#FFC107', 3: '#FF5733', 4: '#4CAF50'}
    plt.figure(figsize=(14, 7))
    for weather_type in monthly_weather_df_pivot.columns:
        plt.plot(
            tick_labels, monthly_weather_df_pivot[weather_type],
            marker='o', label=f'Weather {weather_type}',
            color=colors.get(weather_type), linewidth=3
        )
    plt.title("Penyewaan Berdasarkan Cuaca (Day Data)", fontsize=22)
    plt.xlabel("Month", fontsize=14)
    plt.ylabel("Number of Rentals (cnt)", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.legend(title='Weather Type', loc='upper left')
    plt.grid(True)
    st.pyplot(plt)
    
    # Visualisasi Penyewaan Berdasarkan Hari Kerja (day_df)
    st.write("##### Penyewaan Berdasarkan Hari Kerja (Day Data)")
    monthly_workingday_df = day_df.groupby([
        day_df['dteday'].dt.to_period('M'), 'workingday'
    ]).agg({'cnt': 'sum'}).reset_index()
    monthly_workingday_df.rename(columns={'dteday': 'month_period'}, inplace=True)
    monthly_workingday_df_pivot = monthly_workingday_df.pivot_table(
        index='month_period',
        columns='workingday',
        values='cnt',
        aggfunc='sum'
    ).fillna(0)
    tick_labels = monthly_workingday_df_pivot.index.to_timestamp().strftime('%B %Y')
    colors = {0: '#FF5733', 1: '#72BCD4'}
    plt.figure(figsize=(14, 7))
    for wd in monthly_workingday_df_pivot.columns:
        plt.plot(
            tick_labels, monthly_workingday_df_pivot[wd],
            marker='o', label=f'Workingday {wd}',
            color=colors.get(wd, None), linewidth=3
        )
    plt.title("Penyewaan Berdasarkan Hari Kerja (Day Data)", fontsize=22)
    plt.xlabel("Month", fontsize=14)
    plt.ylabel("Jumlah Penyewaan (cnt)", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.ylim(0, max(monthly_workingday_df_pivot.max()) * 1.1)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{int(x):,}".replace(",", ".")))
    plt.legend(title='Status Hari Kerja', loc='upper left')
    plt.grid(True)
    st.pyplot(plt)

# ----------------------
# Tab 4: Lihat Dataset
# ----------------------
with tab4:
    st.subheader("Lihat Dataset")
    selected_dataset = st.selectbox("Pilih Dataset", ["day.csv", "hour.csv"])
    if selected_dataset == "day.csv":
        df = day_df
    else:
        df = hour_df
    st.write(df)

# ----------------------
# Tab 5: Filter Data
# ----------------------
with tab5:
    st.subheader("Filter Data")
    
    # Filter untuk day.csv
    st.write("Gunakan filter di bawah untuk melihat subset data berdasarkan day.csv.")
    min_date_day = day_df['dteday'].min().date()
    max_date_day = day_df['dteday'].max().date()
    start_date_day, end_date_day = st.slider(
        "Pilih Rentang Tanggal (Day Data)", 
        min_value=min_date_day, 
        max_value=max_date_day, 
        value=(min_date_day, max_date_day),
        key="day_slider"
    )
    filtered_day_df = day_df[
        (day_df['dteday'] >= pd.Timestamp(start_date_day)) & 
        (day_df['dteday'] <= pd.Timestamp(end_date_day))
    ]
    st.write(filtered_day_df)
    
    st.markdown("---")
    
    # Filter untuk hour.csv
    st.write("Gunakan filter di bawah untuk melihat subset data berdasarkan hour.csv.")
    min_date_hour = hour_df['dteday'].min().date()
    max_date_hour = hour_df['dteday'].max().date()
    start_date_hour, end_date_hour = st.slider(
        "Pilih Rentang Tanggal (Hour Data)", 
        min_value=min_date_hour, 
        max_value=max_date_hour, 
        value=(min_date_hour, max_date_hour),
        key="hour_slider"
    )
    filtered_hour_df = hour_df[
        (hour_df['dteday'] >= pd.Timestamp(start_date_hour)) & 
        (hour_df['dteday'] <= pd.Timestamp(end_date_hour))
    ]
    st.write(filtered_hour_df)
