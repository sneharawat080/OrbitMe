import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta

# Page configuration
st.set_page_config(
    page_title="OrbitMe - Goal Tracking",
    layout="wide",
    page_icon="🎯",
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
    
    /* Priority badges */
    .priority-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .priority-critical {
        background: linear-gradient(135deg, #FF6B6B, #EE5A52);
        color: white;
    }
    
    .priority-high {
        background: linear-gradient(135deg, #FFA726, #FF9800);
        color: white;
    }
    
    .priority-medium {
        background: linear-gradient(135deg, #42A5F5, #2196F3);
        color: white;
    }
    
    .priority-low {
        background: linear-gradient(135deg, #66BB6A, #4CAF50);
        color: white;
    }
    
    /* Status indicators */
    .status-completed {
        color: #00D26A;
        font-weight: 600;
    }
    
    .status-progress {
        color: #A5B4FC;
        font-weight: 600;
    }
    
    .status-hold {
        color: #FFA726;
        font-weight: 600;
    }
    
    .status-not-started {
        color: #FF6B6B;
        font-weight: 600;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Goal card styling */
    .goal-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .goal-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div style="padding: 2rem 0 1rem 0;">
    <div class="main-header">Goal Tracking</div>
    <div style="text-align: center; color: #E0E7FF; font-size: 1.2rem; margin-bottom: 1rem; font-weight: 300;">
        Strategic objective and milestone tracking
    </div>
</div>
""", unsafe_allow_html=True)

GOALS_PATH = './data/goals_data.csv'
os.makedirs('./data', exist_ok=True)

# Initialize goals data
goal_columns = [
    "Goal ID", "Goal Title", "Description", "Category", "Priority", 
    "Status", "Start Date", "Target Date", "Progress", "Milestones", 
    "Action Plan", "Notes", "Date Created"
]

if os.path.exists(GOALS_PATH):
    goals_df = pd.read_csv(GOALS_PATH)
    if not goals_df.empty:
        goals_df['Start Date'] = pd.to_datetime(goals_df['Start Date']).dt.date
        goals_df['Target Date'] = pd.to_datetime(goals_df['Target Date']).dt.date
        goals_df['Date Created'] = pd.to_datetime(goals_df['Date Created']).dt.date
else:
    goals_df = pd.DataFrame(columns=goal_columns)
    goals_df.to_csv(GOALS_PATH, index=False)

def create_goal_id():
    if goals_df.empty:
        return "G001"
    else:
        last_id = goals_df["Goal ID"].str.extract(r'G(\d+)').astype(int).max().iloc[0]
        return f"G{last_id + 1:03d}"

# Quick Stats Section
if not goals_df.empty:
    st.markdown('<div class="section-header">Goals Overview</div>', unsafe_allow_html=True)
    
    total_goals = len(goals_df)
    completed_goals = len(goals_df[goals_df["Status"] == "Completed"])
    in_progress_goals = len(goals_df[goals_df["Status"] == "In Progress"])
    
    # Calculate overdue goals
    today_date = date.today()
    goals_df_temp = goals_df.copy()
    goals_df_temp['Target Date'] = pd.to_datetime(goals_df_temp['Target Date'])
    overdue_goals = len(goals_df_temp[
        (goals_df_temp['Target Date'] < pd.to_datetime(today_date)) & 
        (goals_df_temp['Status'] != 'Completed')
    ])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Total Goals</div>
            <div class="stats-number">{total_goals}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Active Objectives</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Completed</div>
            <div class="stats-number">{completed_goals}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Goals Achieved</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">In Progress</div>
            <div class="stats-number">{in_progress_goals}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Active Pursuit</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Overdue</div>
            <div class="stats-number">{overdue_goals}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Require Attention</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Goal Management Interface
tab1, tab2, tab3 = st.tabs(["Set New Goal", "Track Progress", "Goal Overview"])

with tab1:
    st.markdown('<div class="section-header">Define New Goal</div>', unsafe_allow_html=True)
    
    with st.form("goal_creation_form"):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            goal_title = st.text_input("Goal Title", placeholder="What do you want to achieve?")
            category = st.selectbox("Category", 
                                  ["Health & Fitness", "Career", "Education", "Personal Development", "Financial", "Relationships", "Other"])
            priority = st.select_slider("Priority Level", ["Low", "Medium", "High", "Critical"])
            start_date = st.date_input("Start Date", date.today())
        
        with col2:
            target_date = st.date_input("Target Completion Date", date.today() + timedelta(days=90))
            status = st.selectbox("Current Status", ["Not Started", "In Progress", "On Hold", "Completed"])
            initial_progress = st.slider("Initial Progress", 0, 100, 0)
            description = st.text_area("Goal Description", placeholder="Detailed description of your goal...")
        
        milestones = st.text_area("Key Milestones", placeholder="Break down your goal into measurable milestones...")
        action_plan = st.text_area("Action Plan", placeholder="Specific steps you'll take to achieve this goal...")
        notes = st.text_area("Additional Notes")
        
        submitted = st.form_submit_button("Create Goal")
        
        if submitted:
            if not goal_title:
                st.warning("Goal title is required.")
            else:
                new_goal = pd.DataFrame([[
                    create_goal_id(), goal_title, description, category, priority,
                    status, start_date, target_date, initial_progress, milestones,
                    action_plan, notes, date.today()
                ]], columns=goal_columns)
                
                goals_df = pd.concat([goals_df, new_goal], ignore_index=True)
                goals_df.to_csv(GOALS_PATH, index=False)
                st.success("Goal created successfully!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header">Track Goal Progress</div>', unsafe_allow_html=True)
    
    if not goals_df.empty:
        # Select goal to update
        goal_options = goals_df[["Goal ID", "Goal Title"]].apply(lambda x: f"{x[0]} - {x[1]}", axis=1).tolist()
        selected_goal = st.selectbox("Select Goal to Update", goal_options)
        
        if selected_goal:
            goal_id = selected_goal.split(" - ")[0]
            goal_data = goals_df[goals_df["Goal ID"] == goal_id].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Goal Details")
                
                # Priority badge
                priority_class = f"priority-{goal_data['Priority'].lower()}"
                st.markdown(f"**Priority:** <span class='priority-badge {priority_class}'>{goal_data['Priority']}</span>", unsafe_allow_html=True)
                
                st.write(f"**Title:** {goal_data['Goal Title']}")
                st.write(f"**Category:** {goal_data['Category']}")
                
                # Status with color coding
                status_class = f"status-{goal_data['Status'].lower().replace(' ', '-')}"
                st.markdown(f"**Status:** <span class='{status_class}'>{goal_data['Status']}</span>", unsafe_allow_html=True)
                
                st.write(f"**Progress:** {goal_data['Progress']}%")
                st.write(f"**Target Date:** {goal_data['Target Date']}")
                st.write(f"**Start Date:** {goal_data['Start Date']}")
                
                if goal_data['Description']:
                    st.write(f"**Description:** {goal_data['Description']}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Update Progress")
                new_status = st.selectbox("Update Status", 
                                        ["Not Started", "In Progress", "On Hold", "Completed"])
                new_progress = st.slider("Update Progress", 0, 100, goal_data['Progress'])
                progress_notes = st.text_area("Progress Update Notes", 
                                            placeholder="What progress have you made? Any challenges?")
                
                if st.button("Update Goal Progress"):
                    # Update goal progress
                    mask = goals_df["Goal ID"] == goal_id
                    goals_df.loc[mask, "Status"] = new_status
                    goals_df.loc[mask, "Progress"] = new_progress
                    
                    # Append progress notes
                    current_notes = goals_df.loc[mask, "Notes"].iloc[0]
                    if pd.notna(current_notes) and current_notes != "":
                        updated_notes = f"{current_notes}\n\n{date.today()}: {progress_notes}"
                    else:
                        updated_notes = f"{date.today()}: {progress_notes}"
                    
                    goals_df.loc[mask, "Notes"] = updated_notes
                    goals_df.to_csv(GOALS_PATH, index=False)
                    st.success("Goal progress updated successfully!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.markdown('''
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem; font-weight: 700;">No Goals Set</div>
            <div style="color: #E0E7FF; font-size: 1rem; line-height: 1.6;">Create your first goal in the 'Set New Goal' tab to get started.</div>
        </div>
        ''', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">Goals Overview and Analysis</div>', unsafe_allow_html=True)
    
    if not goals_df.empty:
        # Goals by category
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Goals by Category")
        category_counts = goals_df["Category"].value_counts()
        for category, count in category_counts.items():
            st.write(f"- **{category}:** {count} goals")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Upcoming deadlines
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Upcoming Goal Deadlines")
        goals_df_temp = goals_df.copy()
        goals_df_temp['Target Date'] = pd.to_datetime(goals_df_temp['Target Date'])
        upcoming_goals = goals_df_temp[
            (goals_df_temp['Target Date'] >= pd.to_datetime(date.today())) & 
            (goals_df_temp['Target Date'] <= pd.to_datetime(date.today() + timedelta(days=30))) &
            (goals_df_temp['Status'] != 'Completed')
        ]
        
        if not upcoming_goals.empty:
            for _, goal in upcoming_goals.iterrows():
                days_until = (goal["Target Date"].date() - date.today()).days
                priority_class = f"priority-{goal['Priority'].lower()}"
                st.markdown(f"- **{goal['Goal Title']}** (due in {days_until} days) - <span class='priority-badge {priority_class}'>{goal['Priority']}</span> - Progress: {goal['Progress']}%", unsafe_allow_html=True)
        else:
            st.info("No upcoming goal deadlines in the next 30 days.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Overdue goals
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Overdue Goals")
        overdue_goals_list = goals_df_temp[
            (goals_df_temp['Target Date'] < pd.to_datetime(date.today())) & 
            (goals_df_temp['Status'] != 'Completed')
        ]
        
        if not overdue_goals_list.empty:
            for _, goal in overdue_goals_list.iterrows():
                days_overdue = (date.today() - goal["Target Date"].date()).days
                priority_class = f"priority-{goal['Priority'].lower()}"
                st.markdown(f"**{goal['Goal Title']}** - {days_overdue} days overdue - <span class='priority-badge {priority_class}'>{goal['Priority']}</span> - {goal['Progress']}% progress", unsafe_allow_html=True)
        else:
            st.success("No overdue goals")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # All goals table
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("All Goals")
        display_columns = ["Goal ID", "Goal Title", "Category", "Priority", "Status", "Progress", "Target Date"]
        st.dataframe(goals_df[display_columns], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export functionality
        if st.button("Download CSV", type="primary"):
            csv = goals_df.to_csv(index=False)
            st.download_button(
                label="Download Goals Data",
                data=csv,
                file_name=f"goals_data_{date.today()}.csv",
                mime="text/csv"
            )
    
    else:
        st.markdown('''
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem; font-weight: 700;">No Goals Available</div>
            <div style="color: #E0E7FF; font-size: 1rem; line-height: 1.6;">Start by setting your first goal to begin tracking your progress.</div>
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
if st.sidebar.button("View High Priority Goals", use_container_width=True):
    high_priority = goals_df[goals_df["Priority"].isin(["High", "Critical"])]
    if not high_priority.empty:
        st.sidebar.write("**High Priority Goals:**")
        for _, goal in high_priority.iterrows():
            st.sidebar.write(f"- {goal['Goal Title']} ({goal['Progress']}%)")
    else:
        st.sidebar.info("No high priority goals")

if st.sidebar.button("Refresh Data", use_container_width=True):
    st.rerun()

# Clean Footer
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); padding: 2rem 0 1rem 0; font-size: 0.9rem;">
    OrbitMe Goal Tracking v2.1 • Strategic • Measurable • Achievable
</div>
""", unsafe_allow_html=True)