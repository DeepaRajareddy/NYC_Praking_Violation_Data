import argparse
import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from sodapy import Socrata
from math import ceil
from datetime import datetime


parser = argparse.ArgumentParser(description='Process data from NYC OPCV.')
parser.add_argument('--page_size', type=int,
                    help='how many rows to get per page', required=True)
parser.add_argument('--num_pages',
                    type=int, help='how many pages to get in total')
args = parser.parse_args(sys.argv[1:])


DATASET_ID = os.environ["DATASET_ID"]
APP_TOKEN = os.environ["APP_TOKEN"]
ES_HOST = os.environ["ES_HOST"]
ES_USERNAME = os.environ["ES_USERNAME"]
ES_PASSWORD = os.environ["ES_PASSWORD"]

#Connecting to Elasticsearch
#resp = requests.get(ES_HOST, auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD))
#print(resp.json())

if __name__ == '__main__':
    
   # create elasticsearch index
    try:
        
        resp = requests.put(
            # this is the URL to create nyc_parking "index"
            # which is our elasticsearch database/table
            f"{ES_HOST}/nyc_parking",
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
            # these are the "columns" of this database/table
            json={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                 },
                "mappings": {
                    "properties": {
                        "plate": {"type": "keyword"},
                        "state": {"type": "keyword"},
                        "license_type": {"type": "keyword"},
                        "summons_number": {"type": "float"},
                        "issue_date": {"type": "date", "format": "yyyy-MM-dd"},
                        "violation_time": {"type": "keyword"},
                        "violation": {"type": "keyword"},
                        "fine_amount": {"type": "float"},
                        "penalty_amount": {"type": "float"},
                        "interest_amount": {"type": "float"},
                        "reduction_amount": {"type": "float"},
                        "payment_amount": {"type": "float"},
                        "amount_due": {"type": "float"},
                        "precinct": {"type": "float"},
                        "county": {"type": "keyword"},
                        "issuing_agency": {"type": "keyword"},
                        "description":{"type": "keyword"},

                    }
                },
            })
        resp.raise_for_status()
        print(resp.json())
    except Exception:
        print("Index already exists! Skipping")

     
    client = Socrata("data.cityofnewyork.us",APP_TOKEN, timeout = 6000000)
    page_size = args.page_size
    num_pages = args.num_pages
    
    if num_pages is None:
        count_total1 = client.get(DATASET_ID, select='COUNT(*)')
        count_total = int(count_total1[0]["COUNT"])
        num_pages=ceil(count_total/page_size)
        print (f'num_pages = {num_pages}')
        print (f'page_size = {page_size}')
        
    for n in range(num_pages):
        rows = client.get(DATASET_ID, limit=args.page_size, offset=n*page_size)
        print(rows)
    
    
        for row in rows:
            try:
                # convert
                row["summons_number"] = int(row.get("summons_number"))
                row["fine_amount"] =float(row.get("fine_amount"))
                row["penalty_amount"] = float(row.get("penalty_amount"))
                row["interest_amount"] = float(row.get("interest_amount"))
                row["reduction_amount"] = float(row.get("reduction_amount"))
                row["payment_amount"] = float(row.get("payment_amount"))
                row["amount_due"] = float(row.get("amount_due"))
                if "issue_date" in row:
                    row["issue_date"]=datetime.strptime(row["issue_date"],"%M/%d/%Y").strftime("%Y-%M-%d")
                del row["summons_image"]
               
               
            except Exception as e:
                print(f" Error!: {e}, skipping row: {row}")
                continue

            try:
                # upload to elasticsearch by creating a doc
                resp = requests.post(
                    # this is the URL to create a new nyc_parking document
                    # which is our "row" in elasticsearch databse/table
                    f"{ES_HOST}/nyc_parking/_doc",
                    json=row,
                    auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
                    
                )
                resp.raise_for_status()
            except Exception as e:
                print(f"Failed to insert in ES: {e}, skipping row: {row}")
                continue
            
            print(resp.json())
    
