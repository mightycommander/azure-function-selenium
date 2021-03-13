'''
Author: Jaime Badiola Ramos
Email: Jaime.badiolaramos@gmail.com
Date: 2021-01-22
'''

from .client import Client
import pandas as pd
from .db_utils import push_df_to_db, query_db, flatten
from .forge import ForgeApp
import re
import logging

logger = logging.getLogger('name')
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
logger.addHandler(sh)

last_record_query = 'select project, max(DateSync) last_record, getdate()+1 new_limit_date from data_imports.{} group by project'

def smart_function(df):
    for k,v in df.dtypes.to_dict().items():
        x = 'INT' if str(v)=='int64' else 'DATETIME2' if 'date' in k.lower() else 'VARCHAR(400)'
        print(f'{k} {x},')


def update_project_list(client):
    table = 'bim_projects'
    df = pd.DataFrame()

    for project in client.projects:
        df = df.append(flatten(project.data['docs']), ignore_index=True)
    
    logger.info(df.head())
    logger.info(df.columns)

    df['attributes_scopes'] = df['attributes_scopes'].apply(lambda x: x[0])
    df = df.fillna('NULL').replace(False, 'FALSE').replace(True, 'TRUE')
    push_df_to_db(df.to_dict('records'), table=f'reds10_database.data_imports.{table}', overwrite=True)

    return None

def update_project_issues(client):
    table = 'bim_issues'
    df2 = pd.DataFrame()
    for i in client.projects:
        issue_list = client.get_issues(i.data['docs']['relationships']['issues']['data']['id'])
        for issue in issue_list['data']:
            df2 = df2.append(flatten(issue), ignore_index=True)

    df2['container_id'] = df2['links_self'].apply(lambda x: re.search('containers/([0-9a-z].*?)/',x).group(1))
    df2 = df2[[x for x in df2.columns if (x[:10] == 'attributes' and x[:18] != 'attributes_pushpin') or x == 'container_id']]
    
    df2.columns = [[x.replace('attributes_','') for x in df2.columns]]
    
    df2.columns = df2.columns.get_level_values(0)
    df2 = df2[[x for x in df2.columns if x not in ['permitted_actions', 'permitted_attributes', 'permitted_statuses', 'custom_attributes', 'sheet_metadata_is3D']]]
    print(df2.container_id.unique())
    df2['description'] = df2['description'].str.replace("'", '')
    df2['answer'] = df2['answer'].str.replace("'", '')
    df2['title'] = df2['title'].str.replace("'", '')
    #for col in ['answered_at', 'closed_at', 'created_at', 'due_date', 'opened_at', 'synced_at', 'updated_at']:
    #    df2.loc[:,col] = pd.to_datetime(df2.loc[:,col])
    df2 = df2.fillna('NULL')
    push_df_to_db(df2.to_dict('records'), table=f'reds10_database.data_imports.{table}', overwrite=True)

    return None

def update_users(client):
    table = 'bim_users'
    client.get_users()
    df_users = pd.DataFrame()
    for i in client.users:
        df_users = df_users.append(i, ignore_index=True)
    df_users = df_users.fillna('NULL')
    for col in ['last_name', 'name', 'nickname', 'email']:
        df_users[col] = df_users[col].str.replace("'", "")

    push_df_to_db(df_users.to_dict('records'), table=f'reds10_database.data_imports.{table}', overwrite=True)

    return None

def update_companies(client):
    table = 'bim_companies'
    client.get_companies()
    df_companies = pd.DataFrame()
    for i in client.companies:
        df_companies = df_companies.append(i, ignore_index=True)
    df_companies = df_companies.fillna('NULL')
    for col in ['name']:
        df_companies[col] = df_companies[col].str.replace("'", "")

    push_df_to_db(df_companies.to_dict('records'), table=f'reds10_database.data_imports.{table}', overwrite=True)

    return None

