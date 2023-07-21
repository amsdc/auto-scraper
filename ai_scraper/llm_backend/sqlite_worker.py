import json
import sqlite3

def add_data(table_name,insert_data,Json_array):
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    x_text = ", ".join([f"{i[0]} {i[1]}" for i in x_array])
    insert_data = x_text
    cursor.execute(f'Create Table if not exists {table_name} ({insert_data})')
    columns = list(Json_array[0].keys())
    values_list = ", ".join(['?']*len(columns))
    for row in Json_array:
        keys= tuple(row[c] for c in columns)
        cursor.execute(f'insert into {table_name} values({values_list})',keys)
        
    connection.commit()
    connection.close()
    

def query_data(query):
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute(query)
    print(cursor.fetchall())
    connection.close()

