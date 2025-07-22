import streamlit as st
import pandas as pd
import os
from datetime import date

st.title("🚀 Work Orbit - Organize, Track & Reflect")

DATA_PATH = './data/work_data.csv'

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame(columns=["Task Title", "Task Description", "Status", "Hours Spent", "Progress %", "Deadline", "Date Created", "Note"])
    df.to_csv(DATA_PATH, index=False)

st.header("➕ Add New Task")

title = st.text_input("Task Title")
desc = st.text_area("Task Description")
hours = st.number_input("Hours Spent", 0, 24)
progress = st.slider("Progress (%)", 0, 100)
status = st.selectbox("Task Status", ["Not Done", "In Progress", "Done"])
deadline = st.date_input("Deadline", date.today())
task_date = date.today()
note = st.text_area("Note for this Task")

if st.button("Save Task"):
    if not title or not desc:
        st.warning("⚠️ Please fill in both Task Title and Description before saving.")
    else:
        new_task = pd.DataFrame([[title, desc, status, hours, f"{progress}%", deadline, task_date, note]], columns=df.columns)
        df = pd.concat([df, new_task], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        st.success("✅ Task Saved Successfully!")

st.header("✏️ Update Existing Task Status / Progress")

if not df.empty:
    selected_task = st.selectbox("Select Task to Update", df["Task Title"].tolist())
    new_status = st.selectbox("Update Status To", ["Not Done", "In Progress", "Done"])
    new_progress = st.slider("Update Progress (%)", 0, 100)

    if st.button("Update Task"):
        df.loc[df["Task Title"] == selected_task, "Status"] = new_status
        df.loc[df["Task Title"] == selected_task, "Progress %"] = f"{new_progress}%"
        df.to_csv(DATA_PATH, index=False)
        st.success(f"✅ '{selected_task}' updated to '{new_status}' with progress {new_progress}%!")

st.header("📋 Current Work Tasks")
st.dataframe(df)
