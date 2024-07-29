import random
import psycopg as pq

from data.problems.fetch_problems import get_total_problems_metadata


def add_emoji_to_problem(connection_string: str, problem_number, emojis) -> bool:
    rand_int = random.randint(0, len(emojis) - 1)
    try:
        with pq.connect(connection_string) as conn:
            with conn.cursor() as cur:
                query = ("UPDATE problem_info SET emoji = %s WHERE problem_number = %s")
                data = (emojis[rand_int], problem_number)
                cur.execute(query, data)
            conn.commit()
            return True
    except pq.DatabaseError as err:
        print(err)
        return False


def add_emojis_to_problems(connection_string: str, emojis: list) -> bool:
    n = len(emojis) - 1
    try:
        with pq.connect(connection_string) as conn:
            with conn.cursor() as cur:
                total_problems = get_total_problems_metadata(cur)
                for problem_number in range(1, total_problems + 1):
                    if problem_number % 50 == 0:
                        print("Inserting problem number " + str(problem_number))
                    rand_int = random.randint(0, n)
                    query = ("UPDATE problem_info SET emoji = %s WHERE problem_number = %s")
                    data = (emojis[rand_int], problem_number)
                    cur.execute(query, data)
            conn.commit()
        return True
    except pq.DatabaseError as err:
        print(err)
        return False


def get_row(problem_number: int, connection_string: str):
    try:
        with pq.connect(connection_string) as con:
            with con.cursor() as cur:
                query = ("SELECT * FROM problem_info WHERE problem_number = %s;")
                data = (problem_number,)
                cur.execute(query, data)
                return cur.fetchone()
    except pq.DatabaseError as err:
        print(err)
