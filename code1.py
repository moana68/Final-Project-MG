recipes = [
    {
        "name": "Byrek",
        "price": "low",
        "weather": "cold",
        "ingredients": ["cheese", "spinach"],
        "rating": 4.5
    },
    {
        "name": "Tave Kosi",
        "price": "medium",
        "weather": "cold",
        "ingredients": ["lamb", "yogurt"],
        "rating": 4.8
    }
]

def recommend_dishes(recipes, weather, budget, available_ingredients):
    scored_recipes = []

    for r in recipes:
        score = 0

        # Weather match
        if r["weather"] == weather:
            score += 2

        # Budget match
        if r["price"] == budget:
            score += 2

        # Ingredient match
        for ing in r["ingredients"]:
            if ing in available_ingredients:
                score += 1

        # Rating influence
        score += r["rating"]

        scored_recipes.append((score, r))

    # Sort by score (highest first)
    scored_recipes.sort(reverse=True, key=lambda x: x[0])

    # Return top 3 recipes
    top_recipes = [r[1] for r in scored_recipes[:3]]

    return top_recipes

results = recommend_dishes(
    recipes,
    weather="cold",
    budget="low",
    available_ingredients=["cheese", "spinach"]
)

for r in results:
    print(r["name"])
