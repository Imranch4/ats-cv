import streamlit as st
from datetime import datetime
from utils.openai_client import OpenAIClient
from utils.pdf_processor import PDFProcessor
from utils.analytics import Analytics
import re

st.set_page_config(page_title="Resume Analysis", page_icon="📊", layout="wide")

st.title("📊 AI Resume Analysis")
st.markdown("**Real OpenAI-powered analysis** of your resume against job descriptions")

# Initialize services - 🆕 CHANGED HERE
openai_client = OpenAIClient()  # 🆕 CHANGED HERE
pdf_processor = PDFProcessor()
analytics = Analytics()

def extract_score_from_result(result):
    """Extract numerical score from AI response"""
    try:
        patterns = [
            r'Overall Score:\s*(\d{1,3})/100',
            r'Score:\s*(\d{1,3})/100',
            r'(\d{1,3})/100',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, result, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return max(0, min(100, score))
        
        # Estimate from content
        if any(word in result.lower() for word in ['excellent', 'outstanding', 'perfect']):
            return 85
        elif any(word in result.lower() for word in ['good', 'strong', 'solid']):
            return 75
        elif any(word in result.lower() for word in ['average', 'fair', 'adequate']):
            return 65
        elif any(word in result.lower() for word in ['poor', 'weak', 'terrible', 'bad']):
            return 45
        else:
            return 70
            
    except:
        return 70

def extract_job_title(job_description):
    """Extract job title from job description"""
    lines = job_description.split('\n')
    for line in lines[:5]:
        line = line.strip()
        if line and len(line) < 100 and any(word in line.lower() for word in ['engineer', 'developer', 'analyst', 'manager', 'specialist']):
            return line
    return "Analyzed Position"

with st.sidebar:
    st.header("📝 Input Details")
    
    # Connection test - 🆕 CHANGED HERE
    if st.button("🔧 Test OpenAI Connection", key="test_connection"):
        with st.spinner("Testing connection..."):
            success, message = openai_client.test_connection()
            if success:
                st.success(message)
            else:
                st.error(message)
    
    st.markdown("---")
    
    # Job description
    job_desc = st.text_area(
        "Paste Job Description*", 
        height=200,
        placeholder="Copy and paste the complete job description here...",
        help="The AI will compare your resume against this specific job description"
    )
    
    # Resume upload
    resume_file = st.file_uploader(
        "Upload Resume (PDF)*", 
        type=['pdf'],
        help="Upload your resume in PDF format (max 10MB)"
    )
    
    if resume_file:
        is_valid, msg = pdf_processor.validate_pdf(resume_file)
        if is_valid:
            st.success(f"✅ {resume_file.name}")
            st.info(f"📄 File size: {resume_file.size // 1024} KB")
        else:
            st.error(f"❌ {msg}")

# Analysis options
st.subheader("🔍 Choose Analysis Type")

col1, col2, col3, col4 = st.columns(4)

with col1:
    ats_btn = st.button("🤖 ATS Score", use_container_width=True, key="ats_btn")
with col2:
    personality_btn = st.button("👤 Personality Insights", use_container_width=True, key="personality_btn")
with col3:
    keywords_btn = st.button("🔑 Missing Keywords", use_container_width=True, key="keywords_btn")
with col4:
    optimize_btn = st.button("💡 Optimization Tips", use_container_width=True, key="optimize_btn")

# Process analysis
if job_desc and resume_file and (ats_btn or personality_btn or keywords_btn or optimize_btn):
    
    if not job_desc.strip():
        st.error("❌ Please enter a job description")
        st.stop()
    
    # Process PDF
    with st.spinner("🔄 Processing your resume..."):
        resume_images = pdf_processor.convert_pdf_to_images(resume_file)
    
    if not resume_images:
        st.error("❌ Failed to process PDF. Please try another file.")
        st.stop()
    
    # Determine analysis type
    if ats_btn:
        analysis_type = "ats_score"
        st.subheader("🤖 Real ATS Compatibility Analysis")
        st.info("🔍 AI is analyzing your resume content against the job description...")
    elif personality_btn:
        analysis_type = "personality_analysis"
        st.subheader("👤 Professional Profile Analysis")
        st.info("🔍 AI is analyzing your resume style and content...")
    elif keywords_btn:
        analysis_type = "missing_keywords"
        st.subheader("🔑 Missing Keywords Analysis")
        st.info("🔍 AI is comparing keywords between your resume and job description...")
    else:
        analysis_type = "resume_optimization"
        st.subheader("💡 Resume Optimization Suggestions")
        st.info("🔍 AI is identifying improvement opportunities...")
    
    # Perform REAL AI analysis - 🆕 CHANGED HERE
    result = openai_client.analyze_resume(job_desc, resume_images, analysis_type)
    
    if result and not result.startswith("❌"):
        st.markdown("---")
        st.markdown("### 📋 AI Analysis Results")
        
        # Show the actual AI response
        st.markdown(result)
        
        # For ATS scores, extract and save to history
        if analysis_type == "ats_score":
            score = extract_score_from_result(result)
            job_title = extract_job_title(job_desc)
            
            # Save to analytics
            analytics.add_analysis_record(
                job_title=job_title,
                score=score,
                analysis_type=analysis_type,
                details=result[:300]
            )
            
            # Show score with color coding
            if score >= 80:
                st.success(f"🎉 **Overall AI Assessment: STRONG MATCH** ({score}/100)")
            elif score >= 70:
                st.info(f"👍 **Overall AI Assessment: GOOD MATCH** ({score}/100)")
            elif score >= 60:
                st.warning(f"💪 **Overall AI Assessment: FAIR MATCH** ({score}/100)")
            else:
                st.error(f"🚨 **Overall AI Assessment: NEEDS IMPROVEMENT** ({score}/100)")
            
            st.success("✅ Analysis saved to your dashboard!")
        
        # Add download option
        st.download_button(
            "💾 Download Full Analysis",
            data=result,
            file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
        
    else:
        st.error("❌ Analysis failed. Please try again.")
        if result:
            st.error(result)

else:
    # Show instructions
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 How to Use:
        1. **Paste a real job description**
        2. **Upload your actual resume** as PDF
        3. **Choose analysis type**:
           - 🤖 **ATS Score**: Real compatibility analysis
           - 👤 **Personality**: Professional traits
           - 🔑 **Missing Keywords**: Skills gap analysis
           - 💡 **Optimization**: Improvement suggestions
        
        ### ⚡ Powered by OpenAI:
        - **GPT-4 Vision** for text extraction
        - **Real content analysis**
        - **Honest, critical feedback**
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 Real Analysis Features:
        
        **🤖 ATS Scoring:**
        - Skills alignment with job requirements
        - Experience relevance assessment
        - Keyword matching accuracy
        - Formatting and structure analysis
        
        **👤 Personality Insights:**
        - Writing style analysis
        - Professional traits inference
        - Career progression assessment
        
        **💡 Actionable Feedback:**
        - Specific improvement suggestions
        - Missing skills identification
        - Optimization recommendations
        """)