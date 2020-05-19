import os
import psycopg2
import csv
from settings import DB_URL

con = psycopg2.connect(dsn=DB_URL)
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS countries CASCADE")

cur.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id serial PRIMARY KEY, 
        name varchar UNIQUE,
        population integer,
        area integer,
        density integer 
    );'''
)
con.commit()


data = []
rows_count = 0
with open('static/countries.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in spamreader:
        if rows_count > 0:
            data.extend(row)
        rows_count += 1

pls = ["(%s, %s, %s, %s, %s)"] * (rows_count - 1)
query = f'''INSERT INTO countries (id, name, population, area, density) 
        VALUES {", ".join(pls)}
        ON CONFLICT (name) DO NOTHING
'''
cur.execute(query, data)
con.commit()

############# create ships table ####################

cur.execute("DROP TABLE IF EXISTS ships")
con.commit()
cur.execute('''
    CREATE TABLE IF NOT EXISTS ships (
        id serial PRIMARY KEY,
        country_id integer REFERENCES countries(id) NOT NULL,
        name varchar UNIQUE NOT NULL,
        ship_description varchar DEFAULT '--',
        built_year integer NOT NULL,
        length integer DEFAULT 134,
        width integer DEFAULT 100,
        gt integer DEFAULT 300,
        dwt integer DEFAULT 700
    );'''
)

con.commit()
insert_ship = '''
INSERT INTO ships (name, country_id, ship_description, built_year) 
VALUES (%s, (SELECT id from countries WHERE name=%s), %s, %s);
'''

for i in range(5):
    print(i)
    cur.execute(
        insert_ship, (f'ship #{i}', 'Germany', f'cool ship!', 1990+i))
    con.commit()

cur.execute('''
    SELECT ships.*, countries.name 
    FROM ships inner join countries on ships.country_id = countries.id
    WHERE ships.name LIKE %(pattern)s
    LIMIT 1000''',
    {'pattern': '%' + '9' + '%'}
)

for v in cur:
    print('row: ', v)
cur.close()
con.close()
