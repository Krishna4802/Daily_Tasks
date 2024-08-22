# ClickHouse

* Installing clicking in docker : docker pull yandex/clickhouse-server

* To start the container for click house in docker :  docker run -d --name clickhouse -p 8123:8123 -v ~/clickhouse_data:/var/lib/clickhouse yandex/clickhouse-server


* Go to localhost : http://localhost:8123 [ If there is OK, Then the installation was successful ]

* Cmd to start the ClickHouse terminal  :  docker exec -it clickhouse clickhouse-client

* Query for creating table :  CREATE TABLE IF NOT EXISTS patents.patent_table (
                              Patent_number String,
                              Patent_name String,
                              Patent_date Date )
                              ENGINE = MergeTree() ORDER BY Patent_number;


* Query to see list of tables in Database: SHOW TABLES FROM patents;

# Python code to insert data :

          import requests
          import json
          
          # API endpoint to fetch data
          api_url = "https://api.patentsview.org/patents/query?q={%22_gte%22:{%22patent_date%22:%222007-01-04%22}}&f=[%22patent_number%22,%22patent_date%22,%22patent_title%22]&o={%22page%22:1,%22per_page%22:1000}"
          
          # Fetch data from the API
          response = requests.get(api_url)
          data = response.json()
          
          # Prepare the data for insertion
          data_to_insert = [{'Patent_number': item['patent_number'], 'Patent_name': item['patent_title'], 'Patent_date': item['patent_date']} for item in data['patents']]
          
          # ClickHouse server details
          clickhouse_url = 'http://localhost:8123'
          
          # Construct the INSERT query URL
          insert_url = f"{clickhouse_url}/?query=INSERT%20INTO%20patents.patent_table%20FORMAT%20JSONEachRow"
          
          # Send the data to ClickHouse using POST request
          headers = {'Content-Type': 'application/json'}
          response = requests.post(insert_url, data=json.dumps(data_to_insert), headers=headers)
          
          # Check the response status
          if response.status_code == 200:
              print("Data inserted successfully.")
          else:
              print("Failed to insert data.")



* Query to view the table : SELECT * FROM patents.patent_table;


 * Query to view info of the table :  SELECT name, type
                                      FROM system.columns
               					              WHERE database = 'patents' AND table = 'patent_table';


# Query for creating a materialized view to list the count of patents per title word count  

            1)  CREATE MATERIALIZED VIEW IF NOT EXISTS patents_word_count_mv2
                ENGINE = MergeTree()
                ORDER BY word_count
                POPULATE
                AS
                SELECT
                    Patent_number,
                    Patent_name,
                    length(splitByChar(' ', Patent_name)) AS word_count
                FROM patents.patent_table;


             2) CREATE VIEW IF NOT EXISTS temp_data_view1 AS
                SELECT
                    Patent_number,
                    arrayJoin(splitByChar(' ', Patent_name)) AS word,
                    length(arrayJoin(splitByChar(' ', Patent_name))) AS word_count
                FROM patents.patent_table;


                
             3) CREATE MATERIALIZED VIEW IF NOT EXISTS patents_word_count_mv_2
                ENGINE = SummingMergeTree
                ORDER BY (total_pats, avg_word_count) 
                POPULATE
                AS
                SELECT
                    count(*) AS total_pats,
                    avg(word_count) AS avg_word_count
                FROM temp_data_view1;


# Queries to see the materialized table : 

      1)    SELECT * from  patents_word_count_mv;

      2)    SELECT word_count, count(*) AS patent_count
            FROM patents_word_count_mv
                 GROUP BY word_count
                 ORDER BY word_count;

      3)    SELECT Patent_number, Patent_name, word_count
            FROM patents_word_count_mv2;
            
      4)   SELECT * FROM patents_word_count_mv_2;
