import sqlite3
from constants import *

# Create connect with database
connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

# Drop table Documents
cursor.executescript('drop table if exists Documents;')

# Create table Documents
cursor.execute('''
CREATE TABLE Documents (
id INTEGER PRIMARY KEY,
text TEXT NOT NULL,
rubrics TEXT NOT NULL,
created_date TEXT NOT NULL
)
''')

# Save changes
connection.commit()
connection.close()