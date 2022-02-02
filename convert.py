import csv
import sqlite3
import pandas as pd

connection = sqlite3.connect('pairs.db')
c = connection.cursor()
c.execute('''CREATE TABLE general (id text, date date, clue text, answer text, weekday text)''')

clues = pd.read_csv('clues.csv')

clues.to_sql('general', connection, if_exists='append', index=False)