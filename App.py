import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="OrbitMe - Life Management System",
    layout="wide",
    page_icon="🔮",
    initial_sidebar_state="expanded"
)

# Enhanced Modern CSS with better colors and animations
st.markdown("""
<style>
    /* Main styling with sophisticated gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #2c3e50 100%);
        min-height: 100vh;
        background-attachment: fixed;
    }
    
    /* Header styling */
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, #FFFFFF, #E0E7FF, #A5B4FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.1);
        animation: headerGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes headerGlow {
        from { filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.3)); }
        to { filter: drop-shadow(0 0 20px rgba(118, 75, 162, 0.5)); }
    }
    
    .sub-header {
        text-align: center;
        color: #E0E7FF;
        font-size: 1.4rem;
        margin-bottom: 1rem;
        font-weight: 300;
        letter-spacing: 1px;
        opacity: 0.9;
    }
    
    .description {
        text-align: center;
        color: #CBD5E1;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        font-weight: 400;
        line-height: 1.6;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        opacity: 0.9;
    }
    
    /* Enhanced glass morphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2.5rem;
        margin: 0.5rem 0;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: 0.6s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.25);
        background: rgba(255, 255, 255, 0.12);
    }
    
    /* Enhanced stats cards */
    .stats-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    
    .stats-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .stats-card:hover::after {
        opacity: 1;
    }
    
    .stats-card:hover {
        transform: translateY(-6px) scale(1.03);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    .stats-number {
        font-size: 2.8rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0.5rem 0;
        text-shadow: 0 2px 15px rgba(0,0,0,0.2);
        background: linear-gradient(45deg, #FFFFFF, #E0E7FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stats-label {
        color: #E0E7FF;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
        opacity: 0.8;
    }
    
    /* Enhanced navigation cards */
    .nav-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        cursor: default;
        height: 100%;
        position: relative;
        overflow: hidden;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .nav-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #A5B4FC);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .nav-card:hover::before {
        transform: scaleX(1);
    }
    
    .nav-card:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.35);
        border-color: rgba(255, 255, 255, 0.25);
    }
    
    .nav-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #FFFFFF;
        filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));
        transition: all 0.4s ease;
    }
    
    .nav-card:hover .nav-icon {
        transform: scale(1.15);
        filter: drop-shadow(0 8px 20px rgba(0,0,0,0.4));
    }
    
    .nav-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.75rem;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .nav-card:hover .nav-title {
        background: linear-gradient(45deg, #FFFFFF, #E0E7FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .nav-description {
        color: #E0E7FF;
        font-size: 0.9rem;
        line-height: 1.4;
        opacity: 0.9;
        transition: all 0.3s ease;
    }
    
    .nav-card:hover .nav-description {
        opacity: 1;
        color: #FFFFFF;
    }
    
    /* Enhanced section headers */
    .section-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 3rem 0 2rem 0;
        text-align: center;
        text-shadow: 0 4px 15px rgba(0,0,0,0.3);
        position: relative;
        animation: slideIn 1s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -12px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #A5B4FC);
        border-radius: 2px;
        animation: expandWidth 1s ease-out 0.5s both;
    }
    
    @keyframes expandWidth {
        from { width: 0; }
        to { width: 80px; }
    }
    
    /* Enhanced divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        margin: 2.5rem 0;
        position: relative;
    }
    
    .custom-divider::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 1px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 1px;
    }
    
    /* Floating animation for cards */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .floating {
        animation: float 6s ease-in-out infinite;
    }
    
    /* Pulse animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 3s ease-in-out infinite;
    }
    
    /* Consistent card heights */
    .feature-card-content {
        min-height: 260px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)

# Load sample data for dashboard preview
@st.cache_data
def load_sample_data():
    health_path = './data/health_data.csv'
    work_path = './data/work_data.csv'
    
    health_df = pd.read_csv(health_path) if os.path.exists(health_path) else pd.DataFrame()
    work_df = pd.read_csv(work_path) if os.path.exists(work_path) else pd.DataFrame()
    
    return health_df, work_df

# Main header with enhanced animations and description
st.markdown("""
<div style="padding: 3rem 0 1.5rem 0;">
    <div class="main-header floating">OrbitMe</div>
    <div class="sub-header">Intelligent Life Management Platform</div>
    <div class="description">
        A comprehensive system designed to harmonize your personal and professional life through 
        data-driven insights, intelligent tracking, and actionable analytics. Monitor your wellness, 
        optimize productivity, and achieve your goals with precision.
    </div>
</div>
""", unsafe_allow_html=True)

# Quick Stats Section with enhanced design
st.markdown('<div class="section-header">Performance Dashboard</div>', unsafe_allow_html=True)

try:
    health_df, work_df = load_sample_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_health = len(health_df) if not health_df.empty else 0
        st.markdown(f'''
        <div class="stats-card pulse">
            <div class="stats-label">Health Records</div>
            <div class="stats-number">{total_health}</div>
            <div style="color: #E0E7FF; font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;">Days Tracked</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        total_tasks = len(work_df) if not work_df.empty else 0
        completed_tasks = work_df[work_df['Status'] == 'Completed'].shape[0] if not work_df.empty else 0
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        st.markdown(f'''
        <div class="stats-card pulse" style="animation-delay: 0.2s;">
            <div class="stats-label">Task Completion</div>
            <div class="stats-number">{completion_rate:.0f}%</div>
            <div style="color: #E0E7FF; font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;">{completed_tasks}/{total_tasks} Tasks</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        if not health_df.empty:
            avg_mood = health_df['Mood'].mean() if 'Mood' in health_df.columns else 0
            avg_steps = health_df['Steps'].mean() if 'Steps' in health_df.columns else 0
        else:
            avg_mood = avg_steps = 0
            
        st.markdown(f'''
        <div class="stats-card pulse" style="animation-delay: 0.4s;">
            <div class="stats-label">Wellness Score</div>
            <div class="stats-number">{avg_mood:.1f}</div>
            <div style="color: #E0E7FF; font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;">{avg_steps:,.0f} Avg Steps</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        if not work_df.empty and 'Hours Spent' in work_df.columns:
            total_hours = work_df['Hours Spent'].sum()
        else:
            total_hours = 0
            
        st.markdown(f'''
        <div class="stats-card pulse" style="animation-delay: 0.6s;">
            <div class="stats-label">Productivity</div>
            <div class="stats-number">{total_hours}</div>
            <div style="color: #E0E7FF; font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;">Hours Invested</div>
        </div>
        ''', unsafe_allow_html=True)

except:
    # Show placeholder stats when no data
    col1, col2, col3, col4 = st.columns(4)
    
    placeholder_stats = [
        ("Health Records", "0", "Start Tracking"),
        ("Task Completion", "0%", "Add Tasks"),
        ("Wellness Score", "-", "Monitor Health"), 
        ("Productivity", "-", "Track Progress")
    ]
    
    for i, (label, number, subtitle) in enumerate(placeholder_stats):
        with [col1, col2, col3, col4][i]:
            st.markdown(f'''
            <div class="stats-card">
                <div class="stats-label">{label}</div>
                <div class="stats-number">{number}</div>
                <div style="color: #E0E7FF; font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;">{subtitle}</div>
            </div>
            ''', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Features Section with enhanced glass morphism and consistent heights
st.markdown('<div class="section-header">Core Capabilities</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

features = [
    ("📊", "Analytics Dashboard", "Comprehensive data visualization and performance tracking with interactive charts and personalized insights for informed decision-making."),
    ("⚡", "Task Management", "Advanced project organization with priority management, progress tracking, deadline monitoring, and productivity analytics for optimal performance."),
    ("🔬", "Health Intelligence", "Holistic wellness monitoring with comprehensive tracking of physical activity, sleep patterns, nutrition, and mental wellbeing with advanced analytics.")
]

for i, (icon, title, description) in enumerate(features):
    with [col1, col2, col3][i]:
        st.markdown(f'''
        <div class="glass-card">
            <div class="feature-card-content">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; color: #FFFFFF; margin-bottom: 1.5rem; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));">{icon}</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #FFFFFF; margin-bottom: 1.5rem; text-shadow: 0 2px 8px rgba(0,0,0,0.2);">{title}</div>
                </div>
                <div style="color: #E0E7FF; line-height: 1.6; text-align: center; font-size: 1rem;">
                    {description}
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Navigation Section - Perfect equal alignment
st.markdown('<div class="section-header">Platform Modules</div>', unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

modules = [
    ("📈", "Dashboard", "Real-time analytics and comprehensive performance overview"),
    ("⚡", "Work", "Advanced project and task management system"),
    ("🔬", "Health", "Comprehensive wellness and fitness tracking"),
    ("📊", "Analytics", "Advanced data insights and correlation analysis"),
    ("🎯", "Goals", "Strategic objective and milestone tracking")
]

for i, (icon, title, description) in enumerate(modules):
    with [nav_col1, nav_col2, nav_col3, nav_col4, nav_col5][i]:
        st.markdown(f'''
        <div class="nav-card">
            <div class="nav-icon">{icon}</div>
            <div class="nav-title">{title}</div>
            <div class="nav-description">{description}</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Recent Activity with consistent design
st.markdown('<div class="section-header">Recent Activity</div>', unsafe_allow_html=True)

try:
    if not health_df.empty and not work_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            latest_health = health_df.iloc[-1] if len(health_df) > 0 else None
            if latest_health is not None:
                st.markdown(f'''
                <div class="glass-card">
                    <div style="font-size: 1.3rem; font-weight: 700; color: #FFFFFF; margin-bottom: 1.5rem; text-align: center; text-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                        Latest Health Metrics
                    </div>
                    <div style="color: #E0E7FF; line-height: 2;">
                        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.15); padding: 0.75rem 0;">
                            <span style="font-weight: 500;">Date:</span>
                            <span style="color: #FFFFFF; font-weight: 600;">{latest_health['Date'] if 'Date' in latest_health else 'Recent'}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.15); padding: 0.75rem 0;">
                            <span style="font-weight: 500;">Mood Score:</span>
                            <span style="color: #A5B4FC; font-weight: 700;">{latest_health['Mood'] if 'Mood' in latest_health else 'N/A'}/10</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.15); padding: 0.75rem 0;">
                            <span style="font-weight: 500;">Daily Steps:</span>
                            <span style="color: #FFFFFF; font-weight: 600;">{latest_health['Steps'] if 'Steps' in latest_health else 'N/A'}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; padding: 0.75rem 0;">
                            <span style="font-weight: 500;">Sleep Duration:</span>
                            <span style="color: #FFFFFF; font-weight: 600;">{latest_health['Sleep Hours'] if 'Sleep Hours' in latest_health else 'N/A'} hrs</span>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            latest_work = work_df.iloc[-1] if len(work_df) > 0 else None
            if latest_work is not None:
                status_color = {
                    'Completed': '#00D26A',
                    'In Progress': '#A5B4FC', 
                    'Not Started': '#FF6B6B'
                }.get(latest_work['Status'] if 'Status' in latest_work else 'Not Started', '#6C757D')
                
                st.markdown(f'''
                <div class="glass-card">
                    <div style="font-size: 1.3rem; font-weight: 700; color: #FFFFFF; margin-bottom: 1.5rem; text-align: center; text-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                        Active Task Status
                    </div>
                    <div style="color: #E0E7FF;">
                        <div style="font-size: 1.1rem; color: #FFFFFF; font-weight: 700; margin-bottom: 1rem; line-height: 1.4;">
                            {latest_work['Task Title'] if 'Task Title' in latest_work else 'Current Task'}
                        </div>
                        <div style="margin-bottom: 1.5rem; font-size: 0.95rem; line-height: 1.5; opacity: 0.9;">
                            {latest_work['Task Description'] if 'Task Description' in latest_work else 'Task description not available'}
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.1); padding: 1.25rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.15);">
                            <div>
                                <span style="color: {status_color}; font-weight: 700; font-size: 1rem;">
                                    {latest_work['Status'] if 'Status' in latest_work else 'Not Started'}
                                </span>
                            </div>
                            <div style="color: #FFFFFF; font-weight: 700; font-size: 1.1rem;">
                                {latest_work['Progress'] if 'Progress' in latest_work else '0%'}
                            </div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; color: rgba(255,255,255,0.3); margin-bottom: 1.5rem; filter: drop-shadow(0 8px 20px rgba(0,0,0,0.3));">🚀</div>
            <div style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem; font-weight: 700;">Welcome to OrbitMe</div>
            <div style="color: #E0E7FF; font-size: 1rem; line-height: 1.6;">Start by adding your health data and tasks to see personalized insights and analytics.</div>
        </div>
        ''', unsafe_allow_html=True)
        
except Exception as e:
    st.markdown('''
    <div class="glass-card" style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; color: rgba(255,255,255,0.3); margin-bottom: 1.5rem; filter: drop-shadow(0 8px 20px rgba(0,0,0,0.3));">🌟</div>
        <div style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem; font-weight: 700;">Ready to Begin</div>
        <div style="color: #E0E7FF; font-size: 1rem; line-height: 1.6;">Your life management journey starts here. Add data to unlock powerful insights.</div>
    </div>
    ''', unsafe_allow_html=True)

# Clean Footer
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); padding: 3rem 0 1.5rem 0; font-size: 0.95rem;">
    OrbitMe Life Management Platform • v2.1 • 
    <span style="color: #A5B4FC; font-weight: 600;">Secure • Intelligent • Personalized</span>
</div>
""", unsafe_allow_html=True)

# Completely empty sidebar
with st.sidebar:
    pass