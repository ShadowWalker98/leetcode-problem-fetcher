from data.fetch_problems import insert_added_problems_batch

CONNECTION_STRING = "dbname=problems user=probleminfouser password=password"
URL = 'https://leetcode.com/graphql'
import psycopg

if __name__ == "__main__":
    # fetch_all_problems(URL)
    # questions = problems['data']['problemsetQuestionList']['questions']
    print("Insertion into postgres")
    # conn = psycopg.connect(CONNECTION_STRING)
    # cur = conn.cursor()
    insert_added_problems_batch(URL, CONNECTION_STRING)
    # insert_all_problems(url=URL, cursor=cur, connection=conn)



