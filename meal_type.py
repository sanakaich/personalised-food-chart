import pandas as pd

# Load dataset
df = pd.read_excel("Data.xlsx")

# Non-edible or ingredient keywords
non_edible_keywords = [
    "oil", "butter", "fat", "grease", "lard", "syrup", "vinegar", "sauce",
    "gravy", "powder", "spice", "seasoning", "salt", "sugar", "extract",
    "flour", "yeast", "baking", "mix", "starch", "gelatin", "pectin",
    "dressing", "essence", "seeds", "kernel", "bran", "meal"
]

# Expanded rules for meals
rules = {
    "Breakfast": [
        "egg", "omelet", "pancake", "muffin", "toast", "cereal", "oats", "oatmeal",
        "porridge", "idli", "dosa", "upma", "poha", "paratha", "bagel", "croissant",
        "yogurt", "lassi", "waffle", "donut", "jam", "honey", "tea", "coffee", "milk",
        "smoothie"
    ],
    "Lunch": [
        "rice", "biryani", "sandwich", "burger", "wrap", "shawarma", "chicken", "fish", 
        "beef", "mutton", "pork", "dal", "paneer", "sabji", "roti", "chapati", "thali",
        "noodle", "pasta", "curry", "quesadilla", "enchilada", "burrito", "taco",
        "paratha", "fried rice", "kebab", "cutlet", "idli sambar", "pulao", "pav bhaji"
    ],
    "Dinner": [
        "steak", "soup", "stew", "gravy", "chowder", "chop", "roast", "lasagna",
        "pizza", "spaghetti", "fajita", "saute", "fillet", "cutlet", "meatloaf",
        "dal", "sabji", "paneer", "biryani", "thali", "curry", "roti", "naan",
        "pulao", "fried rice", "korma"
    ],
    "Snacks": [
        "chips", "fries", "pakora", "samosa", "vada", "bhel", "chaat", "puff",
        "roll", "spring roll", "nuts", "candy", "chocolate", "cookie", "crackers",
        "pastry", "pie", "cake", "snack", "fudge", "jelly", "pudding", "ice cream",
        "bar", "spread", "granola", "fruit", "kachori", "momo", "dumpling", "nachos",
        "biscuits", "toast", "sev"
    ]
}

def assign_meal(food_name):
    food_name = str(food_name).lower()

    # Step 1: Filter out non-edibles
    if any(kw in food_name for kw in non_edible_keywords):
        return ""  # Null → won’t show in dashboard

    # Step 2: Assign meal type
    assigned = []
    for meal, keywords in rules.items():
        if any(kw in food_name for kw in keywords):
            assigned.append(meal)

    if not assigned:
        return "Lunch,Dinner"  # fallback default

    return ",".join(sorted(set(assigned)))

# Apply tagging
df["Meal_Type"] = df["food"].apply(assign_meal)

# Save updated dataset
df.to_excel("Data_with_MealType.xlsx", index=False)
print("✅ Meal_Type column added. Non-edible items set to null.")
