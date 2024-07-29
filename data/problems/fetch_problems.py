import psycopg
import requests
import json

from queries.problem_queries import get_problem_list, get_num_problems_query


def insert_problem_data(cursor, connection,
                        problem_number: int,
                        problem_name: str,
                        difficulty: str,
                        topics: list[str],
                        acceptance: int) -> bool:
    try:
        query = ("INSERT INTO problem_info (problem_number, problem_name, difficulty, topics, acceptance) "
                 "VALUES (%s, %s, %s, %s, %s);")
        data = (problem_number, problem_name, difficulty, topics, acceptance)
        cursor.execute(query, data)
        connection.commit()
        return True
    except psycopg.DatabaseError as err:
        print(err)
        return False


def get_num_total_problems(url: str) -> int:
    query = get_num_problems_query()
    response = requests.get(url=url, json={"query": query})
    response = json.loads(response.content.decode('utf-8'))
    total_num_problems = int(response['data']['problemsetQuestionList']['total'])
    return total_num_problems


def insert_problems(url: str, cursor, connection, start: int, total_problems: int):
    page_length = 50
    diff = total_problems - start

    try:
        for i in range(start, total_problems, diff):
            page_query = get_problem_list('', i, diff)
            response = requests.get(url=url, json={"query": page_query})
            response = json.loads(response.content.decode('utf-8'))
            page_questions = response['data']['problemsetQuestionList']['questions']
            for question in page_questions:
                problem_number = int(question['frontendQuestionId'])
                problem_name = question['title']
                difficulty = question['difficulty']
                topic_tags = question['topicTags']
                acceptance = int(question['acRate'])
                topics = []
                for topic in topic_tags:
                    topics.append(topic['name'])
                inserted_successfully = insert_problem_data(cursor,
                                                            connection,
                                                            problem_number,
                                                            problem_name,
                                                            difficulty,
                                                            topics,
                                                            acceptance)
                if not inserted_successfully:
                    raise psycopg.Error('Insertion problem')

        return True
    except psycopg.Error as err:
        print(err)
        return False


def insert_all_problems(url: str, cursor, connection):
    total_num_problems = get_num_total_problems(url)
    page_length = 50

    for i in range(0, total_num_problems + 1, page_length):
        page_query = get_problem_list('', i, page_length)
        response = requests.get(url=url, json={"query": page_query})
        response = json.loads(response.content.decode('utf-8'))
        page_questions = response['data']['problemsetQuestionList']['questions']
        for question in page_questions:
            problem_number = int(question['frontendQuestionId'])
            print(problem_number)
            problem_name = question['title']
            difficulty = question['difficulty']

            topic_tags = question['topicTags']
            acceptance = int(question['acRate'])
            topics = []
            for topic in topic_tags:
                topics.append(topic['name'])
            insert_problem_data(cursor,
                                connection,
                                problem_number,
                                problem_name,
                                difficulty,
                                topics,
                                acceptance)


def get_total_problems_metadata(cursor):
    query = (
        "SELECT * FROM problem_metadata;"
    )

    cursor.execute(query)
    return cursor.fetchone()[0]


def set_total_problems_metadata(cursor, connection, old_total, new_total):
    query = (
        "UPDATE problem_metadata SET TOTAL = %s WHERE TOTAL = %s"
    )

    data = (new_total, old_total)
    cursor.execute(query, data)
    connection.commit()


def insert_added_problems_batch(url: str, connection_string: str):
    print("Inserts problems added to leetcode everyday at a set time")
    # get the total number of problems we have already inserted from the problem_metadata table
    conn = psycopg.connect(connection_string)
    cur = conn.cursor()
    total_problems_saved = get_total_problems_metadata(cur)
    # get the total number of problems leetcode has published
    total_problems_published = get_num_total_problems(url)
    # compare and check if they match
    # if they don't, fetch the additional problems using the graphql api
    if total_problems_saved != total_problems_published:
        # and insert them into the problem_info table
        insertion_success = insert_problems(url, cur, conn, total_problems_saved, total_problems_published)
        if insertion_success:
            print("Successfully inserted")
            # if insertion is successful update the problem =_metadata table
            set_total_problems_metadata(cur, conn, total_problems_saved, total_problems_published)
        else:
            print("An error has occurred during insertion")
    else:
        print("Database already up to date with leetcode")
    # update the total problems if inserted successfully
