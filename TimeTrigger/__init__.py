import datetime
import logging
from client import Client, Client_two_legged
from  core import update_project_list, update_project_issues, update_users, update_companies
import azure.functions as func

logger = logging.getLogger('name')
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
logger.addHandler(sh)

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    client = Client

    # logging.info('Python ti
    # mer trigger function ran at %s', utc_timestamp)

    logging.info('Updating bim projects')

    client.get_projects()
    update_project_list(client)

    logging.info('Updating bim issues')
    update_project_issues(client)
    
    # utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    # logging.info('Python timer trigger function finished at %s', utc_timestamp)

    logging.info('Updating bim users')
    client_users = Client_two_legged
    update_users(client_users)

    logging.info('Updating bim companies')
    update_companies(client_users)