import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# ---------- STEP 1: Load Data ----------
df = pd.read_excel("Data.xlsx")

# Drop serial/index-like columns if exist
if "SL No" in df.columns:
    df.drop(columns=["SL No"], inplace=True)

# ---------- STEP 2: Handle Missing Values ----------
df = df.fillna(df.median(numeric_only=True))   # fill numeric NaN with median
df = df.fillna("Unknown")  # fill string NaN if any

# ---------- STEP 3: Normalize Numeric Columns ----------
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

scaler = MinMaxScaler()
df_normalized = df.copy()
df_normalized[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# ---------- STEP 4: Feature Engineering ----------
# Calories breakdown (approximate: 4 kcal/g protein/carb, 9 kcal/g fat)
df_normalized["Protein_Calorie_%"] = (df["Protein"] * 4 / df["Caloric Value"]) * 100
df_normalized["Carb_Calorie_%"] = (df["Carbohydrates"] * 4 / df["Caloric Value"]) * 100
df_normalized["Fat_Calorie_%"] = (df["Fat"] * 9 / df["Caloric Value"]) * 100

# Protein per 100 kcal (density measure)
df_normalized["Protein_per_100kcal"] = (df["Protein"] / df["Caloric Value"]) * 100

# Micronutrient Density Score
micronutrients = [
    "Vitamin A", "Vitamin B1", "Vitamin B11", "Vitamin B12", "Vitamin B2",
    "Vitamin B3", "Vitamin B5", "Vitamin B6", "Vitamin C", "Vitamin D",
    "Vitamin E", "Vitamin K", "Calcium", "Copper", "Iron", "Magnesium",
    "Manganese", "Phosphorus", "Potassium", "Selenium", "Zinc"
]

df_normalized["Micronutrient_Density"] = df[micronutrients].mean(axis=1)

# ---------- STEP 5: Save Processed Dataset ----------
df_normalized.to_excel("Data_Normalized.xlsx", index=False)

print("✅ Dataset normalized & saved as Data_Normalized.xlsx")
