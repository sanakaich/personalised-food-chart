# 🥗 Personalized Food Recommendation Dashboard

## 📌 Project Overview
This project is an **interactive Streamlit dashboard** that generates a **customized daily food plan** based on user details such as **age, weight, height, gender, activity level, and health goals** (maintain, lose, or gain weight).  

It leverages a **nutritional dataset** of food items with detailed attributes (calories, protein, fat, carbs, vitamins, minerals, etc.) and a **Meal_Type column** (Breakfast, Lunch, Dinner, Snacks) to recommend **feasible and realistic meal options**.

---

## ✨ Features
- 🔢 **User Input Form** – Enter weight, height, age, gender, activity level, and goal.
- 🔥 **BMR & Calorie Calculation** – Calculates daily calorie needs using the Mifflin-St Jeor equation.
- 🍽️ **Meal Distribution** – Splits calories into:
  - Breakfast (30%)
  - Lunch (40%)
  - Dinner (25%)
  - Snacks (5%)
- 🥘 **Filtered Meal Recommendations** – Selects top 5 foods per meal **only from items tagged with Meal_Type**.
- 📊 **Interactive Charts** – Macronutrient distribution (bar chart) & calorie split (pie chart).
- 🔍 **Food Search** – Search any food item from the dataset.
- 📤 **Export Plan** – Export the full meal plan to Excel.

---

## 🛠️ Tech Stack
- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Scikit-learn](https://scikit-learn.org/) (for normalization)
- [Plotly Express](https://plotly.com/python/plotly-express/) (charts)
- [ExcelWriter (xlsxwriter)](https://xlsxwriter.readthedocs.io/)

---

## 📂 Dataset
The dataset contains food items with nutritional values per 100g, including:
- **Macronutrients**: Calories, Protein, Fat, Carbohydrates, Sugars, Fiber  
- **Micronutrients**: Vitamins (A, B, C, D, E, K), Minerals (Calcium, Iron, Zinc, etc.)  
- **Other**: Cholesterol, Sodium, Water, Nutrition Density  
- **Meal_Type**: Added column classifying food into Breakfast, Lunch, Dinner, Snacks (kept empty for non-edible/ingredient-only items)

---
