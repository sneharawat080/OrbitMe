import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(layout="wide")

st.title("📊 Dashboard - Your Progress at a Glance")

health_path = './data/health_data.csv'
work_path = './data/work_data.csv'

# Read Data
if os.path.exists(health_path):
    health_df = pd.read_csv(health_path)
else:
    health_df = pd.DataFrame(columns=["Date", "Steps", "Water (Litres)", "Sleep Hours", "Mood (1-10)", "Weight (kg)", "Ate Healthy", "Exercise", "Stress Level (1-10)", "Note"])

if os.path.exists(work_path):
    work_df = pd.read_csv(work_path)
else:
    work_df = pd.DataFrame(columns=["Task Title", "Task Description", "Status", "Hours Spent", "Progress %", "Deadline", "Date Created", "Note"])

# ---------------- Health Overview -----------------
st.header("💪 Health Overview")

if not health_df.empty:
    health_df["Date"] = pd.to_datetime(health_df["Date"]).dt.date
    avg_steps = int(health_df["Steps"].mean())
    avg_water = round(health_df["Water (Litres)"].mean(), 1)
    avg_sleep = round(health_df["Sleep Hours"].mean(), 1)
    avg_mood = round(health_df["Mood (1-10)"].mean(), 1)
    avg_stress = round(health_df["Stress Level (1-10)"].mean(), 1)

    st.subheader("📈 Averages at a Glance")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Steps (Avg)", avg_steps)
    col2.metric("Water (L)", avg_water)
    col3.metric("Sleep (Hrs)", avg_sleep)
    col4.metric("Mood (1-10)", avg_mood)
    col5.metric("Stress (1-10)", avg_stress)

    st.subheader("📊 Health Trends Over Time")
    health_df_sorted = health_df.sort_values("Date")
    health_df_sorted.set_index("Date", inplace=True)

    # Normalized Scale for Graph Comparison
    normalized_health = health_df_sorted[["Steps", "Water (Litres)", "Sleep Hours"]].copy()
    normalized_health["Steps"] = normalized_health["Steps"] / normalized_health["Steps"].max() * 100
    normalized_health["Water (Litres)"] = normalized_health["Water (Litres)"] / normalized_health["Water (Litres)"].max() * 100
    normalized_health["Sleep Hours"] = normalized_health["Sleep Hours"] / normalized_health["Sleep Hours"].max() * 100

    st.line_chart(normalized_health)

    st.subheader("📝 Full Health Records")
    st.dataframe(health_df)
else:
    st.warning("No health data found.")


# ---------------- Work Overview -----------------
st.header("🚀 Work Overview")

if not work_df.empty:
    work_df["Date Created"] = pd.to_datetime(work_df["Date Created"]).dt.date
    work_df["Hours Spent"] = pd.to_numeric(work_df["Hours Spent"], errors='coerce').fillna(0)

    st.subheader("📈 Work Summary Metrics")
    col1, col2, col3 = st.columns(3)
    total_hours = int(work_df["Hours Spent"].sum())
    total_tasks = work_df.shape[0]
    completed_tasks = work_df[work_df["Status"] == "Done"].shape[0]
    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completed", completed_tasks)
    col3.metric("Hours Spent", total_hours)

    st.subheader("📊 Work Hours Per Day (Date Only)")
    work_summary = work_df.groupby("Date Created")["Hours Spent"].sum()
    st.bar_chart(work_summary)

    st.subheader("📈 Task Status Breakdown")

    status_counts = work_df["Status"].value_counts()
    fig, ax = plt.subplots(figsize=(2, 2), facecolor='#0E1117')  # Small pie chart
    ax.set_facecolor("#0E1117")
    wedges, texts, autotexts = ax.pie(
        status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90,
        colors=sns.color_palette('pastel'), textprops={'color': 'white'}
    )
    plt.setp(autotexts, color='white', weight='bold')
    ax.axis('equal')
    st.pyplot(fig)

    st.subheader("📝 Full Work Records")
    st.dataframe(work_df)
else:
    st.warning("No work data found.")
