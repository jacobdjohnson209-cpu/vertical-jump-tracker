import streamlit as st
import pandas as pd
import datetime
import os

# Set up the webpage title
st.title("🏀 Vertical Jump Tracker")

# File to store history
DATA_FILE = "jump_history.csv"

# Function to load history
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Date", "Weight", "Readiness", "Reach", "Touch", "Vertical", "Jumps"])

# Load existing history
df = load_data()

# --- Input Section ---
st.subheader("Log Today's Session")
col1, col2 = st.columns(2)

with col1:
    weight = st.number_input("Bodyweight (lbs)", min_value=100.0, max_value=250.0, value=165.0)
    readiness = st.slider("Readiness Score (1-10)", 1, 10, 8)
    total_jumps = st.number_input("Total Jumps", min_value=1, max_value=50, value=12)

with col2:
    reach = st.number_input("Standing Reach (in)", min_value=70.0, value=90.0)
    touch = st.number_input("Max Touch (in)", min_value=80.0, value=114.0)

# Calculate Vertical
vertical = touch - reach
st.metric(label="Today's Vertical", value=f"{vertical} inches")

# Save Button
if st.button("Save to History"):
    new_data = pd.DataFrame([{
        "Date": datetime.date.today().strftime("%Y-%m-%d"),
        "Weight": weight, "Readiness": readiness, "Reach": reach, 
        "Touch": touch, "Vertical": vertical, "Jumps": total_jumps
    }])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Session Saved!")

# --- History & Analytics Section ---
st.divider()
st.subheader("Your Progress History")

if not df.empty:
    # Show the line chart of jump progress
    st.line_chart(df.set_index("Date")["Vertical"])
    # Show the raw data table
    st.dataframe(df)
else:
    st.info("No data yet. Log your first jump to see your history!")