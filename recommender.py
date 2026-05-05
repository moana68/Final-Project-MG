###recommender.py

import json
from history import load_history, apply_history_penalty

#default argument recipes.json
def load_recipes(path="recipes.json"):
    #Load the scraped recipe dataset.
    with open(path, "r", encoding="utf-8") as f:
        #takes json and converts it to a list of dictionaries
        return json.load(f)

# main recommend algorithm. takes as inputs the following
def recommend(recipes, weather, budget, available_ingredients,
              meal_type=None, exclude_allergens=None, weights=None):

    # Default weights if none provided
    if weights is None:
        weights = {
            "weather":     2,
            "budget":      2,
            "ingredients": 1,
            "meal_type":   2,
        }

    if exclude_allergens is None:
        exclude_allergens = []

    scored = []

    for recipe in recipes:

        if any(allergen in recipe.get("allergens", [])
               for allergen in exclude_allergens):
            continue

        score = 0

        recipe_weather = recipe.get("weather", "any")
        if recipe_weather == weather:
            score += weights["weather"]
        elif recipe_weather == "any":
            score += weights["weather"] * 0.5  #half credit for flexible recipes

        if recipe.get("price") == budget:
            score += weights["budget"]

        recipe_ingredients_text = " ".join(recipe.get("ingredients", [])).lower()
        for ing in available_ingredients:
            if ing.lower() in recipe_ingredients_text:
                score += weights["ingredients"]

        if meal_type and meal_type in recipe.get("meal_type", []):
            score += weights["meal_type"]

        score += recipe.get("rating", 0)

        scored.append({**recipe, "score": round(score, 2)})

        history = load_history()
        scored = apply_history_penalty(scored, history)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:3]

def print_recommendations(results, weather=None, budget=None,
                           available_ingredients=None, meal_type=None):
    if not results:
        print("Nuk u gjet asnjë recetë që përputhet. / No matching recipes found.")
        return

    print("\n🍽  Recetat e rekomanduara / Recommended dishes:\n")
    for i, recipe in enumerate(results, 1):
        print(f"  {i}. {recipe['name']}")
        print(f"     Score: {recipe['score']}")

        # Build a list of reasons this recipe was recommended
        reasons = []
        if weather and recipe.get("weather") == weather:
            reasons.append(f"✓ Weather match ({weather})")
        if budget and recipe.get("price") == budget:
            reasons.append(f"✓ Budget match ({budget})")
        if meal_type and meal_type in recipe.get("meal_type", []):
            reasons.append(f"✓ Meal type match ({meal_type})")
        if available_ingredients:
            recipe_text = " ".join(recipe.get("ingredients", [])).lower()
            matched = [ing for ing in available_ingredients if ing.lower() in recipe_text]
            if matched:
                reasons.append(f"✓ Ingredients matched: {', '.join(matched)}")

        if reasons:
            print(f"     Why: {' | '.join(reasons)}")

        print(f"     Allergens: {', '.join(recipe['allergens']) or 'none'}")
        print(f"     URL: {recipe['url']}")
        print()
