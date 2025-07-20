import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set judul halaman
st.set_page_config(page_title="Dashboard Analisis Tren Topik Penelitian", layout="wide")
st.title("Dashboard Analisis Tren Topik Penelitian Mahasiswa")

# Load data
uploaded_file = st.file_uploader("Upload file Excel hasil clustering", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Tampilkan data mentah
    with st.expander("Lihat Data Mentah"):
        st.write(df.head())

    # Visualisasi: Jumlah Penelitian per Cluster
    st.subheader("Distribusi Jumlah Judul per Cluster")
    cluster_count = df['cluster'].value_counts().sort_index()
    fig1, ax1 = plt.subplots(figsize=(20, 5))
    sns.barplot(x=cluster_count.index, y=cluster_count.values, palette="viridis", ax=ax1)
    ax1.set_xlabel("Cluster")
    ax1.set_ylabel("Jumlah Judul")
    st.pyplot(fig1)

    # Visualisasi tren per Tahun
    st.subheader("Tren Topik Penelitian per Tahun")
    if 'Tahun' in df.columns:
        trend = df.groupby(['Tahun', 'cluster']).size().unstack(fill_value=0)
        fig2, ax2 = plt.subplots(figsize=(20, 5))
        trend.plot(marker='o', ax=ax2)
        plt.title("Tren Topik Penelitian per Tahun")
        plt.xlabel("Tahun")
        plt.ylabel("Jumlah Judul")
        plt.xticks(rotation=45)
        st.pyplot(fig2)
    else:
        st.warning("Kolom 'Tahun' tidak ditemukan dalam dataset.")

#  Word Cloud per Cluster
# ========================
    st.header("☁️ Word Cloud Berdasarkan Cluster")

    selected_cluster = st.selectbox("Pilih Cluster untuk Word Cloud:", sorted(df['cluster'].unique()))

# Ambil judul-judul dari cluster yang dipilih
    filtered_titles = df[df['cluster'] == selected_cluster]['judul_preprocessed']

# Gabungkan semua teks
    text_combined = ' '.join(filtered_titles.astype(str))

# Buat WordCloud
    if text_combined.strip():
        wordcloud = WordCloud(width=400, height=200, background_color='white').generate(text_combined)
        
        fig_wc, ax = plt.subplots(figsize=(20, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig_wc)

    
    # ---- Fitur Pencarian Judul ---- #
    st.subheader("🔍 Cari Judul Skripsi dan Lihat Clusternya")

    judul_input = st.text_input("Masukkan sebagian atau seluruh judul skripsi:")

    if st.button("Cari"):
        if judul_input.strip() == "":
            st.warning("Mohon masukkan judul terlebih dahulu.")
        else:
            df['judul_preprocessed'] = df['judul_preprocessed'].fillna('').astype(str)  # Pastikan semua judul string
            hasil = df[df['judul_preprocessed'].str.lower().str.contains(judul_input.lower())]

            if not hasil.empty:
                st.success(f"Ditemukan {len(hasil)} judul yang cocok:")
                st.dataframe(hasil[['judul_preprocessed', 'cluster']])
    else:
                st.error("Tidak ditemukan judul yang cocok.")

else:   
    st.info("Silakan upload file Excel untuk mulai analisis.")
