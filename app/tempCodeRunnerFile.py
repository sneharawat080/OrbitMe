import streamlit as st

st.set_page_config(
    page_title="OrbitMe - Your Life OS",
    layout="wide",
    page_icon="🌍"
)

st.markdown("<h1 style='text-align: center;'>🌍 OrbitMe</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: grey;'>Your Personal Operating System for Work, Health & Self-Discipline</h3>", unsafe_allow_html=True)

st.divider()

st.subheader("🚀 Why OrbitMe?")
st.markdown("""
**OrbitMe** helps you master your life by tracking:
- **Work Productivity:** Manage tasks, progress & goals.
- **Health Habits:** Steps, Hydration, Sleep, Mood.
- **Self Reflection:** Daily notes, weekly insights.
""")

st.divider()

st.subheader("🎯 Key Features")
col1, col2, col3 = st.columns(3)
with col1:
    st.success("📋 Task Management\n- Set Targets\n- Auto Progress Tracking\n- Weekly Reflection")
with col2:
    st.info("💪 Health Tracker\n- Steps, Water, Sleep\n- Mood, Healthy Habits\n- Monthly Health Score")
with col3:
    st.warning("📊 Dashboard Insights\n- Graphs\n- Reports\n- Export to PDF / CSV")

st.divider()

st.subheader("✨ Motivation of the Day")
st.markdown("> *Discipline is choosing between what you want now and what you want most.*")

st.divider()

