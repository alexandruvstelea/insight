from flair.models import TextClassifier
from flair.data import Sentence
from dotenv import load_dotenv
from os import getenv
import psycopg2
from translate import Translator

translator = Translator(from_lang="ro", to_lang="en")
load_dotenv(".env")

USER = getenv("POSTGRES_USER")
PASSWORD = getenv("POSTGRES_PASSWORD")
HOST = getenv("POSTGRES_HOST")
DB_NAME = getenv("POSTGRES_DB_NAME")
PORT = getenv("PORT")

con = psycopg2.connect(
    dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
)
cur = con.cursor()

cur.execute('SELECT * FROM "Comments"')
comments_list = cur.fetchall()

classifier = TextClassifier.load("en-sentiment")
for comment in comments_list:
    text = comment[3]
    comment_id = comment[0]
    sentiment_value = comment[9]
    if text == "":
        continue
    translated_text = translator.translate(text)

    sentence = Sentence(translated_text)
    classifier.predict(sentence)
    score = sentence.labels[0].score * 100
    value = sentence.labels[0].value

    if value == "NEGATIVE":
        score = -score
    if sentiment_value == -1:
        update_query = (
            f'UPDATE "Comments" SET sentiment = {score} WHERE id = {comment_id}'
        )
        cur.execute(update_query)

    print(f"score = {score}")
    print(f"value = {value}")
con.commit()
cur.close()
con.close()
