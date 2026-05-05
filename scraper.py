###scraper.py

import requests
from bs4 import BeautifulSoup
import json
import time

base_URL = "https://agroweb.org"
tag_URL = "https://agroweb.org/tag/gatime-tradicionale/"


# For any type of broad allergy term, what ingredients should be avoided
allergen_keywords = {
    "gluten":   ["miell", "petë", "bukë", "grurë", "elb"],
    "dairy":    ["qumësht", "djathë", "gjalpë", "kos", "krem"],
    "eggs":     ["vezë", "vezët"],
    "nuts":     ["arra", "bajame", "lajthi", "kikirikë"],
    "meat":     ["mish", "viçi", "derri", "qengji", "pulë"],
    "seafood":  ["peshk", "kallamar", "karkalec"],
}

# weather and what types of dishes fit it (stereotypically)
weather_keywords = {
    "cold": ["supë", "çorb", "tavë", "qeshqek", "japrak", "grurë", "fasule",
             "qull", "pelte", "patate"],
    "warm": ["sallatë", "perime", "domate", "trangull", "fli", "byrek",
             "fergese", "suxhuk"],
    "any":  [],
}

# correlates the words in the title with the likely meal
meal_type_keywords = {
    "breakfast": ["byrek", "bukë", "kulaç", "petë", "qumështor", "ëmbëlsirë",
                  "kek", "ballokume"],
    "lunch":     ["tavë", "supë", "çorb", "japrak", "qeshqek", "fasule",
                  "mish", "pilaf"],
    "dinner":    ["tavë", "mish", "qofte", "suxhuk", "patate", "japrak"],
    "dessert":   ["ëmbëlsirë", "kek", "ballokume", "trilece", "kadaif",
                  "bakllavë", "sheqer", "mjaltë"],
}

def estimate_price(ingredients):
    """
    Estimate recipe cost tier based on ingredient count and expensive keywords.
    More ingredients generally means more expensive. Certain ingredients
    (meat, seafood) push a recipe into a higher price tier.
    """
    expensive_keywords = ["mish viçi", "mish qengji", "peshk", "karkalec",
                          "kallamar", "proshutë", "salcice"]
    cheap_keywords = ["fasule", "patate", "vezë", "miell", "bukë", "lakër"]

    combined = " ".join(ingredients).lower()

    # Hard rules first
    if any(kw in combined for kw in expensive_keywords):
        return "high"
    if any(kw in combined for kw in cheap_keywords) and len(ingredients) <= 6:
        return "low"

    # Fall back to ingredient count
    if len(ingredients) <= 5:
        return "low"
    elif len(ingredients) <= 9:
        return "medium"
    else:
        return "high"

def get_article_links(url):
    #Collect all recipe article URLs from a page, following pagination.
    links = []
    page_url = url

    while page_url:
        print(f"  Fetching listing page: {page_url}")
        resp = requests.get(page_url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Each article card has an <h3> with an <a> inside
        for h3 in soup.select("h3 a[href]"):
            href = h3["href"]
            if href not in links:
                links.append(href)

        # Look for a next page link
        next_link = soup.select_one("a.next.page-numbers")
        page_url = next_link["href"] if next_link else None

        time.sleep(0.5)

    return links

#Scrape a single recipe page and return a structured dict
def scrape_recipe(url):
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.select_one("h1")
    title = title_tag.get_text(strip=True) if title_tag else "E panjohur"

    # Since the site uses bold headers like "Përbërësit" above <ul> lists.
    # We collect all <li> items that come after any ingredients heading.
    ingredients = []

    # Find all bold/strong tags that signal ingredient sections
    ingredient_headers = soup.find_all(
        lambda tag: tag.name in ["h4", "strong", "b"]
        and any(kw in tag.get_text() for kw in
                ["Përbërës", "mbushjen", "salcën", "brumit", "Për"])
    )

    for header in ingredient_headers:
        # Walk siblings until we hit the next heading or run out
        sibling = header.find_next_sibling()
        while sibling:
            if sibling.name in ["h4", "h3", "h2"]:
                break
            if sibling.name == "ul":
                for li in sibling.find_all("li"):
                    text = li.get_text(strip=True)
                    if text:
                        ingredients.append(text)
            sibling = sibling.find_next_sibling()

    # As fallback we grab ALL <li> from the article if nothing found above
    if not ingredients:
        article = soup.select_one("article") or soup.select_one(".entry-content")
        if article:
            for li in article.find_all("li"):
                text = li.get_text(strip=True)
                if text and len(text) < 120:  # skip nav items
                    ingredients.append(text)

    # Auto-tag fields from title + ingredients
    combined_text = (title + " " + " ".join(ingredients)).lower()

    allergens = [
        allergen for allergen, keywords in allergen_keywords.items()
        if any(kw in combined_text for kw in keywords)
    ]

    weather = "any"
    for condition, keywords in weather_keywords.items():
        if condition == "any":
            continue
        if any(kw in combined_text for kw in keywords):
            weather = condition
            break

    meal_type = []
    for mtype, keywords in meal_type_keywords.items():
        if any(kw in combined_text for kw in keywords):
            meal_type.append(mtype)
    if not meal_type:
        meal_type = ["lunch", "dinner"]  # default

    return {
        "name": title,
        "url": url,
        "ingredients": ingredients,
        "allergens": allergens,
        "weather": weather,
        "meal_type": meal_type,
        "price": estimate_price(ingredients),
        "rating": 4.0,         # default
    }


def main():
    print("Step 1: Collecting recipe links...")
    links = get_article_links(tag_URL)
    print(f"  Found {len(links)} recipe links.\n")

    recipes = []
    for i, url in enumerate(links, 1):
        print(f"Step 2: Scraping recipe {i}/{len(links)}: {url}")
        try:
            recipe = scrape_recipe(url)
            if recipe["ingredients"]:  # skip pages with no ingredient data
                recipes.append(recipe)
                print(f"  → '{recipe['name']}' | {len(recipe['ingredients'])} ingredients "
                      f"| weather: {recipe['weather']} | allergens: {recipe['allergens']}")
            else:
                print(f"  → Skipped (no ingredients found)")
        except Exception as e:
            print(f"  → Error: {e}")
        time.sleep(0.8)  # delay between requests

    # Save to JSON
    output_path = "recipes.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)

    print(f"\nDone! {len(recipes)} recipes saved to {output_path}")


if __name__ == "__main__":
    main()
