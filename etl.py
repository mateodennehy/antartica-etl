import requests
import json
from os.path import join
from datetime import datetime


def get_miner_data(miner_address):
    miner_address = miner_address[2:] if "0x" ==  miner_address[:2] else miner_address
    URL = f"https://hiveon.net/api/v1/stats/miner/{miner_address}/ETH/billing-acc"
    r = requests.get(url = URL)
    data = r.json()
    return data



if __name__ == '__main__':
    now = datetime.now()
    data = get_miner_data(miner_address="fc8f035129c537fc19e504613b841fd12aa035e7")
    folder = "/home/matedennehy/Antartica/antartica-etl"
    name = f"{now.year}-{now.month}-{now.day}_{now.hour}:{now.minute}_api_data.json"
    with open(join(folder, name), 'w') as f:
        json.dump(data, f, indent = 2)