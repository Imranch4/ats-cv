import streamlit as st
from datetime import datetime
import random

class Analytics:
    def __init__(self):
        self.history_limit = 50

    def add_analysis_record(self, job_title, score, analysis_type, details):
        """Add REAL analysis record to history"""
        record = {
            'timestamp': datetime.now(),
            'job_title': job_title,
            'score': score,  # REAL score from AI analysis
            'type': analysis_type,
            'details': details
        }
        
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
        
        st.session_state.analysis_history.append(record)
        
        # Update real stats
        self._update_real_stats()
        
        # Keep history limited
        if len(st.session_state.analysis_history) > self.history_limit:
            st.session_state.analysis_history = st.session_state.analysis_history[-self.history_limit:]

    def _update_real_stats(self):
        """Update real statistics based on actual analysis data"""
        if not st.session_state.analysis_history:
            return
            
        scores = [record['score'] for record in st.session_state.analysis_history]
        
        st.session_state.real_stats = {
            'total_analyses': len(scores),
            'avg_score': sum(scores) / len(scores),
            'best_score': max(scores),
            'success_rate': len([s for s in scores if s >= 70]) / len(scores) * 100,
            'improvement_trend': self._calculate_trend(scores)
        }

    def _calculate_trend(self, scores):
        """Calculate improvement trend from real scores"""
        if len(scores) < 2:
            return 0
            
        recent_avg = sum(scores[-3:]) / min(3, len(scores))
        older_avg = sum(scores[:3]) / min(3, len(scores))
        
        return ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0

    def get_real_stats(self):
        """Get real statistics based on actual analysis data"""
        if 'real_stats' not in st.session_state:
            return {
                'total_analyses': 0,
                'avg_score': 0,
                'best_score': 0,
                'success_rate': 0,
                'improvement_trend': 0
            }
        return st.session_state.real_stats