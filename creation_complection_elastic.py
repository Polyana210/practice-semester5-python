from elasticsearch import Elasticsearch
import sqlite3
import constants

# connect to Elasticsearch
es = Elasticsearch(    
    [{'host': 'localhost', 'port': constants.ELASTICSEARCH_PORT,  "scheme": "http"}],    
    http_auth=(constants.ELASTICSEARCH_USERNAME, constants.ELASTICSEARCH_PASSWORD)
)

if es.indices.exists(index=constants.ELASTICSEARCH_INDEX_NAME):
    es.options(ignore_status=[400,404]).indices.delete(index=constants.ELASTICSEARCH_INDEX_NAME)
es.indices.create(index=constants.ELASTICSEARCH_INDEX_NAME)

# Create connect with database
connection = sqlite3.connect(constants.DATABASE_NAME)
cursor = connection.cursor()

# Get data from database
cursor.execute('SELECT * FROM Documents')
data_list= cursor.fetchall()

# complection Elasticsearch
for doc in data_list:
    es.index(
        index=constants.ELASTICSEARCH_INDEX_NAME,
        id=doc[0],
        document={
            "text": doc[1],
        }
    )
connection.close()