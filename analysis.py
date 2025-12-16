import streamlit as st
import pandas as pd
from scipy import stats

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Survey Analysis", layout="wide")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Settings")

language = st.sidebar.selectbox(
    "🌐 Language / Bahasa",
    ["English", "Bahasa Indonesia"]
)

theme = st.sidebar.radio(
    "🎨 Theme",
    ["Light Mode", "Dark Mode"]
)

# =========================
# APPLY DARK MODE (WORKING)
# =========================
if theme == "Dark Mode":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        h1, h2, h3, h4, h5, h6, p, label {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# =========================
# TEXT DICTIONARY
# =========================
if language == "English":
    title = "📊 Survey Analysis App"
    subtitle = "The Effect of Screen Time on Student Productivity"
    upload_text = "Upload your survey dataset (Excel or CSV)"
    raw_data = "📋 Raw Data Preview"
    desc_stat = "📈 Descriptive Statistics"
    composite = "📊 Composite Score Statistics"
    corr_title = "🔗 Pearson Correlation Analysis"
    interp_title = "🧠 Interpretation"
    scatter = "📉 Scatter Plot"
    x_title = "Screen Time (X_TOTAL)"
    y_title = "Student Productivity (Y_TOTAL)"
else:
    title = "📊 Aplikasi Analisis Survei"
    subtitle = "Pengaruh Screen Time terhadap Produktivitas Mahasiswa"
    upload_text = "Unggah dataset survei (Excel atau CSV)"
    raw_data = "📋 Pratinjau Data"
    desc_stat = "📈 Statistik Deskriptif"
    composite = "📊 Statistik Skor Total"
    corr_title = "🔗 Analisis Korelasi Pearson"
    interp_title = "🧠 Interpretasi"
    scatter = "📉 Diagram Sebar"
    x_title = "Screen Time (X_TOTAL)"
    y_title = "Produktivitas Mahasiswa (Y_TOTAL)"

# =========================
# MAIN PAGE
# =========================
st.title(title)
st.subheader(subtitle)

uploaded_file = st.file_uploader(upload_text, type=["xlsx", "csv"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)

    st.success("✅ Dataset uploaded")

    st.subheader(raw_data)
    st.dataframe(df)

    st.subheader(desc_stat)
    st.dataframe(df.describe())

    st.subheader(composite)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### {x_title}")
        st.write(df["X_TOTAL"].describe())

    with col2:
        st.markdown(f"### {y_title}")
        st.write(df["Y_TOTAL"].describe())

    # =========================
    # CORRELATION
    # =========================
    st.subheader(corr_title)

    r, p = stats.pearsonr(df["X_TOTAL"], df["Y_TOTAL"])

    st.write(f"**Correlation coefficient (r):** {r:.3f}")
    st.write(f"**p-value:** {p:.3f}")

    # =========================
    # INTERPRETATION (FIXED)
    # =========================
    st.subheader(interp_title)

    if abs(r) < 0.3:
        strength = "weak" if language == "English" else "lemah"
    elif abs(r) < 0.6:
        strength = "moderate" if language == "English" else "sedang"
    else:
        strength = "strong" if language == "English" else "kuat"

    direction = "negative" if r < 0 else "positive"

    significance = (
        "statistically significant" if p < 0.05 else "not statistically significant"
        if language == "English"
        else "signifikan secara statistik" if p < 0.05 else "tidak signifikan secara statistik"
    )

    if language == "English":
        st.write(
            f"There is a **{strength} {direction} relationship** between screen time "
            f"and student productivity. The relationship is **{significance}**."
        )
    else:
        st.write(
            f"Terdapat hubungan **{direction} {strength}** antara screen time "
            f"dan produktivitas mahasiswa. Hubungan tersebut **{significance}**."
        )

    # =========================
    # SCATTER PLOT
    # =========================
    st.subheader(scatter)
    st.scatter_chart(
        df[["X_TOTAL", "Y_TOTAL"]].rename(
            columns={"X_TOTAL": x_title, "Y_TOTAL": y_title}
        )
    )

else:
    st.info("⬅️ Upload dataset to start analysis")
