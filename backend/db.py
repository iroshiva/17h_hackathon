import sys
import sqlite3
from sqlite3 import Error
import pandas as pd

def create_connection(db_file):
    """ Create a database connection to a SQLite database """
    
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()
    
    return conn

def create_table():
    """ Use a create_table function to write the entire database """

    connection = create_connection('shows.db')
    cursor = connection.cursor()
    queries = ( ''' CREATE TABLE IF NOT EXISTS profession(
                    id_profession VARCHAR(50),
                    name VARCHAR(50),
                    PRIMARY KEY(id_profession)
                    )''',

                ''' CREATE TABLE IF NOT EXISTS speciality(
                    id_speciality VARCHAR(50),
                    name VARCHAR(50),
                    PRIMARY KEY(id_speciality)
                    )''',

                ''' CREATE TABLE IF NOT EXISTS practitioner(
                    id_practitioner VARCHAR(50),
                    name VARCHAR(50) NOT NULL,
                    id_profession VARCHAR(50),
                    PRIMARY KEY(id_practitioner),
                    FOREIGN KEY(id_profession) REFERENCES profession(id_profession)
                    )''',

                ''' CREATE TABLE IF NOT EXISTS rating(
                    id_rating VARCHAR(50),
                    id_profession VARCHAR(50),
                    PRIMARY KEY(id_rating),
                    FOREIGN KEY(id_profession) REFERENCES profession(id_profession)
                    )''')

    # Use cursor.execute() method to write the CREATE TABLE query
    try:
        for query in queries:
            cursor.execute(query)
            connection.commit()

        print("Database and tables created successfully")
    except:
        print("Unexpected error:", sys.exc_info()[0])
    
def insert_values():
    """ Insert dataframe into database """

    connection = create_connection('shows.db')
    try:
        tables = ['profession', 'speciality', 'practitioner', 'rating_profession']
        for sheet_index, table in zip(range(4), tables):  
            pd.read_excel('data.xlsx', sheet_name=sheet_index).to_sql(table, connection, if_exists='replace', index=False)
        
        print("The data has been inserted successfully")
    except:
        print("Unexpected error:", sys.exc_info()[0])
    
def get_query(query):
    """ Create a dataframe based on a SQLite's table """

    connection = create_connection('shows.db')
    df = pd.read_sql(query, connection)
    
    return df

# Define our main tables in dataframe
df_profession = get_query('SELECT * FROM profession')
df_practitioner = get_query('SELECT * FROM practitioner')
df_speciality = get_query('SELECT * FROM speciality')
df_ref = get_query('SELECT * FROM rating_profession')

def get_filter_results(dict_of_values):
    """ Use a json response to filter the values of the dataframe """

    df_result = pd.DataFrame.from_dict(dict_of_values, orient='index', columns=['rating']).reset_index()
    df_result = df_result.join(df_speciality.set_index('name'), on='index')
    
    list_of_profession = []
    for value in list(df_result['id_speciality'].map(str) + df_result['rating'].map(str)):
        df = df_ref[df_ref['id_rating'] == value]['id_profession']
        for row in df:
            list_of_profession.append(row)

    list_of_profession = list(set(list_of_profession))
    
    return df_profession[df_profession['id_profession'].isin(list_of_profession)].to_dict('records'), \
        df_practitioner[df_practitioner['id_profession'].isin(list_of_profession)].to_dict('records')