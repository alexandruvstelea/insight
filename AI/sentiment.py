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
    translated_text = translator.translate(text)
    sentence = Sentence(translated_text)
    classifier.predict(sentence)
    score = sentence.labels[0].score
    value = sentence.labels[0].value

    print(f"score = {score}")
    print(f"value = {value}")
