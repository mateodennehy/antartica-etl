import requests
from os.path import join
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file("dashboard-service-account-key.json")
bigquery_client = bigquery.Client(credentials=credentials)



def excecute_query(query):

    try:
        query_job = bigquery_client.query(query)
        return query_job.result()
    except Exception as e:
        print("Error")
        print(e)

    return False


def insert_data(dataset_id, table_id, rows_to_insert):
    dataset_ref = bigquery_client.dataset(dataset_id)

    table_ref = dataset_ref.table(table_id)
    table = bigquery_client.get_table(table_ref)  # API call

    errors = bigquery_client.insert_rows(table, rows_to_insert)  # API request
    assert errors == []



def get_miner_data(miner_address):
    miner_address = miner_address[2:] if "0x" ==  miner_address[:2] else miner_address
    URL = f"https://hiveon.net/api/v1/stats/miner/{miner_address}/ETH/billing-acc"
    r = requests.get(url = URL)
    data = r.json()
    return data



if __name__ == '__main__':
    project_id = "adept-insight-335504"
    dataset_id = "dashboard_antartica"
    wallet_address = "fc8f035129c537fc19e504613b841fd12aa035e7"

    data = get_miner_data(miner_address=wallet_address)
    
    # ===== Rewards =======
    query = f"SELECT * FROM {project_id}.{dataset_id}.rewards WHERE rigg_id = 1;"
    bq_data = excecute_query(query)
    in_db = []
    for row in bq_data:
        in_db.append(row[1].replace(tzinfo=None).timestamp())

    rows_to_insert = []
    for reward in data['earningStats']:
        end = datetime.strptime(reward['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        start = end - timedelta(hours=1)
        if end.timestamp() not in in_db:
            rows_to_insert.append((start, end, "ETH", reward["reward"], 1))

    if rows_to_insert:
        insert_data(dataset_id, "rewards", rows_to_insert)

    # ===== Payments =======
    query = f"SELECT * FROM {project_id}.{dataset_id}.rewards WHERE rigg_id = 1;"
    bq_data = excecute_query(query)
    in_db = []
    for row in bq_data:
        in_db.append(row[1].replace(tzinfo=None).timestamp())

    rows_to_insert = []
    for reward in data['earningStats']:
        end = datetime.strptime(reward['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        start = end - timedelta(hours=1)
        if end.timestamp() not in in_db:
            rows_to_insert.append((start, end, "ETH", reward["reward"], 1))

    if rows_to_insert:
        insert_data(dataset_id, "rewards", rows_to_insert)
