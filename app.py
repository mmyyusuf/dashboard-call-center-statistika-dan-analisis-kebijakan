import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# ===== KONFIGURASI PAGE =====
st.set_page_config(
    page_title="Dashboard Call Center 112",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS =====
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ===== FUNGSI KATEGORISASI =====
def categorize_report(row):
    tipe = str(row["tipe laporan"]).strip().upper()
    kategori = str(row["kategori"]).strip().upper()
    
    # Lalu lintas
    if any(x in kategori for x in ["LAKA LANTAS","TRAFFIC LIGHT","KEMACETAN","RAMBU"]):
        return "Lalu Lintas"
    # Kesehatan
    if any(x in kategori for x in ["DARURAT MEDIS","ODGJ","PMKS"]):
        return "Kesehatan"
    # Infrastruktur
    if any(x in kategori for x in ["PJU","JALAN RUSAK","KABEL","PDAM","POHON","BANJIR","SUNGAI","TIANG","OLI"]):
        return "Infrastruktur"
    # Keamanan
    if any(x in kategori for x in ["KRIMINALITAS","KEAMANAN","PARKIR"]):
        return "Keamanan"
    # Kebakaran
    if "KEBAKARAN" in kategori:
        return "Kebakaran"
    # Layanan Publik
    if any(x in kategori for x in ["ADMINISTRASI","REKLAME","BEASISWA","SIMULASI"]):
        return "Layanan Publik"
    # Tipe lainnya
    if tipe == "PRANK": return "Prank"
    if tipe == "GHOST": return "Ghost"
    if tipe == "INFORMATION": return "Informasi"
    
    return "Lain-lain"

# ===== FUNGSI LOAD & PROCESS DATA =====
@st.cache_data
def load_and_process_data():
    try:
        # Load data dari folder data/
        df24 = pd.read_excel("data/LAPORAN INSIDEN CALL CENTER 112 TAHUN 2024.xlsx")
        df25 = pd.read_excel("data/LAPORAN INSIDEN CALLCENTER 112 TAHUN 2025.xlsx")
        
        df24["Tahun"] = 2024
        df25["Tahun"] = 2025
        
        # Standardisasi kolom
        df24.columns = df24.columns.str.strip().str.lower()
        df25.columns = df25.columns.str.strip().str.lower()
        
        # Parse waktu
        df24["waktu lapor"] = pd.to_datetime(df24["waktu lapor"], errors="coerce")
        df25["waktu lapor"] = pd.to_datetime(df25["waktu lapor"], errors="coerce")
        
        # Buat kolom tambahan
        df24["bulan"] = df24["waktu lapor"].dt.to_period("M").astype(str)
        df25["bulan"] = df25["waktu lapor"].dt.to_period("M").astype(str)
        
        df24["month"] = df24["waktu lapor"].dt.month
        df25["month"] = df25["waktu lapor"].dt.month
        
        # Kategorisasi besar
        df24["kategori_besar"] = df24.apply(categorize_report, axis=1)
        df25["kategori_besar"] = df25.apply(categorize_report, axis=1)
        
        # Validitas
        df24["validitas"] = df24["tipe laporan"].astype(str).str.lower().apply(
            lambda x: "Tidak Valid" if x in ["prank", "ghost", "silent call"] else "Valid"
        )
        df25["validitas"] = df25["tipe laporan"].astype(str).str.lower().apply(
            lambda x: "Tidak Valid" if x in ["prank", "ghost", "silent call"] else "Valid"
        )
        
        return df24, df25, None
    except FileNotFoundError as e:
        return None, None, "File tidak ditemukan. Pastikan file Excel ada di folder 'data/'"
    except Exception as e:
        return None, None, f"Error: {str(e)}"

# ===== LOAD DATA =====
df24, df25, error = load_and_process_data()

if error:
    st.error(f"❌ {error}")
    st.info("""
    ### 📁 Struktur folder yang dibutuhkan:
    ```
    callcenter-dashboard/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    └── data/
        ├── LAPORAN INSIDEN CALL CENTER 112 TAHUN 2024.xlsx
        └── LAPORAN INSIDEN CALLCENTER 112 TAHUN 2025.xlsx
    ```
    """)
    st.stop()

# Combine data
df_all = pd.concat([df24, df25], ignore_index=True)

# ===== SIDEBAR =====
st.sidebar.markdown("# 📞 Dashboard Call Center 112")
st.sidebar.markdown("**Analisis Laporan Call Center 112 Surabaya**")
st.sidebar.markdown(f"📊 **Total Data**: {len(df_all):,} laporan")
st.sidebar.markdown("---")

# Filters
st.sidebar.markdown("### 🔍 Filter Data")

tahun_filter = st.sidebar.multiselect(
    "Pilih Tahun:",
    options=[2024, 2025],
    default=[2024, 2025]
)

kategori_options = sorted(df_all["kategori_besar"].unique())
kategori_filter = st.sidebar.multiselect(
    "Pilih Kategori Besar:",
    options=kategori_options,
    default=kategori_options
)

validitas_filter = st.sidebar.multiselect(
    "Pilih Validitas:",
    options=["Valid", "Tidak Valid"],
    default=["Valid", "Tidak Valid"]
)

# Apply filters
df_filtered = df_all[
    (df_all["Tahun"].isin(tahun_filter)) &
    (df_all["kategori_besar"].isin(kategori_filter)) &
    (df_all["validitas"].isin(validitas_filter))
]

# ===== MAIN CONTENT =====
st.markdown('<p class="main-header">📊 Dashboard Analisis Laporan Call Center 112</p>', unsafe_allow_html=True)
st.markdown("**Statistika Sains Data & Analisis Kebijakan**")
st.markdown("---")

# ===== TABS =====
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview", 
    "📊 Distribusi & Perbandingan", 
    "📉 Tren Waktu",
    "🎯 Validitas Data",
    "💡 Insight & Rekomendasi"
])

# ===== TAB 1: OVERVIEW =====
with tab1:
    st.markdown("## 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_laporan = len(df_filtered)
        st.metric("Total Laporan", f"{total_laporan:,}")
    
    with col2:
        valid_count = len(df_filtered[df_filtered["validitas"] == "Valid"])
        valid_pct = (valid_count/total_laporan*100) if total_laporan > 0 else 0
        st.metric("Laporan Valid", f"{valid_count:,}", f"{valid_pct:.1f}%")
    
    with col3:
        if 2024 in tahun_filter and 2025 in tahun_filter:
            count_24 = len(df24)
            count_25 = len(df25)
            growth = ((count_25 - count_24) / count_24 * 100) if count_24 > 0 else 0
            st.metric("Growth Rate", f"{growth:+.1f}%", delta=f"{count_25-count_24:+,} laporan")
        else:
            st.metric("Growth Rate", "N/A")
    
    with col4:
        top_kategori = df_filtered["kategori_besar"].value_counts().index[0] if len(df_filtered) > 0 else "N/A"
        st.metric("Kategori Terbanyak", top_kategori)
    
    st.markdown("---")
    
    # Distribusi per tahun
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Distribusi Laporan per Tahun")
        year_dist = df_filtered["Tahun"].value_counts().sort_index()
        fig = px.bar(
            x=year_dist.index, 
            y=year_dist.values,
            labels={'x': 'Tahun', 'y': 'Jumlah Laporan'},
            color=year_dist.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Proporsi Validitas")
        valid_dist = df_filtered["validitas"].value_counts()
        fig = px.pie(
            values=valid_dist.values,
            names=valid_dist.index,
            color_discrete_sequence=['#2ecc71', '#e74c3c']
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# ===== TAB 2: DISTRIBUSI & PERBANDINGAN =====
with tab2:
    st.markdown("## 📊 Distribusi dan Perbandingan Kategori")
    
    # Top 10 Kategori Besar
    st.markdown("### 🏆 Top 10 Kategori Besar")
    top10_cat = df_filtered["kategori_besar"].value_counts().head(10)
    fig = px.bar(
        x=top10_cat.values,
        y=top10_cat.index,
        orientation='h',
        labels={'x': 'Jumlah Laporan', 'y': 'Kategori'},
        color=top10_cat.values,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Perbandingan 2024 vs 2025
    if 2024 in tahun_filter and 2025 in tahun_filter:
        st.markdown("### 📊 Perbandingan Kategori Besar: 2024 vs 2025")
        
        count24 = df24["kategori_besar"].value_counts()
        count25 = df25["kategori_besar"].value_counts()
        
        comparison = pd.DataFrame({
            "2024": count24,
            "2025": count25
        }).fillna(0)
        
        comparison["Total"] = comparison["2024"] + comparison["2025"]
        top10_idx = comparison.sort_values("Total", ascending=False).head(10).index
        
        plot_data = comparison.loc[top10_idx, ["2024", "2025"]]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='2024', x=plot_data.index, y=plot_data["2024"], marker_color='#3498db'))
        fig.add_trace(go.Bar(name='2025', x=plot_data.index, y=plot_data["2025"], marker_color='#e74c3c'))
        
        fig.update_layout(
            barmode='group',
            xaxis_title="Kategori",
            yaxis_title="Jumlah Laporan",
            height=500,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Tipe Laporan Detail
    st.markdown("### 📋 Distribusi Tipe Laporan")
    tipe_dist = df_filtered["tipe laporan"].value_counts().head(15)
    fig = px.bar(
        x=tipe_dist.index,
        y=tipe_dist.values,
        labels={'x': 'Tipe Laporan', 'y': 'Jumlah'},
        color=tipe_dist.values,
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# ===== TAB 3: TREN WAKTU =====
with tab3:
    st.markdown("## 📉 Analisis Tren Temporal")
    
    # Tren Bulanan Total
    st.markdown("### 📅 Tren Bulanan Total Laporan")
    
    monthly_data = df_filtered.groupby(["bulan", "Tahun"]).size().reset_index(name="count")
    
    fig = px.line(
        monthly_data,
        x="bulan",
        y="count",
        color="Tahun",
        markers=True,
        labels={'bulan': 'Bulan', 'count': 'Jumlah Laporan'},
        color_discrete_map={2024: '#3498db', 2025: '#e74c3c'}
    )
    fig.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Tren Top 4 Kategori
    st.markdown("### 🏆 Tren Top 4 Kategori Besar")
    
    top4_cat = df_all["kategori_besar"].value_counts().head(4).index
    df_top4 = df_filtered[df_filtered["kategori_besar"].isin(top4_cat)]
    
    trend_data = df_top4.groupby(["bulan", "kategori_besar"]).size().reset_index(name="count")
    
    fig = px.line(
        trend_data,
        x="bulan",
        y="count",
        color="kategori_besar",
        markers=True,
        labels={'bulan': 'Bulan', 'count': 'Jumlah Laporan', 'kategori_besar': 'Kategori'}
    )
    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Heatmap
    st.markdown("### 🔥 Heatmap Laporan per Bulan & Kategori")
    
    heatmap_data = df_filtered.groupby(["bulan", "kategori_besar"]).size().reset_index(name="count")
    heatmap_pivot = heatmap_data.pivot(index="kategori_besar", columns="bulan", values="count").fillna(0)
    
    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x="Bulan", y="Kategori", color="Jumlah"),
        color_continuous_scale="YlOrRd",
        aspect="auto"
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

# ===== TAB 4: VALIDITAS DATA =====
with tab4:
    st.markdown("## 🎯 Analisis Validitas Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Distribusi Validitas 2024")
        valid_24 = df24["validitas"].value_counts()
        fig = px.pie(
            values=valid_24.values,
            names=valid_24.index,
            color_discrete_sequence=['#2ecc71', '#e74c3c']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### ✅ Distribusi Validitas 2025")
        valid_25 = df25["validitas"].value_counts()
        fig = px.pie(
            values=valid_25.values,
            names=valid_25.index,
            color_discrete_sequence=['#2ecc71', '#e74c3c']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detail Laporan Tidak Valid
    st.markdown("### ❌ Detail Laporan Tidak Valid")
    
    invalid_data = df_filtered[df_filtered["validitas"] == "Tidak Valid"]
    invalid_type = invalid_data["tipe laporan"].value_counts()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            x=invalid_type.index,
            y=invalid_type.values,
            labels={'x': 'Tipe', 'y': 'Jumlah'},
            color=invalid_type.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Statistik")
        total_invalid = len(invalid_data)
        pct_invalid = (total_invalid/len(df_filtered)*100) if len(df_filtered) > 0 else 0
        
        st.metric("Total Tidak Valid", f"{total_invalid:,}")
        st.metric("Persentase", f"{pct_invalid:.2f}%")
        
        if 2024 in tahun_filter and 2025 in tahun_filter:
            invalid_24 = len(df24[df24["validitas"] == "Tidak Valid"])
            invalid_25 = len(df25[df25["validitas"] == "Tidak Valid"])
            delta_invalid = invalid_25 - invalid_24
            st.metric("Perubahan 2024→2025", f"{delta_invalid:+,}")

# ===== TAB 5: INSIGHT & REKOMENDASI =====
with tab5:
    st.markdown("## 💡 Insight & Rekomendasi Kebijakan")
    
    # Insight Otomatis
    if 2024 in tahun_filter and 2025 in tahun_filter:
        st.markdown("### 📈 Perubahan Signifikan (2024 → 2025)")
        
        sum24 = df24["kategori_besar"].value_counts()
        sum25 = df25["kategori_besar"].value_counts()
        delta = (sum25 - sum24).fillna(sum25).sort_values(ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔺 Top 5 Kategori Meningkat")
            top_naik = delta.head(5)
            for idx, (cat, val) in enumerate(top_naik.items(), 1):
                pct = (val/sum24.get(cat, 1)*100) if cat in sum24.index else 0
                st.markdown(f"**{idx}. {cat}**: +{val:.0f} laporan ({pct:+.1f}%)")
        
        with col2:
            st.markdown("#### 🔻 Top 5 Kategori Menurun")
            top_turun = delta.tail(5).sort_values()
            for idx, (cat, val) in enumerate(top_turun.items(), 1):
                pct = (val/sum24.get(cat, 1)*100) if cat in sum24.index else 0
                st.markdown(f"**{idx}. {cat}**: {val:.0f} laporan ({pct:.1f}%)")
    
    st.markdown("---")
    
    # Rekomendasi Kebijakan
    st.markdown("### 🎯 Rekomendasi Kebijakan")
    
    top5_overall = df_all["kategori_besar"].value_counts().head(5)
    
    rekomendasi = {
        "Lalu Lintas": "🚦 Tingkatkan koordinasi dengan Dinas Perhubungan untuk manajemen lalu lintas dan perbaikan traffic light",
        "Infrastruktur": "🏗️ Alokasikan anggaran prioritas untuk perbaikan jalan, PJU, dan infrastruktur dasar",
        "Kesehatan": "🏥 Perkuat koordinasi dengan Dinas Kesehatan dan rumah sakit untuk respon darurat medis",
        "Keamanan": "👮 Tingkatkan patroli dan koordinasi dengan kepolisian untuk antisipasi kriminalitas",
        "Kebakaran": "🚒 Evaluasi waktu respon dan kebutuhan armada damkar di zona rawan kebakaran",
        "Layanan Publik": "📋 Optimalkan sistem informasi publik dan pelayanan administrasi",
        "Prank": "⚠️ Implementasi sanksi tegas dan edukasi masyarakat tentang bahaya prank call",
        "Ghost": "📞 Evaluasi sistem teknis call center untuk mengurangi ghost call",
        "Informasi": "ℹ️ Perkuat fungsi layanan informasi dan call center sebagai pusat informasi publik"
    }
    
    for idx, (cat, count) in enumerate(top5_overall.items(), 1):
        pct = count/len(df_all)*100
        st.markdown(f"""
        <div class="insight-box">
            <h4>{idx}. {cat} ({count:,} laporan - {pct:.1f}%)</h4>
            <p>{rekomendasi.get(cat, '📌 Evaluasi dan monitoring berkala diperlukan')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Download Data
    st.markdown("### 📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Data Filtered (CSV)",
            data=csv,
            file_name="call_center_filtered.csv",
            mime="text/csv"
        )
    
    with col2:
        summary_stats = df_filtered.groupby("kategori_besar").agg({
            "kategori_besar": "count"
        }).rename(columns={"kategori_besar": "jumlah"})
        
        csv_summary = summary_stats.to_csv().encode('utf-8')
        st.download_button(
            label="📊 Download Summary Statistics (CSV)",
            data=csv_summary,
            file_name="summary_statistics.csv",
            mime="text/csv"
        )