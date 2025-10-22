import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="OrbitMe - Advanced Analytics",
    layout="wide",
    page_icon="📈",
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
    
    /* Insight cards */
    .insight-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .insight-positive {
        border-left: 4px solid #00D26A;
    }
    
    .insight-warning {
        border-left: 4px solid #FFA726;
    }
    
    .insight-info {
        border-left: 4px solid #42A5F5;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div style="padding: 2rem 0 1rem 0;">
    <div class="main-header">Advanced Analytics</div>
    <div style="text-align: center; color: #E0E7FF; font-size: 1.2rem; margin-bottom: 1rem; font-weight: 300;">
        Deep insights and correlation analysis
    </div>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_data():
    health_df = pd.read_csv('./data/health_data.csv') if os.path.exists('./data/health_data.csv') else pd.DataFrame()
    work_df = pd.read_csv('./data/work_data.csv') if os.path.exists('./data/work_data.csv') else pd.DataFrame()
    
    # Convert date columns
    if not health_df.empty and 'Date' in health_df.columns:
        health_df['Date'] = pd.to_datetime(health_df['Date'])
    if not work_df.empty and 'Date Created' in work_df.columns:
        work_df['Date Created'] = pd.to_datetime(work_df['Date Created'])
    
    return health_df, work_df

health_df, work_df = load_all_data()

if health_df.empty and work_df.empty:
    st.markdown('''
    <div class="glass-card" style="text-align: center; padding: 3rem;">
        <div style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem; font-weight: 700;">No Data Available</div>
        <div style="color: #E0E7FF; font-size: 1rem; line-height: 1.6;">Start by adding health and work data to unlock advanced analytics.</div>
    </div>
    ''', unsafe_allow_html=True)
    st.stop()

# Quick Stats Overview
st.markdown('<div class="section-header">Performance Overview</div>', unsafe_allow_html=True)

if not health_df.empty or not work_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    # Health metrics
    if not health_df.empty:
        avg_mood = health_df['Mood'].mean() if 'Mood' in health_df.columns else 0
        avg_sleep = health_df['Sleep Hours'].mean() if 'Sleep Hours' in health_df.columns else 0
        avg_steps = health_df['Steps'].mean() if 'Steps' in health_df.columns else 0
        avg_stress = health_df['Stress Level'].mean() if 'Stress Level' in health_df.columns else 0
    else:
        avg_mood = avg_sleep = avg_steps = avg_stress = 0
    
    # Work metrics
    if not work_df.empty:
        total_tasks = len(work_df)
        completed_tasks = len(work_df[work_df['Status'] == 'Completed']) if 'Status' in work_df.columns else 0
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    else:
        total_tasks = completed_tasks = completion_rate = 0
    
    with col1:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Average Mood</div>
            <div class="stats-number">{avg_mood:.1f}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Wellness Indicator</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Task Completion</div>
            <div class="stats-number">{completion_rate:.1f}%</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Productivity Rate</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Average Sleep</div>
            <div class="stats-number">{avg_sleep:.1f}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Hours per Night</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Data Points</div>
            <div class="stats-number">{len(health_df) + len(work_df)}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Total Records</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Correlation Analysis
st.markdown('<div class="section-header">Health and Productivity Correlation</div>', unsafe_allow_html=True)

if not health_df.empty and not work_df.empty:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Merge data on dates (simplified approach)
    health_daily = health_df.groupby('Date').agg({
        'Mood': 'mean',
        'Sleep Hours': 'mean',
        'Steps': 'mean',
        'Stress Level': 'mean'
    }).reset_index()
    
    # Analysis options
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Mood vs Physical Activity", "Sleep vs Wellness", "Stress Impact Analysis", "Productivity Patterns"]
    )
    
    if analysis_type == "Mood vs Physical Activity":
        fig = px.scatter(health_daily, x='Mood', y='Steps', 
                        title="Mood vs Physical Activity Correlation",
                        trendline="ols",
                        color='Mood',
                        color_continuous_scale='Viridis')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Sleep vs Wellness":
        fig = px.scatter(health_daily, x='Sleep Hours', y='Mood',
                        title="Sleep Duration vs Mood Correlation",
                        trendline="ols",
                        color='Sleep Hours',
                        color_continuous_scale='Blues')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Stress Impact Analysis":
        fig = px.scatter(health_daily, x='Stress Level', y='Mood',
                        title="Stress Level vs Mood Correlation",
                        trendline="ols",
                        color='Stress Level',
                        color_continuous_scale='RdYlGn_r')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Productivity Patterns":
        if 'Hours Spent' in work_df.columns and 'Date Created' in work_df.columns:
            work_daily = work_df.groupby('Date Created').agg({
                'Hours Spent': 'sum'
            }).reset_index()
            
            # Merge with health data
            merged_data = pd.merge(health_daily, work_daily, left_on='Date', right_on='Date Created', how='inner')
            
            fig = px.scatter(merged_data, x='Hours Spent', y='Mood',
                            title="Work Hours vs Mood Correlation",
                            trendline="ols",
                            color='Hours Spent',
                            color_continuous_scale='Purples')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Trend Analysis
st.markdown('<div class="section-header">Long-term Trends</div>', unsafe_allow_html=True)

if not health_df.empty:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    time_period = st.selectbox("Analysis Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"])
    
    # Filter data based on selection
    end_date = health_df['Date'].max()
    if time_period == "Last 7 Days":
        start_date = end_date - timedelta(days=7)
    elif time_period == "Last 30 Days":
        start_date = end_date - timedelta(days=30)
    elif time_period == "Last 90 Days":
        start_date = end_date - timedelta(days=90)
    else:
        start_date = health_df['Date'].min()
    
    filtered_health = health_df[(health_df['Date'] >= start_date) & (health_df['Date'] <= end_date)]
    
    # Create trend visualization
    metrics = st.multiselect("Select Metrics to Display", 
                           ["Mood", "Sleep Hours", "Steps", "Stress Level"],
                           default=["Mood", "Sleep Hours"])
    
    if metrics:
        fig = go.Figure()
        colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']
        
        for i, metric in enumerate(metrics):
            fig.add_trace(go.Scatter(
                x=filtered_health['Date'], 
                y=filtered_health[metric],
                mode='lines+markers', 
                name=metric,
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title=f"Health Metrics Trend - {time_period}",
            xaxis_title="Date", 
            yaxis_title="Value",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Insights and Recommendations
st.markdown('<div class="section-header">Data Insights</div>', unsafe_allow_html=True)

if not health_df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Health Insights")
        
        # Calculate insights
        avg_mood = health_df['Mood'].mean()
        avg_sleep = health_df['Sleep Hours'].mean()
        avg_steps = health_df['Steps'].mean() if 'Steps' in health_df.columns else 0
        avg_stress = health_df['Stress Level'].mean() if 'Stress Level' in health_df.columns else 0
        
        # Display insights with conditional formatting
        st.markdown(f"**Average Mood Score:** {avg_mood:.1f}/10")
        st.markdown(f"**Average Sleep Duration:** {avg_sleep:.1f} hours")
        if 'Steps' in health_df.columns:
            st.markdown(f"**Average Daily Steps:** {avg_steps:,.0f}")
        if 'Stress Level' in health_df.columns:
            st.markdown(f"**Average Stress Level:** {avg_stress:.1f}/10")
        
        # Recommendations
        if avg_sleep < 7:
            st.markdown('<div class="insight-card insight-warning">', unsafe_allow_html=True)
            st.write("**Recommendation:** Consider increasing sleep duration to 7-9 hours for optimal health and cognitive function.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if avg_steps < 8000 and 'Steps' in health_df.columns:
            st.markdown('<div class="insight-card insight-info">', unsafe_allow_html=True)
            st.write("**Recommendation:** Aim for 8,000-10,000 steps daily to maintain good physical activity levels.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if avg_mood >= 7:
            st.markdown('<div class="insight-card insight-positive">', unsafe_allow_html=True)
            st.write("**Positive Trend:** Your average mood score indicates good emotional well-being.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Productivity Insights")
        
        if not work_df.empty:
            total_tasks = len(work_df)
            completed_tasks = len(work_df[work_df['Status'] == 'Completed']) if 'Status' in work_df.columns else 0
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            high_priority_tasks = len(work_df[work_df['Priority'] == 'High']) if 'Priority' in work_df.columns else 0
            
            st.markdown(f"**Task Completion Rate:** {completion_rate:.1f}%")
            st.markdown(f"**Total Tasks Tracked:** {total_tasks}")
            st.markdown(f"**High Priority Tasks:** {high_priority_tasks}")
            
            # Productivity recommendations
            if completion_rate < 70:
                st.markdown('<div class="insight-card insight-warning">', unsafe_allow_html=True)
                st.write("**Recommendation:** Review task priorities and time allocation to improve completion rates.")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if completion_rate >= 85:
                st.markdown('<div class="insight-card insight-positive">', unsafe_allow_html=True)
                st.write("**Excellent Performance:** High task completion rate indicates effective productivity management.")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if high_priority_tasks > total_tasks * 0.4:
                st.markdown('<div class="insight-card insight-info">', unsafe_allow_html=True)
                st.write("**Priority Management:** Consider reviewing task prioritization to ensure focus on truly critical items.")
                st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            st.info("No work data available for productivity insights.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Export Comprehensive Report
st.markdown('<div class="section-header">Reporting</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

if st.button("Generate Comprehensive Report", type="primary"):
    report_data = {
        "Health Summary": {
            "Average Mood": f"{health_df['Mood'].mean():.1f}",
            "Average Sleep Hours": f"{health_df['Sleep Hours'].mean():.1f}",
            "Average Steps": f"{health_df['Steps'].mean():.0f}" if 'Steps' in health_df.columns else "N/A",
            "Data Points": f"{len(health_df)}"
        },
        "Work Summary": {
            "Total Tasks": f"{len(work_df)}",
            "Completion Rate": f"{(len(work_df[work_df['Status'] == 'Completed']) / len(work_df) * 100):.1f}%" if not work_df.empty else "N/A",
            "High Priority Tasks": f"{len(work_df[work_df['Priority'] == 'High'])}" if not work_df.empty and 'Priority' in work_df.columns else "N/A"
        } if not work_df.empty else {}
    }
    
    st.subheader("Comprehensive Report")
    st.json(report_data)
    
    # Export functionality
    if st.button("Download Report Summary"):
        report_text = f"""
OrbitMe Analytics Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

HEALTH SUMMARY:
- Average Mood: {health_df['Mood'].mean():.1f}/10
- Average Sleep: {health_df['Sleep Hours'].mean():.1f} hours
- Data Points: {len(health_df)} records

WORK SUMMARY:
- Total Tasks: {len(work_df)}
- Completion Rate: {(len(work_df[work_df['Status'] == 'Completed']) / len(work_df) * 100):.1f}%
- High Priority Tasks: {len(work_df[work_df['Priority'] == 'High']) if not work_df.empty and 'Priority' in work_df.columns else 0}
        """
        
        st.download_button(
            label="Download Report as Text",
            data=report_text,
            file_name=f"orbitme_report_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

st.markdown('</div>', unsafe_allow_html=True)

# Quick Actions in Sidebar
st.sidebar.markdown("""
<div style="padding: 1.5rem 0 1rem 0;">
    <div style="font-size: 1.3rem; font-weight: 700; color: #FFFFFF; margin-bottom: 1rem;">
        Analytics Controls
    </div>
</div>
""", unsafe_allow_html=True)

# Refresh button
if st.sidebar.button("Refresh Analytics", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

# Clean Footer
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); padding: 2rem 0 1rem 0; font-size: 0.9rem;">
    OrbitMe Advanced Analytics v2.1 • Intelligent • Insightful • Actionable
</div>
""", unsafe_allow_html=True)