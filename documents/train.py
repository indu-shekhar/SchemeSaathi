import sqlite3

# Connect to the database
conn = sqlite3.connect('../app.db')
cursor = conn.cursor()

# Read the document names from the file
with open('document.txt', 'r') as file:
    document_names = eval(file.read())

# Insert each document name into the document table
for document_name in document_names:
    cursor.execute("INSERT INTO document (document_name) VALUES (?)", (document_name,))

# Commit the transaction and close the connection
conn.commit()
conn.close()