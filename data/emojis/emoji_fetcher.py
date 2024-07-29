import requests

EMOJI_API_KEY = "access_key=a5aaa3cff23b64ad4af47b576eeba8112be5ee10"
EMOJI_LIST_ALL_EMOJIS_URL = "https://emoji-api.com/emojis"
EMOJI_LIST_CATEGORIES_URL = "https://emoji-api.com/categories"
EMOJI_LIST_EMOJIS_IN_CATEGORY_BASE_URL = "https://emoji-api.com/categories/"
FOOD_DRINK_CATEGORY = "food-drink"
TRAVEL_PLACES_CATEGORY = "travel-places"
ANIMALS_NATURE_CATEGORY = "animals-nature"


def make_call_to_emoji_api():
    print("Gets emojis from api")
    modified_url = EMOJI_LIST_ALL_EMOJIS_URL + "?" + EMOJI_API_KEY
    response = requests.get(modified_url)
    response = response.json()
    print(response)


def get_emojis_for_insertion() -> list[str]:
    emoji_categories = [FOOD_DRINK_CATEGORY, TRAVEL_PLACES_CATEGORY, ANIMALS_NATURE_CATEGORY]
    emojis = get_emojis_from_categories(emoji_categories)
    return emojis


def get_emoji_categories() -> list[str]:
    print("Gets emoji categories")
    categories = []
    modified_url = EMOJI_LIST_CATEGORIES_URL + "?" + EMOJI_API_KEY
    response = requests.get(modified_url)
    response = response.json()
    for category in response:
        categories.append(category['slug'])
    return categories


def get_emojis_in_category(category: str):
    print("gets emojis in category " + category)
    modified_url = EMOJI_LIST_EMOJIS_IN_CATEGORY_BASE_URL + category + "?" + EMOJI_API_KEY
    response = requests.get(modified_url)
    response = response.json()
    emojis = []
    for emoji in response:
        emojis.append(emoji['character'])
    return emojis


def get_emojis_from_categories(categories: list[str]) -> list[str]:
    emojis = []
    for category in categories:
        modified_url = EMOJI_LIST_EMOJIS_IN_CATEGORY_BASE_URL + category + "?" + EMOJI_API_KEY
        response = requests.get(modified_url)
        response = response.json()
        for emoji in response:
            emojis.append(emoji['character'])
    return emojis
