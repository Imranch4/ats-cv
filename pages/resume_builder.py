import streamlit as st

st.set_page_config(page_title="Resume Builder", page_icon="📝", layout="wide")

st.title("📝 Smart Resume Builder")
st.markdown("Create an optimized, ATS-friendly resume tailored to your target roles")

# Resume building form
with st.form("resume_builder"):
    st.subheader("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone")
    
    with col2:
        location = st.text_input("Location")
        linkedin = st.text_input("LinkedIn Profile")
        portfolio = st.text_input("Portfolio/GitHub")
    
    st.subheader("Professional Summary")
    professional_summary = st.text_area(
        "Summary*",
        height=100,
        help="2-3 sentence overview of your professional background and key strengths"
    )
    
    st.subheader("Work Experience")
    st.info("Add your most recent and relevant positions")
    
    # Experience entries
    for i in range(3):  # Allow up to 3 positions
        with st.expander(f"Position {i+1}" if i > 0 else "Current/Most Recent Position", expanded=i==0):
            col1, col2 = st.columns(2)
            
            with col1:
                job_title = st.text_input(f"Job Title {i+1}")
                company = st.text_input(f"Company {i+1}")
            
            with col2:
                start_date = st.text_input(f"Start Date {i+1}", placeholder="MM/YYYY")
                end_date = st.text_input(f"End Date {i+1}", placeholder="MM/YYYY or Present")
            
            responsibilities = st.text_area(
                f"Responsibilities & Achievements {i+1}",
                height=80,
                help="Use bullet points and include metrics where possible"
            )
    
    st.subheader("Skills")
    skills = st.text_area(
        "Technical & Professional Skills",
        height=100,
        help="List your key skills separated by commas"
    )
    
    st.subheader("Education")
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        degree = st.text_input("Degree/Certification")
    
    with col2:
        institution = st.text_input("Institution")
    
    with col3:
        grad_year = st.text_input("Year", placeholder="YYYY")
    
    # Form submission
    submitted = st.form_submit_button("🚀 Generate Optimized Resume")
    
    if submitted:
        if not full_name or not email or not professional_summary:
            st.error("Please fill in required fields (marked with *)")
        else:
            st.success("✅ Resume data captured! Generating optimized version...")
            # Here you would integrate with AI to optimize the resume
            st.info("AI optimization feature would generate improved content here")

# Resume preview section
st.markdown("---")
st.subheader("👀 Resume Preview")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <div style='border: 2px dashed #ccc; padding: 20px; border-radius: 10px; background: white;'>
        <h3 style='color: #3498db;'>{name}</h3>
        <p>{email} | {phone} | {location}</p>
        
        <h4 style='color: #2c3e50;'>Professional Summary</h4>
        <p>{summary}</p>
        
        <h4 style='color: #2c3e50;'>Experience</h4>
        <p>Your experience will appear here...</p>
        
        <h4 style='color: #2c3e50;'>Skills</h4>
        <p>{skills}</p>
    </div>
    """.format(
        name=full_name or "Your Name",
        email=email or "your.email@example.com",
        phone=phone or "Phone number",
        location=location or "Location",
        summary=professional_summary or "Professional summary will appear here",
        skills=skills or "Your skills will appear here"
    ), unsafe_allow_html=True)

with col2:
    st.markdown("### 💡 Tips")
    st.info("""
    - Use action verbs
    - Include metrics
    - Tailor to target role
    - Keep it concise
    - Use relevant keywords
    """)
    
    if st.button("📄 Download Resume"):
        st.success("Download feature would be implemented here")