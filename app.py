import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import plotly.express as px

# ----------------------------
# Load & Normalize Dataset
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Data.xlsx", sheet_name="Sheet1")
    
    # Normalize numeric columns
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    scaler = MinMaxScaler()
    df_normalized = df.copy()
    df_normalized[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    return df, df_normalized

df, df_normalized = load_data()

# ----------------------------
# BMR & Calorie Calculation
# ----------------------------
def calculate_calories(weight, height, age, gender, activity_level, goal):
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    activity_factors = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    
    daily_calories = bmr * activity_factors[activity_level]
    
    if goal == "Lose Weight":
        daily_calories -= 500
    elif goal == "Gain Weight":
        daily_calories += 500
    
    return round(daily_calories)

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Personalized Food Chart", layout="wide")

st.sidebar.header("User Information")

weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=25)
gender = st.sidebar.radio("Gender", ["Male", "Female"])
activity_level = st.sidebar.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
goal = st.sidebar.selectbox("Goal", ["Maintain Weight", "Lose Weight", "Gain Weight"])

daily_calories = calculate_calories(weight, height, age, gender, activity_level, goal)

st.title("🥗 Personalized Food Chart Dashboard")
st.subheader(f"Daily Calorie Requirement: 🔥 {daily_calories} kcal")

# ----------------------------
# Meal Recommendations
# ----------------------------
st.header("Recommended Meals")

meal_ratios = {"Breakfast": 0.3, "Lunch": 0.4, "Dinner": 0.25, "Snacks": 0.05}
meal_plans = {}

for meal, ratio in meal_ratios.items():
    meal_calories = daily_calories * ratio
    avg_cal = meal_calories / 5
    
    df["Calorie_Diff"] = abs(df["Caloric Value"] - avg_cal)
    meal_items = df.sort_values("Calorie_Diff").head(5)
    meal_plans[meal] = meal_items
    
    st.subheader(f"{meal} ({round(meal_calories)} kcal)")
    st.table(meal_items[["food", "Caloric Value", "Protein", "Fat", "Carbohydrates"]])

# ----------------------------
# Charts
# ----------------------------
st.header("📊 Nutrition Breakdown")

# Combine all selected items
combined = pd.concat(meal_plans.values())
macro_summary = combined[["Protein", "Fat", "Carbohydrates"]].sum()

# Bar Chart for Macros
fig = px.bar(
    macro_summary,
    x=macro_summary.index,
    y=macro_summary.values,
    title="Macronutrient Distribution",
    labels={"x": "Nutrient", "y": "Amount (g)"}
)
st.plotly_chart(fig, use_container_width=True)

# Pie Chart for Calories per Meal
calories_per_meal = {meal: df["Caloric Value"].mean() * 5 for meal, df in meal_plans.items()}
fig2 = px.pie(
    names=list(calories_per_meal.keys()),
    values=list(calories_per_meal.values()),
    title="Calories Distribution per Meal"
)
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# Food Search
# ----------------------------
st.header("🔍 Search Food")
search = st.text_input("Enter food name:")
if search:
    results = df[df["food"].str.contains(search, case=False)]
    st.dataframe(results)

# ----------------------------
# Export Meal Plan
# ----------------------------
st.header("📤 Export Meal Plan")
if st.button("Export to Excel"):
    output = pd.ExcelWriter("meal_plan.xlsx", engine="xlsxwriter")
    for meal, items in meal_plans.items():
        items.to_excel(output, sheet_name=meal, index=False)
    output.close()
    st.success("✅ Meal plan exported as 'meal_plan.xlsx'")
