import os


if os.getenv('gcp') is None:
    from dotenv import load_dotenv
    load_dotenv()


QUIZZES_COLLCTION_NAME = os.environ['QUIZZES_COLLCTION_NAME']
QUIZ_SETS_COLLCTION_NAME = os.environ['QUIZ_SETS_COLLCTION_NAME']
