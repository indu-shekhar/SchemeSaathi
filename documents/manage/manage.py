import csv
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('../../app.db')
cur = conn.cursor()

# Create the schemes table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS schemes (
    id INTEGER PRIMARY KEY,
    scheme_name TEXT,
    nodal_ministry TEXT,
    implementing_agency TEXT,
    target_beneficiaries TEXT,
    tags TEXT,
    state TEXT,
    category TEXT,
    level TEXT,
    brief_description TEXT,
    detailed_description TEXT,
    eligibility_criteria TEXT,
    documents_required TEXT,
    application_process TEXT,
    benefits TEXT,
    official_website TEXT,
    application_form TEXT,
    order_notice TEXT,
    slug TEXT
);
''')

# Open the CSV file and read its contents
with open('/workspaces/SchemeSaathi/documents/schemeswslug.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute('''
        INSERT INTO schemes (
            id, scheme_name, nodal_ministry, implementing_agency, target_beneficiaries, tags, state, category, level, brief_description, detailed_description, eligibility_criteria, documents_required, application_process, benefits, official_website, application_form, order_notice, slug
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['id'],
            row['scheme_name'],
            row['nodal_ministry'],
            row['implementing_agency'],
            row['target_beneficiaries'],
            row['tags'],
            row['state'],
            row['category'],
            row['level'],
            row['brief_description'],
            row['detailed_description'],
            row['eligibility_criteria'],
            row['documents_required'],
            row['application_process'],
            row['benefits'],
            row['Official Website'],
            row['Application Form'],
            row['Order/Notice'],
            row['slug']
        ))

# Commit the transaction and close the connection
conn.commit()
conn.close()