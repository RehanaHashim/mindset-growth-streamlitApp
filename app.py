
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App title

st.title("Health and Fitness Tracker")

# Sidebar for user input
st.sidebar.header("Daily Health Metrics")

# Input fields
date = st.sidebar.date_input("Date")
weight = st.sidebar.number_input("Weight (kg)", min_value=0.0)
calories_intake = st.sidebar.number_input("Calories Intake", min_value=0)
calories_burned = st.sidebar.number_input("Calories Burned", min_value=0)
exercise = st.sidebar.text_input("Exercise Done")

# Save data to a CSV file
def save_data(date, weight, calories_intake, calories_burned, exercise):
    data = {
        "Date": [date],
        "Weight (kg)": [weight],
        "Calories Intake": [calories_intake],
        "Calories Burned": [calories_burned],
        "Exercise": [exercise]
    }
    df = pd.DataFrame(data)
    df.to_csv("health_data.csv", mode="a", header=not pd.io.common.file_exists("health_data.csv"), index=False)

# Load existing data
def load_data():
    try:
        df = pd.read_csv("health_data.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Weight (kg)", "Calories Intake", "Calories Burned", "Exercise"])
    return df

# Save button
if st.sidebar.button("Save Data"):
    save_data(date, weight, calories_intake, calories_burned, exercise)
    st.sidebar.success("Data saved successfully!")

# Load and display data
df = load_data()
st.header("Your Health Data")
st.write(df)

# Visualizations
st.header("Progress Tracking")

# Weight Progress
if not df.empty:
    st.subheader("Weight Progress")
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Weight (kg)"], marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (kg)")
    ax.set_title("Weight Over Time")
    st.pyplot(fig)

# Calories Intake vs Burned
if not df.empty:
    st.subheader("Calories Intake vs Burned")
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Calories Intake"], label="Calories Intake", marker="o")
    ax.plot(df["Date"], df["Calories Burned"], label="Calories Burned", marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories")
    ax.set_title("Calories Intake vs Burned")
    ax.legend()
    st.pyplot(fig)

# Recommendations
st.header("Recommendations")
if not df.empty:
    latest_weight = df["Weight (kg)"].iloc[-1]
    latest_calories_intake = df["Calories Intake"].iloc[-1]
    latest_calories_burned = df["Calories Burned"].iloc[-1]

    if latest_calories_intake > latest_calories_burned:
        st.warning("You are consuming more calories than you are burning. Consider increasing your exercise or reducing calorie intake.")
    else:
        st.success("Great job! You are burning more calories than you are consuming.")

    if latest_weight > df["Weight (kg)"].iloc[0]:
        st.warning("Your weight has increased. Consider adjusting your diet and exercise routine.")
    elif latest_weight < df["Weight (kg)"].iloc[0]:
        st.success("Congratulations! Your weight has decreased.")
    else:
        st.info("Your weight is stable. Keep up the good work!")
   
     