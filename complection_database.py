import sqlite3
import csv
from constants import *

def read_csv_file(file_name):
    with open(file_name, 'r', encoding='utf8') as file:
        csv_file = csv.DictReader(file)
        data_list = [] 
        for row in csv_file:
            data_list.append(dict(row))
    return data_list


connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

for i in read_csv_file(INPUT_FILE_NAME):
    cursor.execute('INSERT INTO Documents (text, rubrics, created_date) VALUES (?, ?, ?)', (i['text'], i['rubrics'], i['created_date']))

connection.commit()
connection.close()