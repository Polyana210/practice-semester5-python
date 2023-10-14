import csv
from operator import itemgetter
import json

def read_csv_file(file_name):
    with open(file_name, 'r', encoding='utf8') as file:
        csv_file = csv.DictReader(file)
        db_list = [] 
        for row in csv_file:
            db_list.append(dict(row))
    return db_list

def sort_data(db_list):
    db_list = sorted(db_list, key=itemgetter('created_date'), reverse=True)
    for i in range(0, len(db_list)):
        db_list[i]['id']=i+1
    return db_list

def create_json_file(db_info):
    for i in range(0, len(db_info)):
        db_info[i]['id']=i+1
    with open("database.json", "w", encoding='utf8') as fh:
        l =json.dump(db_info, fh, indent=3)



db_list = read_csv_file('posts.csv')
db_list = sort_data(db_list)
db_list = create_json_file(db_list)
    