import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="OrbitMe - Analytics Dashboard",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Professional CSS matching OrbitMe theme
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
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, #FFFFFF, #E0E7FF, #A5B4FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .section-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 2rem 0 1.5rem 0;
        text-shadow: 0 4px 15px rgba(0,0,0,0.3);
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 0;
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #A5B4FC);
        border-radius: 2px;
    }
    
    /* Enhanced glass morphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.25);
        background: rgba(255, 255, 255, 0.12);
    }
    
    /* Enhanced stats cards */
    .stats-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        border-radius: 18px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .stats-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0.5rem 0;
        background: linear-gradient(45deg, #FFFFFF, #E0E7FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stats-label {
        color: #E0E7FF;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        opacity: 0.8;
    }
    
    /* Custom divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        margin: 2rem 0;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Download button styling */
    .download-button {
        background: linear-gradient(135deg, #00D26A, #00B85C) !important;
    }
    
    .download-button:hover {
        background: linear-gradient(135deg, #00B85C, #009E4F) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 8px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 12px;
        padding: 0 24px;
        background: transparent;
        color: #E0E7FF;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(102, 126, 234, 0.3) !important;
        color: #FFFFFF !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div style="padding: 2rem 0 1rem 0;">
    <div class="main-header">Analytics Dashboard</div>
    <div style="text-align: center; color: #E0E7FF; font-size: 1.2rem; margin-bottom: 1rem; font-weight: 300;">
        Advanced data insights and correlation analysis
    </div>
</div>
""", unsafe_allow_html=True)

# Data paths
health_path = './data/health_data.csv'
work_path = './data/work_data.csv'

@st.cache_data
def load_data():
    # Health data
    if os.path.exists(health_path):
        health_df = pd.read_csv(health_path)
        if not health_df.empty and 'Date' in health_df.columns:
            health_df["Date"] = pd.to_datetime(health_df["Date"]).dt.date
    else:
        health_df = pd.DataFrame(columns=["Date", "Steps", "Water", "Sleep Hours", "Sleep Quality", "Mood", "Weight", "Calories", "Ate Healthy", "Exercise", "Stress Level", "Note"])
    
    # Work data
    if os.path.exists(work_path):
        work_df = pd.read_csv(work_path)
        if not work_df.empty:
            if 'Date Created' in work_df.columns:
                work_df["Date Created"] = pd.to_datetime(work_df["Date Created"]).dt.date
            if 'Deadline' in work_df.columns:
                work_df["Deadline"] = pd.to_datetime(work_df["Deadline"]).dt.date
    else:
        work_df = pd.DataFrame(columns=["Task Title", "Task Description", "Category", "Priority", "Status", "Hours Spent", "Progress", "Deadline", "Date Created", "Tags", "Note"])
    
    return health_df, work_df

health_df, work_df = load_data()

# Key Metrics Section
st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)

if not health_df.empty or not work_df.empty:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Health metrics
    if not health_df.empty:
        avg_mood = health_df["Mood"].mean() if 'Mood' in health_df.columns and not health_df.empty else 0
        avg_sleep = health_df["Sleep Hours"].mean() if 'Sleep Hours' in health_df.columns and not health_df.empty else 0
        avg_steps = health_df["Steps"].mean() if 'Steps' in health_df.columns and not health_df.empty else 0
        avg_water = health_df["Water"].mean() if 'Water' in health_df.columns and not health_df.empty else 0
        avg_stress = health_df["Stress Level"].mean() if 'Stress Level' in health_df.columns and not health_df.empty else 0
    else:
        avg_mood = avg_sleep = avg_steps = avg_water = avg_stress = 0
    
    # Work metrics
    if not work_df.empty:
        completed_tasks = work_df[work_df["Status"] == "Completed"].shape[0] if 'Status' in work_df.columns else 0
        total_tasks = work_df.shape[0]
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        total_hours = work_df["Hours Spent"].sum() if 'Hours Spent' in work_df.columns else 0
        
        # Calculate progress average safely
        if 'Progress' in work_df.columns:
            work_df["Progress Numeric"] = work_df["Progress"].astype(str).str.rstrip('%').astype(float)
            avg_progress = work_df["Progress Numeric"].mean()
        else:
            avg_progress = 0
    else:
        completed_tasks = total_tasks = completion_rate = total_hours = avg_progress = 0
    
    with col1:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Average Mood</div>
            <div class="stats-number">{avg_mood:.1f}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Out of 10</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Average Sleep</div>
            <div class="stats-number">{avg_sleep:.1f}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Hours</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Task Completion</div>
            <div class="stats-number">{completion_rate:.1f}%</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Success Rate</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Total Hours</div>
            <div class="stats-number">{total_hours}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Time Invested</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col5:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Avg Progress</div>
            <div class="stats-number">{avg_progress:.1f}%</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Overall Progress</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Health Overview
st.markdown('<div class="section-header">Health Overview</div>', unsafe_allow_html=True)

if not health_df.empty:
    # Recent Health Metrics
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Recent Health Metrics")
    
    # Get last 7 days of data
    if len(health_df) > 0:
        recent_health = health_df.tail(7)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            latest_mood = recent_health["Mood"].iloc[-1] if 'Mood' in recent_health.columns else 0
            mood_change = recent_health["Mood"].iloc[-1] - recent_health["Mood"].iloc[-2] if len(recent_health) > 1 else 0
            st.metric("Latest Mood", f"{latest_mood}/10", f"{mood_change:+.1f}")
        
        with col2:
            latest_steps = recent_health["Steps"].iloc[-1] if 'Steps' in recent_health.columns else 0
            steps_change = recent_health["Steps"].iloc[-1] - recent_health["Steps"].iloc[-2] if len(recent_health) > 1 else 0
            st.metric("Latest Steps", f"{latest_steps:,}", f"{steps_change:+,}")
        
        with col3:
            latest_sleep = recent_health["Sleep Hours"].iloc[-1] if 'Sleep Hours' in recent_health.columns else 0
            sleep_change = recent_health["Sleep Hours"].iloc[-1] - recent_health["Sleep Hours"].iloc[-2] if len(recent_health) > 1 else 0
            st.metric("Latest Sleep", f"{latest_sleep} hrs", f"{sleep_change:+.1f}")
        
        with col4:
            latest_stress = recent_health["Stress Level"].iloc[-1] if 'Stress Level' in recent_health.columns else 0
            stress_change = recent_health["Stress Level"].iloc[-1] - recent_health["Stress Level"].iloc[-2] if len(recent_health) > 1 else 0
            st.metric("Latest Stress", f"{latest_stress}/10", f"{stress_change:+.1f}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Health Trends
st.markdown('<div class="section-header">Health Trends Analysis</div>', unsafe_allow_html=True)

if not health_df.empty and 'Date' in health_df.columns:
    health_df_sorted = health_df.sort_values("Date")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Comprehensive View", "Mood Analysis", "Activity Analysis"])
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Comprehensive health dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Mood Trend', 'Sleep Patterns', 'Step Count', 'Stress Levels'),
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        # Mood trend
        if 'Mood' in health_df_sorted.columns:
            fig.add_trace(
                go.Scatter(x=health_df_sorted["Date"], y=health_df_sorted["Mood"], 
                          mode='lines+markers', name='Mood', line=dict(color='#1f77b4')),
                row=1, col=1
            )
        
        # Sleep patterns
        if 'Sleep Hours' in health_df_sorted.columns:
            fig.add_trace(
                go.Bar(x=health_df_sorted["Date"], y=health_df_sorted["Sleep Hours"], 
                      name='Sleep Hours', marker_color='#2ca02c'),
                row=1, col=2
            )
        
        # Step count
        if 'Steps' in health_df_sorted.columns:
            fig.add_trace(
                go.Scatter(x=health_df_sorted["Date"], y=health_df_sorted["Steps"], 
                          mode='lines', name='Steps', line=dict(color='#ff7f0e')),
                row=2, col=1
            )
        
        # Stress levels
        if 'Stress Level' in health_df_sorted.columns:
            fig.add_trace(
                go.Scatter(x=health_df_sorted["Date"], y=health_df_sorted["Stress Level"], 
                          mode='lines+markers', name='Stress Level', line=dict(color='#d62728')),
                row=2, col=2
            )
        
        fig.update_layout(
            height=600, 
            showlegend=True, 
            title_text="Health Metrics Over Time",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Mood and Stress correlation
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Mood' in health_df_sorted.columns and 'Stress Level' in health_df_sorted.columns:
                fig_corr = px.scatter(health_df_sorted, x='Stress Level', y='Mood', 
                                     title="Mood vs Stress Level",
                                     trendline="ols",
                                     color='Stress Level',
                                     color_continuous_scale='RdYlGn_r')
                fig_corr.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_corr, use_container_width=True)
        
        with col2:
            if 'Mood' in health_df_sorted.columns:
                # Mood distribution
                fig_dist = px.histogram(health_df_sorted, x='Mood', 
                                       title="Mood Distribution",
                                       nbins=10,
                                       color_discrete_sequence=['#1f77b4'])
                fig_dist.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_dist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Activity and Sleep analysis
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Steps' in health_df_sorted.columns:
                # Steps over time
                fig_steps = px.area(health_df_sorted, x='Date', y='Steps',
                                   title="Daily Step Count",
                                   color_discrete_sequence=['#ff7f0e'])
                fig_steps.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_steps, use_container_width=True)
        
        with col2:
            if 'Sleep Hours' in health_df_sorted.columns and 'Sleep Quality' in health_df_sorted.columns:
                # Sleep quality vs duration
                fig_sleep = px.scatter(health_df_sorted, x='Sleep Hours', y='Sleep Quality',
                                      title="Sleep Quality vs Duration",
                                      size='Sleep Quality',
                                      color='Sleep Quality',
                                      color_continuous_scale='Viridis')
                fig_sleep.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_sleep, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('''
    <div class="glass-card" style="text-align: center; padding: 3rem;">
        <div style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem; font-weight: 700;">No Health Data Available</div>
        <div style="color: #E0E7FF; font-size: 1rem; line-height: 1.6;">Add health data in the Health Tracking section for trend analysis.</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Work Progress
st.markdown('<div class="section-header">Work Progress Analysis</div>', unsafe_allow_html=True)

if not work_df.empty:
    # Work metrics overview
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Work Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        high_priority = work_df[work_df["Priority"] == "High"].shape[0] if 'Priority' in work_df.columns else 0
        st.metric("High Priority Tasks", high_priority)
    
    with col2:
        in_progress = work_df[work_df["Status"] == "In Progress"].shape[0] if 'Status' in work_df.columns else 0
        st.metric("In Progress", in_progress)
    
    with col3:
        overdue = work_df[
            (work_df['Deadline'] < pd.to_datetime('today').date()) & 
            (work_df['Status'] != 'Completed')
        ].shape[0] if 'Deadline' in work_df.columns and 'Status' in work_df.columns else 0
        st.metric("Overdue Tasks", overdue)
    
    with col4:
        avg_hours_per_task = work_df["Hours Spent"].mean() if 'Hours Spent' in work_df.columns else 0
        st.metric("Avg Hours/Task", f"{avg_hours_per_task:.1f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Work visualization tabs
    tab1, tab2, tab3 = st.tabs(["Task Distribution", "Progress Timeline", "Time Analysis"])
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            # Task status distribution
            if 'Status' in work_df.columns:
                status_counts = work_df["Status"].value_counts()
                fig_pie = px.pie(values=status_counts.values, names=status_counts.index,
                                title="Task Status Distribution",
                                color_discrete_sequence=px.colors.qualitative.Set3)
                fig_pie.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Priority distribution
            if 'Priority' in work_df.columns:
                priority_counts = work_df["Priority"].value_counts()
                fig_bar = px.bar(x=priority_counts.index, y=priority_counts.values,
                                title="Tasks by Priority",
                                color=priority_counts.index,
                                color_discrete_sequence=px.colors.qualitative.Bold)
                fig_bar.update_layout(
                    xaxis_title="Priority", 
                    yaxis_title="Number of Tasks",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Progress over time
        if 'Progress' in work_df.columns and 'Date Created' in work_df.columns:
            work_df["Progress Numeric"] = work_df["Progress"].astype(str).str.rstrip('%').astype(float)
            progress_trend = work_df.groupby("Date Created")["Progress Numeric"].mean().reset_index()
            
            fig_progress = px.line(progress_trend, x="Date Created", y="Progress Numeric",
                                 title="Average Progress Over Time",
                                 markers=True,
                                 line_shape="spline")
            fig_progress.update_layout(
                xaxis_title="Date", 
                yaxis_title="Average Progress (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_progress, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Time spent analysis
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Hours Spent' in work_df.columns and 'Category' in work_df.columns:
                hours_by_category = work_df.groupby("Category")["Hours Spent"].sum().reset_index()
                fig_hours = px.pie(hours_by_category, values='Hours Spent', names='Category',
                                  title="Time Spent by Category")
                fig_hours.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_hours, use_container_width=True)
        
        with col2:
            if 'Hours Spent' in work_df.columns and 'Date Created' in work_df.columns:
                daily_hours = work_df.groupby("Date Created")["Hours Spent"].sum().reset_index()
                fig_daily = px.bar(daily_hours, x='Date Created', y='Hours Spent',
                                  title="Daily Hours Spent",
                                  color='Hours Spent',
                                  color_continuous_scale='Blues')
                fig_daily.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_daily, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('''
    <div class="glass-card" style="text-align: center; padding: 3rem;">
        <div style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem; font-weight: 700;">No Work Data Available</div>
        <div style="color: #E0E7FF; font-size: 1rem; line-height: 1.6;">Add tasks in the Work Management section for analysis.</div>
    </div>
    ''', unsafe_allow_html=True)

# Quick Actions in Sidebar
st.sidebar.markdown("""
<div style="padding: 1.5rem 0 1rem 0;">
    <div style="font-size: 1.3rem; font-weight: 700; color: #FFFFFF; margin-bottom: 1rem;">
        Dashboard Controls
    </div>
</div>
""", unsafe_allow_html=True)

# Refresh button
if st.sidebar.button("Refresh Dashboard", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

# Export options
st.sidebar.markdown("""
<div style="padding: 1.5rem 0 1rem 0;">
    <div style="font-size: 1.3rem; font-weight: 700; color: #FFFFFF; margin-bottom: 1rem;">
        Export Data
    </div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("Export Health Data", use_container_width=True):
    if not health_df.empty:
        csv = health_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download Health CSV",
            data=csv,
            file_name=f"health_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if st.sidebar.button("Export Work Data", use_container_width=True):
    if not work_df.empty:
        csv = work_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download Work CSV",
            data=csv,
            file_name=f"work_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Clean Footer
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); padding: 2rem 0 1rem 0; font-size: 0.9rem;">
    OrbitMe Analytics Dashboard v2.1 • Insightful • Data-Driven • Comprehensive
</div>
""", unsafe_allow_html=True)