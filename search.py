import csv
from elasticsearch import Elasticsearch

from operator import itemgetter
from creation_database import *
from complection_database import *
from creation_complection_elastic import *

# connect to Elasticsearch
es = Elasticsearch(    
    [{'host': 'localhost', 'port': constants.ELASTICSEARCH_PORT,  "scheme": "http"}],    
    http_auth=(constants.ELASTICSEARCH_USERNAME, constants.ELASTICSEARCH_PASSWORD)
)

# search
search_phrase = input("Input phrase to search: ")
res= es.search(index=constants.ELASTICSEARCH_INDEX_NAME,body={
        'query':{
            'match_phrase':{
                "text": search_phrase
            }
        }
    })

# Create connect with database
connection = sqlite3.connect(constants.DATABASE_NAME)
cursor = connection.cursor()

# getting information from database
result_list = []
for hit in res['hits']['hits']:
    cursor.execute('SELECT * FROM Documents WHERE id = {id}.'.format(id = hit['_id']))
    res_document = cursor.fetchone()
    result_list.append({'id':res_document[0], 'text':res_document[1], 'rubrics':res_document[2], 'created_date':res_document[3]})

connection.commit()
connection.close()

# sorting result
sorted_result_list = sorted(result_list, key=itemgetter('created_date'), reverse=True)

# write results into file
with open(constants.OUTPUT_FILE_NAME, 'w', encoding='utf8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['id', 'text', 'rubrics', 'created_date'])
    writer.writeheader()
    for data in sorted_result_list[:20]:
        writer.writerow(data)

# write information about results into terminal
print("Found", len(sorted_result_list), "results")
if len(sorted_result_list)>20:
    print('The newest 20 documents are written to a file:', constants.OUTPUT_FILE_NAME)
else:
    print("All documents are written to a file:", constants.OUTPUT_FILE_NAME)