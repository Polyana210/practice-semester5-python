import csv
from elasticsearch import Elasticsearch
from constants import *
from operator import itemgetter
from creation_database import *
from complection_database import *
from creation_complection_elastic import *

def search_phrase(phrase):
    search_stat = dict()
    search_stat['Input_document'] = INPUT_FILE_NAME
    search_stat['Output_document'] = OUTPUT_FILE_NAME
    search_stat['Phrase'] = phrase
    # connect to Elasticsearch
    es = Elasticsearch(    
        [{'host': 'localhost', 'port': ELASTICSEARCH_PORT,  "scheme": "http"}],    
        http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
    )

    # search
    res= es.search(index=ELASTICSEARCH_INDEX_NAME,body={
            'query':{
                'match_phrase':{
                    "text": phrase
                }
            }
        })

    # Create connect with database
    connection = sqlite3.connect(DATABASE_NAME)
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
    search_stat["Count"] = len(sorted_result_list)
    search_stat["Result"] = sorted_result_list

    # write results into file
    with open(OUTPUT_FILE_NAME, 'w', encoding='utf8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['id', 'text', 'rubrics', 'created_date'])
        writer.writeheader()
        for data in sorted_result_list[:20]:
            writer.writerow(data)

    # write information about results into terminal
    print("Found", len(sorted_result_list), "results")
    return search_stat
    
if __name__ == '__main__':
    #phrase = input('Input phrase to search:')
    search_res = search_phrase("книга")
    print(search_res["Count"])
    #search_phrase(phrase)