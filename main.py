###main.py

#need this for the recipes.json (interact w os)
import os
from recommender import load_recipes, recommend, print_recommendations

def get_weights_input():
    # The four criteria the user can rank defined here
    criteria = ["weather", "budget", "ingredients", "meal_type"]

    # Get user input
    print("\nRank what matters most to you today (1 = most important):")
    print("  Criteria: weather, budget, ingredients, meal_type")
    print("  Example input: budget, weather, meal_type, ingredients")

    raw = input("Your ranking: ").strip().lower()

    # Split the input by commas and clean up whitespace around each item
    ranked = [r.strip() for r in raw.split(",") if r.strip()]

    # Points attributed in order of ranking
    point_values = [3, 2.5, 2, 1.5]
    weights = {}

    for i, criterion in enumerate(ranked):
        # Only assign a weight if the criterion is valid and we haven't run out of point values
        if criterion in criteria and i < len(point_values):
            weights[criterion] = point_values[i]

    # Any criterion the user left out still needs a weight so the code
    # doesn't crash. 1.0 means it still counts, just least important
    for criterion in criteria:
        if criterion not in weights:
            weights[criterion] = 1.0

    return weights


def get_weather_input():
    print("\nSi eshte koha sot? (What is the weather like today?)")
    print("  1. Cold (ftohte)")
    print("  2. Warm (ngrohte)")
    print("  3. Any (S'ka rendesi)")
    #strip removes any spaces or newlines from what the user typed
    choice = input("Choose (1/2/3): ").strip()
    return {"1": "cold", "2": "warm", "3": "any"}.get(choice, "any")


def get_budget_input():
    print("\nCili eshte buxheti juaj? (What is your budget today?)")
    print("  1. Low (i ulet)")
    print("  2. Medium (mesatar)")
    print("  3. High (i larte)")
    choice = input("Choose (1/2/3): ").strip()
    return {"1": "low", "2": "medium", "3": "high"}.get(choice, "medium")


def get_meal_type_input():
    print("\nCilin vakt do te pergatisni? (Which meal are you preparing?)")
    print("  1. Breakfast (mengjes)")
    print("  2. Lunch (drek)")
    print("  3. Dinner (dark)")
    print("  4. Dessert (embelsire)")
    print("  5. Any (S'ka rendesi)")
    choice = input("Choose (1-5): ").strip()
    return {"1": "breakfast", "2": "lunch", "3": "dinner",
            "4": "dessert", "5": None}.get(choice, None)


def get_ingredients_input():
    print("\nCilet perberes keni ne shtepi? (What ingredients do you have?)")
    print("  Ndajini fjalet me presje (Enter comma-separated keywords) (p.sh (e.g).: mish, djath, veze)")
    raw = input("Ingredients: ").strip()
    #if we didn't input any preferences
    if not raw:
        return []
    #This is a list comprehension — a compact way to build a list. It takes the raw string
    # (e.g. "mish, djath, veze"), splits it by commas into ["mish", " djath", " veze"],
    # then for each item i it runs .strip() to remove spaces and .lower() to make it lowercase.
    # The if i.strip() at the end skips any empty entries in case the user typed a trailing comma
    return [i.strip().lower() for i in raw.split(",") if i.strip()]


def get_allergens_input():
    print("\nKeni alergji? (Do you have any allergens to avoid?)")
    print("  Opsionet (Options): gluten, dairy, eggs, nuts, meat, seafood")
    print("  Enter comma-separated, or press Enter to skip")
    raw = input("Allergens: ").strip()
    if not raw:
        return []
    return [a.strip().lower() for a in raw.split(",") if a.strip()]


def main():
    # Check that recipes.json exists
    if not os.path.exists("recipes.json"):
        print("recipes.json not found!")
        print("Please run 'python scraper.py' first to build the recipe database.")
        return

    recipes = load_recipes()
    print(f"\nLoaded {len(recipes)} Albanian recipes from recipes.json")

    #get inputs from user
    weather = get_weather_input()
    budget = get_budget_input()
    meal_type = get_meal_type_input()
    ingredients = get_ingredients_input()
    allergens = get_allergens_input()

    print("\nSearching for the best matches...")

    weights = get_weights_input()

    results = recommend(
    recipes,
    weather=weather,
    budget=budget,
    available_ingredients=ingredients,
    meal_type=meal_type,
    exclude_allergens=allergens,
    weights=weights,
)

    print_recommendations(results)


if __name__ == "__main__":
    main()
