import random

from data.emojis.emoji_adder import add_emoji_to_problem, get_row, add_emojis_to_problems
from data.emojis.emoji_fetcher import get_emojis_for_insertion

CONNECTION_STRING = "dbname=problems user=probleminfouser password=password"
URL = 'https://leetcode.com/graphql'


if __name__ == "__main__":
    # emojis = get_emojis_for_insertion()
    # print(emojis)
    # inserted = add_emoji_to_problem(CONNECTION_STRING, 72, emojis)
    # if inserted:
    #     print("inserted emoji successfully")

    row = get_row(1230, CONNECTION_STRING)
    print(row)
    # insertion_successful = add_emojis_to_problems(CONNECTION_STRING, emojis)
    # if insertion_successful:
    #     print("Insertion successful")




