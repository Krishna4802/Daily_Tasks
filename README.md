# Postgress Python

* Pull postgres Image : docker pull postgres

* Creating a Container using postgres Image
    docker run -itd -e POSTGRES_USER=<user_name> -e POSTGRES_PASSWORD=<password> -p 5432:5432  --name <container_name> postgres

    docker run -itd -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test123 -p 5432:5432 -v /data:/var/lib/postgresql/data --name postgresql postgres


# Following Command should be execute in docker terminal

* To Connect Postgres’s db in docker 
	PGPASSWORD=<password> psql -U <user_name>
	
	PGPASSWORD=test123 psql -U test

* Creating database
	create database training;
	
* To connect to db-training
	\c training
	
* Creating a Table for patents 
	CREATE TABLE patents (patent_number varchar(255),patent_title varchar(255),patent_date varchar(255));


* Install psycopg2  — To connect to Postgres’s
    pip3 install psycopg2-binary

* Install requests — To get the data from the api(Url)
    pip3 install requests 




# The code to insert data from API 

    import psycopg2
    import requests
    import json
    # Database connection parameters
    db_host = 'localhost'      # Hostname
    db_port = 5432             # Port mapped to the Docker container
    db_name = 'training'  # Name of the PostgreSQL database
    db_user = 'test'  # Username for the PostgreSQL database
    db_password = 'test123'  # Password for the PostgreSQL database

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    # Send GET request to the API
    response = requests.get('https://api.patentsview.org/patents/query?q={%22_gte%22:{%22patent_date%22:%222007-01-04%22}}&f=[%22patent_number%22,%22patent_date%22,%22patent_title%22]')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract relevant information from the response
        results = data['patents']
        # Create a cursor object to interact with the database
        cur = conn.cursor()

        #SQL query to insert data to table:patents
        insert_sql = "INSERT INTO patents (patent_number, patent_title, patent_date) VALUES (%s, %s, %s);"

        #Inserting the retrieved data from api
        for result in results:
            patent_number = result['patent_number']
            patent_date = result['patent_date']
            patent_title = result['patent_title']

            # Storing the data 
            data = [(result['patent_number'],result['patent_title'],result['patent_date'])]

            try:
                # Execute the SQL statement for each row of data
                cur.executemany(insert_sql, data)

                # Commit the changes to the database
                conn.commit()

                print("Data inserted successfully!")
            except psycopg2.Error as e:
                # Rollback the transaction if any error occurs
                conn.rollback()
                print(f"Error inserting data: {e}")

    # Close the cursor and connection
    cur.close()
    conn.close()



* Query to see output : Select * from patents




# Another Aproach

        import psycopg2
        
        # Database connection parameters
        db_host = 'localhost'      # Hostname
        db_port = 5432             # Port mapped to the Docker container
        db_name = 'training'       # Name of the PostgreSQL database
        db_user = 'test'           # Username for the PostgreSQL database
        db_password = 'test123'    # Password for the PostgreSQL database
        
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        
        # Create a cursor object to interact with the database
        cur = conn.cursor()
        
        # SQL query to create the partitioned table 'patents'
        create_table_sql = """
        CREATE TABLE patents3 (
            patent_number VARCHAR(255),
            patent_title TEXT,
            patent_date DATE
        ) PARTITION BY RANGE (patent_date);
        """
        
        try:
            # Execute the create table query
            cur.execute(create_table_sql)
        
            # Commit the changes to the database
            conn.commit()
        
            print("Table 'patents' created successfully!")
        except psycopg2.Error as e:
            # Rollback the transaction if any error occurs
            conn.rollback()
            print(f"Error creating table: {e}")
        
        # Close the cursor and connection
        cur.close()
        conn.close()



# To Add all the files from maultiple pages on Api link along with Partitioning Table 

        import psycopg2
        import requests
        import time
        from datetime import datetime, timedelta
        
        # Database connection parameters
        db_host = 'localhost'
        db_port = 5432
        db_name = 'training'
        db_user = 'test'
        db_password = 'test123'
        
        # Function to create a new connection and cursor
        def create_connection():
            return psycopg2.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=db_password
            )
        
        def create_partition(cursor, table_name, partition_name, start_time, end_time):
            query = f"""
                CREATE TABLE {partition_name} PARTITION OF {table_name}
                FOR VALUES FROM ('{start_time}') TO ('{end_time}');
            """
            cursor.execute(query)
        
        def insert_data_into_partition(cursor, table_name, data, start_time, end_time):
            insert_query = f"""
                INSERT INTO {table_name} (patent_number, patent_title, patent_date, created_at)
                VALUES (%s, %s, %s, %s);
            """
            valid_data = [(num, title, date, created_at) for num, title, date, created_at in data if start_time <= created_at < end_time]
            cursor.executemany(insert_query, valid_data)
        
        def main():
            table_name = "patents_part"
            partition_base_name = "patents8_minute_"
        
            # ... (previous code to create the main table and partitions)
        
            # Send GET request to the API with dynamic page retrieval
            for i in range(1, 40):
                url = f'https://api.patentsview.org/patents/query?q={{"_gte":{{"patent_date":"2007-01-04"}}}}&f=["patent_number","patent_date","patent_title"]&o={{"page":{i},"per_page":25}}'
                try:
                    response = requests.get(url)
                    response_data = response.json()
        
                    # Check if there is data available in the current response
                    if 'patents' not in response_data or not response_data['patents']:
                        break  # No more data available, exit the loop
        
                    # Extract relevant information from the response
                    results = response_data['patents']
        
                    # Storing the data in a list of tuples
                    data = [(result['patent_number'], result['patent_title'], result['patent_date'], datetime.now()) for result in results]
        
                    # Insert data into the appropriate partition
                    minute = datetime.now().minute  # Get the current minute
                    partition_name = f"{partition_base_name}{minute:02}"
                    start_time = datetime(2023, 7, 21, 14, minute, 0)
                    end_time = start_time + timedelta(minutes=1)
        
                    with create_connection() as conn, conn.cursor() as cursor:
                        insert_data_into_partition(cursor, partition_name, data, start_time, end_time)
                        conn.commit()
                        print(f"Inserted {len(data)} rows into {partition_name}")
        
                    # Pause for 5 seconds after each insertion
                    time.sleep(5)
        
                except requests.RequestException as re:
                    print(f"Error making API request: {re}")
                    break  # Exit the loop if there's an API request error
        
        if __name__ == "__main__":
            main()


