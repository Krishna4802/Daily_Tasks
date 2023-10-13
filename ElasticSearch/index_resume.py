import warnings
from elasticsearch import Elasticsearch
from urllib3.exceptions import InsecureRequestWarning

# Disable the warning message
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200'], verify_certs=False)

# Define the resume data
resume = {
    'name': 'Krishna Prasath',
    'email': 'krishnaprasath.thirunavukaras@hashagile.com',
    'education': 'B.tech IT',
    'experience': 'Intern at HashAgile',
    'skills': ['C', 'Java', 'Data Analysis']
}

# Index the resume document
index_name = 'resumes'  # Specify the index name
document_id = '1'  # Specify a unique document ID

# Index the document into Elasticsearch
resp = es.index(index=index_name, id=document_id, document=resume)
print(resp['result'])


resp = es.get(index=index_name, id=document_id)
print(resp['_source'])

