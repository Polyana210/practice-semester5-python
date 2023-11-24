from constants import *
import sqlite3
from elasticsearch import Elasticsearch

# Create connect with database
connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

# connect to Elasticsearch
es = Elasticsearch(    
    [{'host': 'localhost', 'port': ELASTICSEARCH_PORT,  "scheme": "http"}],    
    http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
)

delete_id = int(input("Input id to delete: "))
try:
    k = es.get(index=ELASTICSEARCH_INDEX_NAME, id=delete_id)
    print('The document that we are deleting: ')
    print(k['_source']['text'])

    # delete from database
    cursor.execute( 'DELETE FROM Documents WHERE id = {id}.'.format(id = delete_id))
    # delete from elasticsearch index
    es.delete(index=ELASTICSEARCH_INDEX_NAME, id=delete_id)

    connection.commit()
    connection.close()
    print('The document was deleted successfully')
except:
    print('ERROR')
