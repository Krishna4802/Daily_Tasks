import warnings
from elasticsearch import Elasticsearch

# Disable the warning message
warnings.filterwarnings("ignore", category=DeprecationWarning)

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
index_name = 'test-index'
document_id = '1'

# Index the document into Elasticsearch
es.index(index=index_name, id=document_id, body=resume)

# Refresh the index
es.indices.refresh(index=index_name)

# Search and print the indexed documents
resp = es.search(index=index_name, body={"query": {"match_all": {}}})
hits = resp['hits']['hits']
for hit in hits:
    print(hit["_source"])
