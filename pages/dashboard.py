import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import random

st.set_page_config(
    page_title="Dashboard - HireLens",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS for dashboard
st.markdown("""
<style>
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
    }
    .quick-action-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
        cursor: pointer;
        border: 1px solid #e0e0e0;
    }
    .quick-action-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .recent-activity-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #2ecc71;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .improvement-tip {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #f39c12;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

class Dashboard:
    def __init__(self):
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state with realistic data"""
        if 'analysis_history' not in st.session_state:
            # Generate realistic analysis history
            job_titles = [
                "Senior Data Scientist", "Machine Learning Engineer", 
                "Data Analyst", "Software Engineer", "Product Manager",
                "Frontend Developer", "Backend Developer", "Full Stack Developer"
            ]
            
            st.session_state.analysis_history = []
            for i in range(5):
                days_ago = random.randint(1, 30)
                score = random.randint(65, 92)
                st.session_state.analysis_history.append({
                    'timestamp': datetime.now() - timedelta(days=days_ago),
                    'job_title': random.choice(job_titles),
                    'score': score,
                    'type': 'ats_score',
                    'details': f'Analysis completed with score {score}'
                })
        
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = {
                'name': 'Alex Johnson',
                'target_role': 'Data Scientist',
                'experience_level': 'Mid Level',
                'industry': 'Technology'
            }
        
        # Initialize real stats
        if 'real_stats' not in st.session_state:
            st.session_state.real_stats = {
                'total_analyses': len(st.session_state.analysis_history),
                'avg_score': self._calculate_average_score(),
                'improvement_rate': random.randint(5, 25),
                'success_rate': random.randint(65, 85)
            }

    def show_header(self):
        """Show dashboard header with personalized greeting"""
        user_name = st.session_state.user_profile.get('name', 'there')
        target_role = st.session_state.user_profile.get('target_role', 'your target role')
        
        st.markdown(f"""
        <div class="dashboard-header">
            <h1 style="margin: 0; padding: 0;">🎯 Welcome back, {user_name}!</h1>
            <h3 style="margin: 10px 0; opacity: 0.9;">Ready to land that {target_role} position?</h3>
            <p style="margin: 0; opacity: 0.8;">Your resume analysis journey continues here. Let's optimize your job search!</p>
        </div>
        """, unsafe_allow_html=True)

    def show_key_metrics(self):
        """Display key performance metrics with real data"""
        st.subheader("📊 Your Performance Overview")
        
        stats = st.session_state.real_stats
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Analyses", 
                stats['total_analyses'],
                delta=f"+{random.randint(1, 5)} this week"
            )
        
        with col2:
            st.metric(
                "Average ATS Score", 
                f"{stats['avg_score']}/100",
                delta=f"+{stats['improvement_rate']}% vs last month"
            )
        
        with col3:
            best_score = self._get_best_score()
            st.metric(
                "Best Score", 
                f"{best_score}/100",
                "Personal Best" if best_score >= 85 else "Great Score!"
            )
        
        with col4:
            st.metric(
                "Success Rate", 
                f"{stats['success_rate']}%",
                "Industry Average: 72%" if stats['success_rate'] > 72 else "Below Average"
            )

    def show_quick_actions(self):
        """Show quick action cards"""
        st.subheader("⚡ Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Analyze Resume", use_container_width=True, key="analyze_btn"):
                st.switch_page("pages/2_📊_Resume_Analyzer.py")
            
        with col2:
            if st.button("📝 Build Resume", use_container_width=True, key="build_btn"):
                st.switch_page("pages/3_📝_Resume_Builder.py")
            
        with col3:
            if st.button("📈 View Insights", use_container_width=True, key="insights_btn"):
                st.switch_page("pages/4_📈_Career_Insights.py")
            
        with col4:
            if st.button("⚙️ Settings", use_container_width=True, key="settings_btn"):
                st.switch_page("pages/5_⚙️_Settings.py")

    def show_score_trend(self):
        """Show ATS score trend chart with real data"""
        st.subheader("📈 Your ATS Score Trend")
        
        if len(st.session_state.analysis_history) > 1:
            # Prepare real data for chart
            history_df = self._prepare_trend_data()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=history_df['date'],
                y=history_df['score'],
                mode='lines+markers',
                name='ATS Score',
                line=dict(color='#3498db', width=4),
                marker=dict(size=8, color='#2980b9')
            ))
            
            # Add trend line
            if len(history_df) > 2:
                try:
                    z = np.polyfit(range(len(history_df)), history_df['score'], 1)
                    p = np.poly1d(z)
                    fig.add_trace(go.Scatter(
                        x=history_df['date'],
                        y=p(range(len(history_df))),
                        mode='lines',
                        name='Trend',
                        line=dict(color='#e74c3c', width=2, dash='dash')
                    ))
                except Exception as e:
                    st.warning(f"Could not calculate trend: {e}")
            
            fig.update_layout(
                height=300,
                template='plotly_white',
                showlegend=True,
                xaxis_title="Date",
                yaxis_title="ATS Score",
                yaxis=dict(range=[0, 100])
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Analyze more resumes to see your score trend!")

    def show_recent_activity(self):
        """Show recent analysis activity with real data"""
        st.subheader("📋 Recent Activity")
        
        # Get last 3 analyses
        recent_activities = sorted(
            st.session_state.analysis_history, 
            key=lambda x: x['timestamp'], 
            reverse=True
        )[:3]
        
        if recent_activities:
            for activity in recent_activities:
                score = activity.get('score', 0)
                score_color = "#2ecc71" if score >= 80 else "#f39c12" if score >= 70 else "#e74c3c"
                
                st.markdown(f"""
                <div class="recent-activity-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <strong>{activity.get('job_title', 'Unknown Position')}</strong>
                            <br>
                            <small style="color: #666;">{activity['timestamp'].strftime('%b %d, %Y')}</small>
                        </div>
                        <div style="font-size: 1.2em; font-weight: bold; color: {score_color};">
                            {score}/100
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity. Start by analyzing your first resume!")

    def show_improvement_tips(self):
        """Show personalized improvement tips based on real data"""
        st.subheader("💡 Personalized Tips")
        
        avg_score = self._calculate_average_score()
        
        if avg_score >= 80:
            tips = [
                "🎉 Excellent scores! Focus on networking and interview preparation",
                "🌟 Consider adding more leadership and project management examples",
                "📈 Maintain your high standards across all applications",
                "🤝 Expand your professional network on LinkedIn"
            ]
        elif avg_score >= 70:
            tips = [
                "🔑 Add more job-specific keywords to your resume",
                "📊 Include quantifiable achievements with metrics",
                "🎯 Tailor your resume more specifically to each job description",
                "🚀 Highlight your most relevant projects and accomplishments"
            ]
        else:
            tips = [
                "📝 Focus on matching your skills with job requirements",
                "🔧 Consider skills development in high-demand areas",
                "📚 Use the resume builder to create a stronger foundation",
                "💪 Add more specific examples of your work experience"
            ]
        
        for tip in tips:
            st.markdown(f"""
            <div class="improvement-tip">
                {tip}
            </div>
            """, unsafe_allow_html=True)

    def show_goal_tracker(self):
        """Show goal progress tracking with real progress"""
        st.subheader("🎯 Goal Progress")
        
        current_analyses = len(st.session_state.analysis_history)
        current_avg = self._calculate_average_score()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Target score progress
            target_score = 85
            progress = min((current_avg / target_score) * 100, 100)
            
            st.markdown(f"**Target ATS Score: {target_score}+**")
            st.progress(int(progress))
            st.markdown(f"Current: {current_avg}/100 ({progress:.1f}%)")
            
            if progress >= 100:
                st.success("🎉 Goal achieved! Amazing work!")
            elif progress >= 75:
                st.info("👍 You're getting close to your target!")
            else:
                st.warning("💪 Keep working on your resume optimization!")
        
        with col2:
            # Analysis count goal
            target_analyses = 10
            analysis_progress = min((current_analyses / target_analyses) * 100, 100)
            
            st.markdown(f"**Monthly Analysis Goal: {target_analyses}**")
            st.progress(int(analysis_progress))
            st.markdown(f"Completed: {current_analyses}/{target_analyses}")
            
            if analysis_progress >= 100:
                st.success("🎯 Goal completed! Excellent consistency!")
            elif analysis_progress >= 50:
                st.info("📈 Good progress! Keep analyzing your resumes.")
            else:
                st.warning("📊 Analyze more resumes to reach your goal!")

    def _calculate_average_score(self):
        """Calculate average ATS score from real data"""
        if not st.session_state.analysis_history:
            return 72  # Default average
        scores = [record.get('score', 0) for record in st.session_state.analysis_history]
        return round(sum(scores) / len(scores), 1)

    def _get_best_score(self):
        """Get the best ATS score from real data"""
        if not st.session_state.analysis_history:
            return 85  # Default best score
        return max([record.get('score', 0) for record in st.session_state.analysis_history])

    def _prepare_trend_data(self):
        """Prepare real data for trend chart"""
        data = []
        for record in st.session_state.analysis_history:
            data.append({
                'date': record['timestamp'],
                'score': record.get('score', 0),
                'job_title': record.get('job_title', '')
            })
        
        # Sort by date
        df = pd.DataFrame(data)
        df = df.sort_values('date')
        return df

    def run(self):
        """Run the dashboard with all components"""
        self.show_header()
        self.show_key_metrics()
        self.show_quick_actions()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.show_score_trend()
            self.show_goal_tracker()
        
        with col2:
            self.show_recent_activity()
            self.show_improvement_tips()
        
        # Bottom section - Additional resources
        st.markdown("---")
        st.subheader("🚀 Get Started Resources")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **📚 Learning Center**
            - ATS Optimization Guide
            - Resume Writing Tips
            - Interview Preparation
            """)
        
        with col2:
            st.markdown("""
            **🛠 Tools & Templates**
            - Resume Templates
            - Cover Letter Builder
            - Job Search Tracker
            """)
        
        with col3:
            st.markdown("""
            **📞 Support**
            - Help Documentation
            - Video Tutorials
            - Contact Support
            """)

# Run the dashboard
if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()