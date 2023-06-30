from elasticsearch import Elasticsearch
import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()
## INPUTS
opensearch_domain_url ='https://vpc-ti-shared-e2wxgh4hpjqlvfgbqe472c4maa.us-east-1.es.amazonaws.com/'
feedback_rating = 5
size = 10000

index = os.environ['INDEX_NAME']
username = os.environ['USERNAME']
password =os.environ['PASSWORD']
filename = 'qa_5star_feedback_data.json'

search_path ='jive_copilot_qa_corpus/_search'
def write_to_file(filename:str, data):
    file_data =[]
    with open(filename, 'w') as file:
        for item in data:
            file_data.append(item)
        file.write(json.dumps(file_data))

    print(f"Data written to {filename}")
    return

def get_qa_data_feedback_based():

    # Elasticsearch query
    query = {
        "size": size,
        "from": 0,
        "query": {
            "term": {
                "feedback.rating": feedback_rating
            }
        }
    }

    # Execute the query


    # Execute the query
    response = requests.get(
        url=opensearch_domain_url+search_path,
        auth=(username, password),  # if authentication is required
        headers={'Content-Type': 'application/json'},
        data=json.dumps(query)
    )

    # Extract the data from the response
    hits = response.json()['hits']['hits']

    data = [hit['_source'] for hit in hits]

    # Write the data into a file
    write_to_file(filename,data)




get_qa_data_feedback_based()