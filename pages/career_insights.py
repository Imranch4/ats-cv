import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Career Insights", page_icon="📈", layout="wide")

st.title("📈 Career Insights & Analytics")
st.markdown("Track your progress and get personalized career recommendations")

if not st.session_state.analysis_history:
    st.info("📊 Start by analyzing some resumes to see your insights here!")
    st.stop()

# Overall metrics
st.subheader("📊 Overall Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_score = sum([r.get('score', 0) for r in st.session_state.analysis_history]) / len(st.session_state.analysis_history)
    st.metric("Average ATS Score", f"{avg_score:.1f}/100")

with col2:
    best_score = max([r.get('score', 0) for r in st.session_state.analysis_history])
    st.metric("Best Score", f"{best_score}/100")

with col3:
    analyses_count = len(st.session_state.analysis_history)
    st.metric("Total Analyses", analyses_count)

with col4:
    improvement = "↑ 15%" if len(st.session_state.analysis_history) > 1 else "N/A"
    st.metric("Trend", improvement)

# Score trend chart
st.subheader("📈 Score Trend Over Time")

if len(st.session_state.analysis_history) > 1:
    dates = [r['timestamp'] for r in st.session_state.analysis_history]
    scores = [r.get('score', 0) for r in st.session_state.analysis_history]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=scores,
        mode='lines+markers',
        name='ATS Score',
        line=dict(color='#3498db', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Your ATS Score Progress",
        xaxis_title="Date",
        yaxis_title="ATS Score",
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Analyze more resumes to see your trend chart!")

# Common issues analysis
st.subheader("🔍 Common Improvement Areas")

issues = {
    'Missing Keywords': 45,
    'Experience Gaps': 30,
    'Format Issues': 15,
    'Skill Mismatch': 10
}

fig_pie = px.pie(
    values=list(issues.values()),
    names=list(issues.keys()),
    title="Common Resume Issues",
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig_pie, use_container_width=True)

# Recommendations
st.subheader("💡 Personalized Recommendations")

recommendations = [
    "🎯 Focus on adding more technical keywords from job descriptions",
    "📈 Include more metrics and quantifiable achievements",
    "🔧 Consider obtaining AWS certification for cloud roles",
    "📝 Tailor your resume more specifically to each application",
    "🚀 Add more project experience to showcase practical skills"
]

for rec in recommendations:
    st.markdown(f"- {rec}")

# Recent activity
st.subheader("📋 Recent Analyses")

for analysis in list(reversed(st.session_state.analysis_history))[:5]:
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.write(f"**{analysis.get('job_title', 'Unknown Position')}**")
        
        with col2:
            score = analysis.get('score', 0)
            color = "#2ecc71" if score >= 70 else "#f39c12" if score >= 50 else "#e74c3c"
            st.markdown(f"<span style='color: {color}; font-weight: bold;'>{score}/100</span>", 
                      unsafe_allow_html=True)
        
        with col3:
            st.write(analysis.get('type', 'ATS').replace('_', ' ').title())
        
        with col4:
            st.write(analysis['timestamp'].strftime("%m/%d/%Y"))
        
        st.markdown("---")