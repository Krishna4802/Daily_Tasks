26/07/2023

*************************************************************************************************************************************************************************************

Using Python Load 1000 rows from API https://api.patentsview.org/patents/query?q={%22_and%22:[{%22_gte%22:{%22patent_date%22:%222007-04-10%22}},{%22inventor_last_name%22:%22Whitney%22}]}&f=[%22patent_title%22,%22patent_number%22,%22patent_date%22,%22inventor_last_name%22]&_gl=1*1921iv2*_ga*MTA4MTg0OTMyNi4xNjg5ODQxNjU0*_ga_K4PTTLH074*MTY5MDI5MDk0OS4zLjEuMTY5MDI5MDk3Ny4zMi4wLjA. to table in json column

import requests
import psycopg2
import json

db_params = {
    "dbname": "postgres",
    "user": "test",
    "password": "test123",
    "host": "localhost",
    "port": "5433"
}

# Function to fetch data from the API and insert it into the table
def load_data_into_db():
    url = "https://api.patentsview.org/patents/query?q={%22_and%22:[{%22_gte%22:{%22patent_date%22:%222007-04-10%22}},{%22inventor_last_name%22:%22Whitney%22}]}&f=[%22patent_title%22,%22patent_number%22,%22patent_date%22,%22inventor_last_name%22]&o={%22page%22:1,%22per_page%22:1000}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error if the response status is not successful (e.g., 200 OK)
    except requests.exceptions.RequestException as e:
        print("Error fetching data from the API:", e)
        return

    data = response.json()

    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patent_data (
            data JSON NOT NULL
        )
    """)

    # Insert the data into the table
    try:
        for row in data["patents"][:1000]:
            json_data = json.dumps(row)  # Convert the dictionary to JSON string
            cursor.execute("""
                INSERT INTO patent_data (data)
                VALUES (%s)
            """, (json_data,))
    except Exception as e:
        print("Error inserting data into table:", e)

    connection.commit()
    connection.close()

# Call the function to load data into the database
load_data_into_db()


*************************************************************************************************************************************************************************************


Using SQL Create a rn column in table and set the value to serial [Use alter command]



import psycopg2

# Replace these values with your database credentials
db_params = {
    "dbname": "postgres",
    "user": "test",
    "password": "test123",
    "host": "localhost",
    "port": "5433"
}

def add_rn_column():
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Add the "rn" column with serial type using ALTER command
    try:
        cursor.execute("""
            ALTER TABLE patent_data
            ADD COLUMN rn SERIAL
        """)
        print("Column 'rn' added successfully.")
    except Exception as e:
        print("Error adding column:", e)

    connection.commit()
    connection.close()

# Call the function to add the "rn" column
add_rn_column()




To see output :


SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'patent_data';



*************************************************************************************************************************************************************************************

create a db function which will take min_id and max_id as input and return the data from table in json rows
* get_patent_data(p_min_id, p_max_id)
    * output format :
        * json1
        * json2





CREATE OR REPLACE FUNCTION get_patent_data(p_min_id INTEGER, p_max_id INTEGER)
RETURNS SETOF JSON AS
$$
DECLARE
    row_data JSON;
BEGIN
    FOR row_data IN
        SELECT data FROM patent_data
        WHERE rn >= p_min_id AND rn <= p_max_id
    LOOP
        RETURN NEXT row_data;
    END LOOP;
    RETURN;
END;
$$
LANGUAGE plpgsql;



SELECT * FROM get_patent_data(1, 10);




CREATE OR REPLACE FUNCTION get_patent_data1(p_min_id INTEGER, p_max_id INTEGER)
RETURNS SETOF JSON AS
$$
BEGIN
    RETURN QUERY
    SELECT data FROM patent_data
    WHERE rn >= p_min_id AND rn <= p_max_id;
END;
$$
LANGUAGE plpgsql;



SELECT * FROM get_patent_data1(1, 10);



*************************************************************************************************************************************************************************************


Create a Python Code
* infinite while loop
    * using random value increment max_id and fetch values from get_patent_data
    * Load the data to Kafka Topic




import psycopg2
from kafka import KafkaProducer
import json
import time
import random

# Replace these values with your database credentials
db_params = {
    "dbname": "postgres",
    "user": "test",
    "password": "test123",
    "host": "localhost",
    "port": "5433"
}

# Kafka setup
bootstrap_servers = 'localhost:9092'
topic_name = 'patent_topic'
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

def get_patent_data(p_min_id, p_max_id):
    # The database function to fetch data within the specified ID range
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    cursor.callproc("get_patent_data", (p_min_id, p_max_id))
    data = cursor.fetchall()

    connection.commit()
    connection.close()

    return data

def simulate_fetching_data():
    # Simulate fetching data by calling the database function with random ID ranges
    while True:
        min_id = random.randint(1, 1000)
        max_id = min_id + random.randint(1, 100)
        data = get_patent_data(min_id, max_id)
        for row_data in data:
            producer.send(topic_name, value=row_data[0])
            print("Data sent to Kafka:", row_data[0])
        time.sleep(10)

if __name__ == "__main__":
    simulate_fetching_data()




See output in : http://localhost:9000/topic/patent_topic



*************************************************************************************************************************************************************************************



Create two consumers with duplicate 
* SOLR
    * index the data to solr
        * patent_title
        * patent_number
        * patent_date
        * inventor_names as list
* Elastic
    * index the data to es
        * patent_title
        * patent_number
        * patent_date
        * inventor_names as list



Solr :

import json
import pysolr
from kafka import KafkaConsumer

# Replace this with the URL of your Solr server and core
solr_url = 'http://localhost:8989/solr/patents_core'

# Function to index data into Solr
def index_data_to_solr(data):
    solr = pysolr.Solr(solr_url, timeout=10)

    # Create a list to store the documents
    documents = []

    for message in data:
        # Assuming the message value is in JSON format
        document = json.loads(message.value)
        documents.append(document)

    solr.add(documents)
    solr.commit()

# Implement a Kafka consumer that reads data from the Kafka topic and calls the indexing function
def kafka_to_solr_consumer():
    consumer = KafkaConsumer(
        'patent_topic',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: x.decode('utf-8')
    )

    for message in consumer:
        index_data_to_solr([message])

        # Print the message to confirm it was indexed
        print("Data indexed to Solr:", message.value)

if __name__ == "__main__":
    kafka_to_solr_consumer()




See the output : http://localhost:8989/solr/#/patent_core/query?q=*:*&q.op=OR&indent=true&rows=1000&useParams=


 Elastic Search import json
from elasticsearch import Elasticsearch

# Replace this with the URL of your Elasticsearch server
es_url = 'http://localhost:9200/'

# Function to index data into Elasticsearch
def index_data_to_es(data):
    es = Elasticsearch(es_url)

    for row_data in data:
        es.index(index='patents_index', body=row_data)  # Remove 'doc_type' parameter

# Implement an Elasticsearch consumer that reads data from the Kafka topic and indexes it
def es_consumer():
    from kafka import KafkaConsumer

    consumer = KafkaConsumer(
        'patent_topic',  
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        data = message.value
        index_data_to_es([data])
        print("Data indexed to Elasticsearch:", data)

# Run the Elasticsearch consumer
es_consumer()



To see output :

curl -X GET "http://localhost:9200/patent/_search?pretty" -H "Content-Type: application/json" -d' 
{
  "query": {
    "match_all": {}
  }
}
'

