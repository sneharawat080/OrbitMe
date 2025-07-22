import streamlit as st
import pandas as pd
import os
from datetime import date

st.title("💪 Health Orbit - Health Tracking")

DATA_PATH = "./data/health_data.csv"
HEADERS = ["Date", "Steps", "Water (Litres)", "Sleep Hours", "Sleep Quality (1-5)", "Mood (1-10)", "Weight (kg)", "Calories", "Ate Healthy", "Exercise", "Stress Level (1-10)", "Note"]

if not os.path.exists(DATA_PATH):
    pd.DataFrame(columns=HEADERS).to_csv(DATA_PATH, index=False)

steps = st.number_input("Steps Walked", min_value=0, step=500)
water = st.number_input("Water Intake (Litres)", min_value=0.0, step=0.5, format="%.1f")
sleep_hours = st.number_input("Sleep Hours", min_value=0, max_value=24)
sleep_quality = st.slider("Sleep Quality (1-5)", 1, 5)
mood = st.slider("Mood (1-10)", 1, 10)
weight = st.number_input("Weight (kg)", min_value=20, max_value=200)
calories = st.number_input("Calories Eaten", min_value=0, step=50)
ate_healthy = st.radio("Ate Healthy Today?", ["Yes", "No"])
exercise = st.radio("Did Exercise Today?", ["Yes", "No"])
stress_level = st.slider("Stress Level (1-10)", 1, 10)
note = st.text_area("Note")
today = st.date_input("Date", date.today())

if st.button("💾 Save Health Data"):
    new_health = pd.DataFrame([[today, steps, water, sleep_hours, sleep_quality, mood, weight, calories, ate_healthy, exercise, stress_level, note]], columns=HEADERS)
    new_health.to_csv(DATA_PATH, mode='a', header=False, index=False)
    st.success("✅ Health Data Saved!")

st.divider()
st.header("📊 Health Records")
df = pd.read_csv(DATA_PATH)
st.dataframe(df)
