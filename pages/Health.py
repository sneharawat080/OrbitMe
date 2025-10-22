import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta

# Page configuration
st.set_page_config(
    page_title="OrbitMe - Health Tracking",
    layout="wide",
    page_icon="🔬",
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
    
    /* Form styling */
    .stForm {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2rem;
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
    
    /* Custom divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        margin: 2rem 0;
    }
    
    /* Metric indicators */
    .metric-excellent {
        color: #00D26A;
        font-weight: 600;
    }
    
    .metric-good {
        color: #A5B4FC;
        font-weight: 600;
    }
    
    .metric-fair {
        color: #FFA726;
        font-weight: 600;
    }
    
    .metric-poor {
        color: #FF6B6B;
        font-weight: 600;
    }
    
    /* Download button styling */
    .download-button {
        background: linear-gradient(135deg, #00D26A, #00B85C) !important;
    }
    
    .download-button:hover {
        background: linear-gradient(135deg, #00B85C, #009E4F) !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div style="padding: 2rem 0 1rem 0;">
    <div class="main-header">Health Tracking</div>
    <div style="text-align: center; color: #E0E7FF; font-size: 1.2rem; margin-bottom: 1rem; font-weight: 300;">
        Comprehensive wellness and fitness monitoring
    </div>
</div>
""", unsafe_allow_html=True)

DATA_PATH = "./data/health_data.csv"

# Ensure data directory exists
os.makedirs("./data", exist_ok=True)

# Initialize data structure
default_headers = [
    "Date", "Steps", "Water", "Sleep Hours", "Sleep Quality", 
    "Mood", "Weight", "Calories", "Ate Healthy", "Exercise", 
    "Stress Level", "Note"
]

if not os.path.exists(DATA_PATH):
    pd.DataFrame(columns=default_headers).to_csv(DATA_PATH, index=False)

# Load existing data for stats
if os.path.exists(DATA_PATH):
    df_all = pd.read_csv(DATA_PATH)
    if not df_all.empty:
        df_all["Date"] = pd.to_datetime(df_all["Date"]).dt.date
else:
    df_all = pd.DataFrame(columns=default_headers)

# Quick Stats Section
if not df_all.empty:
    st.markdown('<div class="section-header">Health Overview</div>', unsafe_allow_html=True)
    
    # Calculate metrics
    avg_steps = df_all['Steps'].mean() if 'Steps' in df_all.columns else 0
    avg_sleep = df_all['Sleep Hours'].mean() if 'Sleep Hours' in df_all.columns else 0
    avg_mood = df_all['Mood'].mean() if 'Mood' in df_all.columns else 0
    healthy_days = (df_all['Ate Healthy'].isin(['Excellent', 'Good'])).sum() if 'Ate Healthy' in df_all.columns else 0
    total_days = len(df_all)
    healthy_percentage = (healthy_days / total_days * 100) if total_days > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Average Steps</div>
            <div class="stats-number">{avg_steps:.0f}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Daily Average</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Sleep Quality</div>
            <div class="stats-number">{avg_sleep:.1f}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Hours per Night</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Mood Score</div>
            <div class="stats-number">{avg_mood:.1f}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Out of 10</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Healthy Days</div>
            <div class="stats-number">{healthy_percentage:.0f}%</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">{healthy_days}/{total_days} Days</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Health Data Entry Form
st.markdown('<div class="section-header">Daily Health Metrics</div>', unsafe_allow_html=True)

with st.form("health_entry_form"):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        entry_date = st.date_input("Entry Date", date.today())
        steps = st.number_input("Daily Steps", min_value=0, value=0)
        water = st.number_input("Water Intake (Liters)", min_value=0.0, value=0.0, step=0.5)
        sleep_hours = st.number_input("Sleep Duration (Hours)", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
        sleep_quality = st.select_slider("Sleep Quality", options=[1, 2, 3, 4, 5], value=3)
    
    with col2:
        mood = st.slider("Mood Assessment (1-10)", 1, 10, 5)
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, value=70.0, step=0.1)
        calories = st.number_input("Caloric Intake", min_value=0, value=2000, step=50)
        ate_healthy = st.radio("Nutrition Quality", ["Excellent", "Good", "Fair", "Poor"])
        exercise = st.radio("Exercise Completed", ["Yes", "No"])
        stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
    
    note = st.text_area("Additional Notes", placeholder="Any observations or comments...")
    
    submitted = st.form_submit_button("Save Health Entry")
    
    if submitted:
        new_entry = pd.DataFrame([[
            entry_date, steps, water, sleep_hours, sleep_quality,
            mood, weight, calories, ate_healthy, exercise,
            stress_level, note
        ]], columns=default_headers)
        
        # Append to existing data
        existing_data = pd.read_csv(DATA_PATH)
        updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
        updated_data.to_csv(DATA_PATH, index=False)
        
        st.success("Health data successfully recorded.")
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Health History and Analysis
st.markdown('<div class="section-header">Health Data History</div>', unsafe_allow_html=True)

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        
        # Date range filter
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", df["Date"].min())
        with col2:
            end_date = st.date_input("End Date", df["Date"].max())
        st.markdown('</div>', unsafe_allow_html=True)
        
        filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
        
        if not filtered_df.empty:
            # Detailed metrics analysis
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Health Metrics Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Sleep analysis
                avg_sleep_filtered = filtered_df['Sleep Hours'].mean()
                sleep_quality_avg = filtered_df['Sleep Quality'].mean()
                
                st.write("**Sleep Analysis**")
                st.write(f"Average Hours: {avg_sleep_filtered:.1f}")
                st.write(f"Quality Score: {sleep_quality_avg:.1f}/5")
                
                # Sleep quality indicator
                if avg_sleep_filtered >= 7 and sleep_quality_avg >= 4:
                    st.markdown("<span class='metric-excellent'>Excellent Sleep</span>", unsafe_allow_html=True)
                elif avg_sleep_filtered >= 6 and sleep_quality_avg >= 3:
                    st.markdown("<span class='metric-good'>Good Sleep</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='metric-poor'>Needs Improvement</span>", unsafe_allow_html=True)
            
            with col2:
                # Activity analysis
                avg_steps_filtered = filtered_df['Steps'].mean()
                exercise_days = (filtered_df['Exercise'] == 'Yes').sum()
                exercise_percentage = (exercise_days / len(filtered_df)) * 100
                
                st.write("**Activity Analysis**")
                st.write(f"Average Steps: {avg_steps_filtered:.0f}")
                st.write(f"Exercise Days: {exercise_percentage:.0f}%")
                
                # Activity indicator
                if avg_steps_filtered >= 8000 and exercise_percentage >= 70:
                    st.markdown("<span class='metric-excellent'>Very Active</span>", unsafe_allow_html=True)
                elif avg_steps_filtered >= 5000 and exercise_percentage >= 50:
                    st.markdown("<span class='metric-good'>Moderately Active</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='metric-poor'>Low Activity</span>", unsafe_allow_html=True)
            
            with col3:
                # Nutrition & Stress analysis
                healthy_days_filtered = (filtered_df['Ate Healthy'].isin(['Excellent', 'Good'])).sum()
                healthy_percentage_filtered = (healthy_days_filtered / len(filtered_df)) * 100
                avg_stress = filtered_df['Stress Level'].mean()
                avg_mood_filtered = filtered_df['Mood'].mean()
                
                st.write("**Wellness Analysis**")
                st.write(f"Healthy Eating: {healthy_percentage_filtered:.0f}%")
                st.write(f"Stress Level: {avg_stress:.1f}/10")
                st.write(f"Mood Score: {avg_mood_filtered:.1f}/10")
                
                # Wellness indicator
                if healthy_percentage_filtered >= 70 and avg_stress <= 4 and avg_mood_filtered >= 7:
                    st.markdown("<span class='metric-excellent'>Optimal Wellness</span>", unsafe_allow_html=True)
                elif healthy_percentage_filtered >= 50 and avg_stress <= 6 and avg_mood_filtered >= 5:
                    st.markdown("<span class='metric-good'>Good Wellness</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='metric-poor'>Wellness Concern</span>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Data table
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Detailed Records")
            st.dataframe(filtered_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export option
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("Download CSV", type="primary"):
                    csv = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="Download Health Data",
                        data=csv,
                        file_name=f"health_data_{date.today()}.csv",
                        mime="text/csv"
                    )
        else:
            st.markdown('''
            <div class="glass-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem; font-weight: 700;">No Data in Selected Range</div>
                <div style="color: #E0E7FF; font-size: 1rem; line-height: 1.6;">Adjust the date range or add new health entries.</div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem; font-weight: 700;">No Health Data Available</div>
            <div style="color: #E0E7FF; font-size: 1rem; line-height: 1.6;">Start by entering your first health metrics above.</div>
        </div>
        ''', unsafe_allow_html=True)

# Quick Actions in Sidebar
st.sidebar.markdown("""
<div style="padding: 1.5rem 0 1rem 0;">
    <div style="font-size: 1.3rem; font-weight: 700; color: #FFFFFF; margin-bottom: 1rem;">
        Quick Actions
    </div>
</div>
""", unsafe_allow_html=True)

# Simple sidebar buttons
if st.sidebar.button("View Recent Entries", use_container_width=True):
    if os.path.exists(DATA_PATH):
        df_recent = pd.read_csv(DATA_PATH)
        if not df_recent.empty:
            st.sidebar.write("**Recent Entries:**")
            recent = df_recent.tail(3)
            for _, entry in recent.iterrows():
                date_str = entry['Date'] if 'Date' in entry else 'Unknown'
                steps_str = entry['Steps'] if 'Steps' in entry else 'N/A'
                st.sidebar.write(f"- {date_str}: {steps_str} steps")
        else:
            st.sidebar.info("No entries available")

if st.sidebar.button("Refresh Data", use_container_width=True):
    st.rerun()

# Clean Footer
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); padding: 2rem 0 1rem 0; font-size: 0.9rem;">
    OrbitMe Health Tracking v2.1 • Comprehensive • Insightful • Personalized
</div>
""", unsafe_allow_html=True)