import streamlit as st
import os

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ Settings & Configuration")

# User profile
st.subheader("👤 User Profile")

with st.form("user_profile"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", value=st.session_state.user_profile.get('name', ''))
        target_role = st.text_input("Target Role", value=st.session_state.user_profile.get('target_role', ''))
    
    with col2:
        experience = st.selectbox(
            "Experience Level",
            ["Entry Level", "Mid Level", "Senior", "Executive"],
            index=0
        )
        industry = st.text_input("Industry", value=st.session_state.user_profile.get('industry', ''))
    
    if st.form_submit_button("💾 Save Profile"):
        st.session_state.user_profile.update({
            'name': name,
            'target_role': target_role,
            'experience_level': experience,
            'industry': industry
        })
        st.success("Profile saved successfully!")

# Application settings
st.subheader("🛠 Application Settings")

col1, col2 = st.columns(2)

with col1:
    st.checkbox("Enable email notifications", value=True)
    st.checkbox("Save analysis history", value=True)
    st.checkbox("Auto-delete uploaded files", value=True)

with col2:
    st.selectbox("Default analysis type", ["ATS Score", "Comprehensive", "Quick Scan"])
    st.slider("Results history limit", 10, 100, 50)

# Data management
st.subheader("📊 Data Management")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🗑️ Clear Analysis History"):
        st.session_state.analysis_history = []
        st.success("Analysis history cleared!")

with col2:
    if st.button("📤 Export All Data"):
        st.info("Export feature would be implemented here")

with col3:
    if st.button("🔄 Reset to Defaults"):
        st.warning("This will reset all settings to defaults")

# API status
st.subheader("🔌 API Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Gemini API", "Connected", "✅")

with col2:
    st.metric("PDF Processing", "Active", "✅")

with col3:
    st.metric("Storage", "Local", "⚡")

# About section
st.subheader("ℹ️ About HireLens")

st.markdown("""
**HireLens v1.0** - AI-Powered Resume Analysis Platform

- **Version**: 1.0.0
- **Last Updated**: December 2024
- **Support**: Contact support@hirelens.com

Built with Streamlit, Google Gemini AI, and ❤️
""")