###history.py

import json
import os

history_file = "history.json"

#Load previously cooked recipe URLs from history.json
def load_history():
    if not os.path.exists(history_file):
        return []
    with open(history_file, "r", encoding="utf-8") as f:
        return json.load(f)

#Add a cooked recipe to history.json
def save_to_history(recipe):
    history = load_history()
    # Avoid duplicates
    if recipe["url"] not in [r["url"] for r in history]:
        history.append({"name": recipe["name"], "url": recipe["url"]})
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

#Subtract 1.5 points from recipes the user has already cooked.
def apply_history_penalty(scored_recipes, history):
    cooked_urls = {r["url"] for r in history}
    for recipe in scored_recipes:
        if recipe["url"] in cooked_urls:
            recipe["score"] = round(recipe["score"] - 1.5, 2)
    return scored_recipes
