# Final-Project-MG
# Albanian Recipe Recommender 

## Overview

This project is a personalized recipe recommendation system focused on traditional Albanian cuisine. The program suggests dishes based on user preferences such as weather, budget, and available ingredients.

The goal of this project is to combine cultural relevance with algorithmic decision-making to generate useful and realistic meal recommendations.

---

## Features

* Recommends Albanian dishes based on:

  * Weather (e.g., cold or warm)
  * Budget (low, medium, high)
  * Available ingredients
* Returns the **top 3 best matching recipes**
* Uses a scoring algorithm to rank recipes
* Includes recipe ratings as part of the recommendation logic

---

## How It Works

Each recipe is stored with attributes such as:

* Name
* Price category
* Ideal weather
* Ingredients
* Rating

The program assigns a **score** to each recipe based on how well it matches the user's input:

* Weather match → +2 points
* Budget match → +2 points
* Ingredient matches → +1 point per match
* Rating → added directly to score

After scoring all recipes, the program:

1. Sorts them from highest to lowest score
2. Returns the top 3 recommendations

---

## Example

### Input:

* Weather: cold
* Budget: low
* Ingredients: cheese, spinach

### Output:

Recommended dishes might include:

* Byrek
* Tavë Kosi
* (other matches depending on dataset)

---

## Technologies Used

* Python (no external libraries required for current version)
* Basic data structures:

  * Lists
  * Dictionaries
* Algorithms:

  * Iteration
  * Conditional logic
  * Sorting

---

## Project Structure

* `main.py` – contains the recipe dataset and recommendation algorithm
* `README.md` – project documentation

---

## Future Improvements

* Web scraping to gather real Albanian recipes dynamically
* User rating system for recipes
* Saving/loading recipes using JSON
* Building a simple web interface for user interaction
* Integration with a weather API for real-time recommendations

---

## Motivation

This project is inspired by my interest in cooking and my cultural background. It aims to highlight Albanian cuisine while applying computer science concepts such as algorithms and data processing.

---

## Author

Moana Gorezi
