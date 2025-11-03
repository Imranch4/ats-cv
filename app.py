import streamlit as st

st.set_page_config(
    page_title="HireLens | AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Redirect to dashboard
st.switch_page("pages/dashboard.py")