import streamlit as st
import pandas as pd
import os
from datetime import date, datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="OrbitMe - Work Management",
    layout="wide",
    page_icon="⚡",
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
    
    /* Sidebar button styling */
    .sidebar-button {
        width: 100%;
        background: rgba(255, 255, 255, 0.1);
        color: #E0E7FF;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-button:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-1px);
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
    
    .status-review {
        color: #FFA726;
        font-weight: 600;
    }
    
    .status-not-started {
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
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div style="padding: 2rem 0 1rem 0;">
    <div class="main-header">Work Management</div>
    <div style="text-align: center; color: #E0E7FF; font-size: 1.2rem; margin-bottom: 1rem; font-weight: 300;">
        Advanced project and task management system
    </div>
</div>
""", unsafe_allow_html=True)

DATA_PATH = './data/work_data.csv'
os.makedirs('./data', exist_ok=True)

# Initialize work data
default_columns = [
    "Task Title", "Task Description", "Category", "Priority", "Status", 
    "Hours Spent", "Progress", "Deadline", "Date Created", "Tags", "Note"
]

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    # Convert date columns to datetime
    if not df.empty:
        if 'Deadline' in df.columns:
            df['Deadline'] = pd.to_datetime(df['Deadline']).dt.date
        if 'Date Created' in df.columns:
            df['Date Created'] = pd.to_datetime(df['Date Created']).dt.date
else:
    df = pd.DataFrame(columns=default_columns)
    df.to_csv(DATA_PATH, index=False)

# Quick Stats Section
if not df.empty:
    st.markdown('<div class="section-header">Work Overview</div>', unsafe_allow_html=True)
    
    total_tasks = len(df)
    completed_tasks = len(df[df["Status"] == "Completed"])
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    if 'Hours Spent' in df.columns:
        total_hours = df['Hours Spent'].sum()
    else:
        total_hours = 0
    
    # Count overdue tasks
    today_date = date.today()
    if 'Deadline' in df.columns:
        df_deadlines = df.copy()
        df_deadlines['Deadline'] = pd.to_datetime(df_deadlines['Deadline']).dt.date
        overdue_tasks = len(df_deadlines[
            (df_deadlines['Deadline'] < today_date) & 
            (df_deadlines['Status'] != 'Completed')
        ])
    else:
        overdue_tasks = 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Total Tasks</div>
            <div class="stats-number">{total_tasks}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Active Projects</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Completion Rate</div>
            <div class="stats-number">{completion_rate:.0f}%</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">{completed_tasks}/{total_tasks} Tasks</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Hours Invested</div>
            <div class="stats-number">{total_hours}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Productive Time</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="stats-card">
            <div class="stats-label">Overdue Tasks</div>
            <div class="stats-number">{overdue_tasks}</div>
            <div style="color: #E0E7FF; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">Require Attention</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Task Management Interface
tab1, tab2, tab3 = st.tabs(["Add New Task", "Update Tasks", "Task Analysis"])

with tab1:
    st.markdown('<div class="section-header">Create New Task</div>', unsafe_allow_html=True)
    
    with st.form("task_creation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Task Title", placeholder="Enter task title")
            category = st.selectbox("Category", ["Work", "Personal", "Learning", "Health", "Other"])
            priority = st.select_slider("Priority", options=["Low", "Medium", "High", "Critical"])
            hours = st.number_input("Time Estimate (Hours)", 0, 100, 1)
        
        with col2:
            description = st.text_area("Task Description", placeholder="Detailed description...")
            status = st.selectbox("Initial Status", ["Not Started", "In Progress", "Review", "Completed"])
            progress = st.slider("Initial Progress (%)", 0, 100, 0)
            deadline = st.date_input("Deadline", date.today() + timedelta(days=7))
        
        tags = st.text_input("Tags (comma-separated)", placeholder="urgent, important, project")
        note = st.text_area("Additional Notes")
        
        submitted = st.form_submit_button("Create Task")
        
        if submitted:
            if not title:
                st.warning("Task title is required.")
            else:
                new_task = pd.DataFrame([[
                    title, description, category, priority, status,
                    hours, f"{progress}%", deadline, date.today(), tags, note
                ]], columns=default_columns)
                
                # Load existing data and append new task
                if os.path.exists(DATA_PATH):
                    existing_df = pd.read_csv(DATA_PATH)
                    updated_df = pd.concat([existing_df, new_task], ignore_index=True)
                else:
                    updated_df = new_task
                
                # Convert date columns before saving
                if 'Deadline' in updated_df.columns:
                    updated_df['Deadline'] = pd.to_datetime(updated_df['Deadline']).dt.date
                if 'Date Created' in updated_df.columns:
                    updated_df['Date Created'] = pd.to_datetime(updated_df['Date Created']).dt.date
                
                updated_df.to_csv(DATA_PATH, index=False)
                df = updated_df  # Update the current dataframe
                st.success("Task created successfully!")
                st.rerun()

with tab2:
    st.markdown('<div class="section-header">Manage Existing Tasks</div>', unsafe_allow_html=True)
    
    if not df.empty:
        # Task selection for updates
        task_list = df["Task Title"].tolist()
        selected_task = st.selectbox("Select Task to Update", task_list)
        
        if selected_task:
            task_data = df[df["Task Title"] == selected_task].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Current Status")
                
                # Priority badge
                priority_class = f"priority-{task_data['Priority'].lower()}"
                st.markdown(f"**Priority:** <span class='priority-badge {priority_class}'>{task_data['Priority']}</span>", unsafe_allow_html=True)
                
                st.write(f"**Title:** {task_data['Task Title']}")
                st.write(f"**Description:** {task_data['Task Description']}")
                
                # Status with color coding
                status_class = f"status-{task_data['Status'].lower().replace(' ', '-')}"
                st.markdown(f"**Status:** <span class='{status_class}'>{task_data['Status']}</span>", unsafe_allow_html=True)
                
                st.write(f"**Progress:** {task_data['Progress']}")
                st.write(f"**Deadline:** {task_data['Deadline']}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Update Task")
                new_status = st.selectbox("Update Status", 
                                        ["Not Started", "In Progress", "Review", "Completed"])
                # Safely extract progress percentage
                current_progress = task_data['Progress']
                if isinstance(current_progress, str) and '%' in current_progress:
                    current_progress_val = int(current_progress.rstrip('%'))
                else:
                    current_progress_val = int(current_progress) if pd.notna(current_progress) else 0
                
                new_progress = st.slider("Update Progress", 0, 100, current_progress_val)
                additional_hours = st.number_input("Additional Hours Spent", 0, 24, 0)
                update_note = st.text_area("Update Notes")
                
                if st.button("Apply Updates"):
                    # Update the task
                    mask = df["Task Title"] == selected_task
                    
                    # Convert hours to numeric and handle NaN values
                    current_hours = df.loc[mask, "Hours Spent"]
                    if pd.api.types.is_numeric_dtype(current_hours):
                        current_hours_val = current_hours.iloc[0] if not current_hours.empty else 0
                    else:
                        current_hours_val = int(current_hours.iloc[0]) if not current_hours.empty else 0
                    
                    df.loc[mask, "Status"] = new_status
                    df.loc[mask, "Progress"] = f"{new_progress}%"
                    df.loc[mask, "Hours Spent"] = current_hours_val + additional_hours
                    
                    # Append update note
                    current_note = df.loc[mask, "Note"].iloc[0] if not df.loc[mask, "Note"].empty else ""
                    if pd.notna(current_note) and current_note != "":
                        updated_note = f"{current_note} | {date.today()}: {update_note}"
                    else:
                        updated_note = f"{date.today()}: {update_note}"
                    
                    df.loc[mask, "Note"] = updated_note
                    
                    # Save updated dataframe
                    df.to_csv(DATA_PATH, index=False)
                    st.success("Task updated successfully!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.markdown('''
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem; font-weight: 700;">No Tasks Available</div>
            <div style="color: #E0E7FF; font-size: 1rem; line-height: 1.6;">Create your first task in the 'Add New Task' tab to get started.</div>
        </div>
        ''', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">Task Analysis</div>', unsafe_allow_html=True)
    
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Task Statistics")
            
            # Priority distribution
            if 'Priority' in df.columns:
                priority_counts = df["Priority"].value_counts()
                st.write("**Tasks by Priority:**")
                for priority, count in priority_counts.items():
                    priority_class = f"priority-{priority.lower()}"
                    st.markdown(f"- <span class='priority-badge {priority_class}'>{priority}</span>: {count} tasks", unsafe_allow_html=True)
            
            # Status distribution
            if 'Status' in df.columns:
                status_counts = df["Status"].value_counts()
                st.write("**Tasks by Status:**")
                for status, count in status_counts.items():
                    status_class = f"status-{status.lower().replace(' ', '-')}"
                    st.markdown(f"- <span class='{status_class}'>{status}</span>: {count} tasks", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Upcoming Deadlines")
            
            # Upcoming deadlines
            if 'Deadline' in df.columns:
                # Ensure both are date objects for comparison
                today_date = date.today()
                next_week = today_date + timedelta(days=7)
                
                # Convert to date if needed and filter
                df_deadlines = df.copy()
                df_deadlines['Deadline'] = pd.to_datetime(df_deadlines['Deadline']).dt.date
                
                upcoming_tasks = df_deadlines[
                    (df_deadlines['Deadline'] >= today_date) & 
                    (df_deadlines['Deadline'] <= next_week) &
                    (df_deadlines['Status'] != 'Completed')
                ]
                
                if not upcoming_tasks.empty:
                    for _, task in upcoming_tasks.iterrows():
                        days_until = (task["Deadline"] - today_date).days
                        priority_class = f"priority-{task['Priority'].lower()}"
                        st.markdown(f"- **{task['Task Title']}** (in {days_until} days) - <span class='priority-badge {priority_class}'>{task['Priority']}</span> - Progress: {task['Progress']}", unsafe_allow_html=True)
                else:
                    st.info("No tasks due in the next 7 days.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Overdue tasks
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Overdue Tasks")
        if 'Deadline' in df.columns:
            overdue_tasks = df_deadlines[df_deadlines['Deadline'] < today_date]
            overdue_incomplete = overdue_tasks[overdue_tasks['Status'] != 'Completed']
            
            if not overdue_incomplete.empty:
                for _, task in overdue_incomplete.iterrows():
                    days_overdue = (today_date - task["Deadline"]).days
                    priority_class = f"priority-{task['Priority'].lower()}"
                    st.markdown(f"**{task['Task Title']}** - {days_overdue} days overdue - <span class='priority-badge {priority_class}'>{task['Priority']}</span> - {task['Progress']} progress", unsafe_allow_html=True)
            else:
                st.success("No overdue tasks")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Full task list
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("All Tasks")
        display_columns = [col for col in ["Task Title", "Category", "Priority", "Status", "Progress", "Deadline"] if col in df.columns]
        st.dataframe(df[display_columns], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export functionality
        if st.button("Download CSV", type="primary"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Task Data",
                data=csv,
                file_name=f"task_data_{date.today()}.csv",
                mime="text/csv"
            )

    else:
        st.markdown('''
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem; font-weight: 700;">No Data Available</div>
            <div style="color: #E0E7FF; font-size: 1rem; line-height: 1.6;">Create tasks to see analytics and insights about your work patterns.</div>
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

# Simple sidebar buttons without emojis
if st.sidebar.button("View Overdue Tasks", use_container_width=True):
    if not df.empty and 'Deadline' in df.columns:
        today_date = date.today()
        df_deadlines = df.copy()
        df_deadlines['Deadline'] = pd.to_datetime(df_deadlines['Deadline']).dt.date
        
        overdue = df_deadlines[
            (df_deadlines['Deadline'] < today_date) & 
            (df_deadlines['Status'] != 'Completed')
        ]
        
        if not overdue.empty:
            st.sidebar.write("**Overdue Tasks:**")
            for _, task in overdue.iterrows():
                days_overdue = (today_date - task["Deadline"]).days
                st.sidebar.write(f"- {task['Task Title']} ({days_overdue} days overdue)")
        else:
            st.sidebar.info("No overdue tasks.")

# Refresh data button
if st.sidebar.button("Refresh Data", use_container_width=True):
    st.rerun()

# Clean Footer
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); padding: 2rem 0 1rem 0; font-size: 0.9rem;">
    OrbitMe Work Management v2.1 • Organized • Efficient • Productive
</div>
""", unsafe_allow_html=True)