'''
Author: Jaime Badiola Ramos
Email: Jaime.badiolaramos@gmail.com
Date: 2021-01-22
'''

import pandas as pd
import collections

def conn():
    import sqlalchemy
    import pyodbc
    import pandas as pd
    import urllib
    
    params = urllib.parse.quote_plus("Driver={ODBC Driver 17 for SQL Server};Server=tcp:reds10-db.database.windows.net,1433;Database=reds10_database;Uid=reds10Administratorrole;Pwd=kzuWgr2t2PYD;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    return engine


# Insert Dataframe into SQL Server:
def push_df_to_db(records_dict :dict, table, overwrite=True):
    engine = conn()
    if overwrite:
        delete_row_sql = f"delete from {table} where 1=1"
        engine.execute(delete_row_sql)
    for x in records_dict:
        query = f'''INSERT INTO {table} ({','.join(x.keys())}) values({str(list(x.values())).strip('[]')})'''.replace("'NULL'", "NULL")
        # print(query)
        engine.execute(query)


def query_db(query):
    engine = conn()
    df = pd.read_sql(query, engine)
    return df

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
