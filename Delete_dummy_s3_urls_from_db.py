import boto3
import psycopg2
from botocore.exceptions import ClientError
import configparser

config = configparser.ConfigParser()
config.read('config.properties')

AWS_ACCESS_KEY = config['aws']['aws_access_key']
AWS_SECRET_KEY = config['aws']['aws_secret_key']

DB_HOST = config['db']['db_host']
DB_NAME = config['db']['db_name']
DB_USER = config['db']['db_user']
DB_PASSWORD = config['db']['db_password']

LAST_PROCESSED_FILE = 'last_processed_id.txt'
BATCH_SIZE = 2

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

def file_exists_in_s3(s3_url):
    try:
        bucket_name = s3_url.split('/')[2]
        file_key = '/'.join(s3_url.split('/')[3:])
        s3.head_object(Bucket=bucket_name, Key=file_key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise e

def update_pdf_url_to_null(cursor, conn, file_id):
    update_query = "UPDATE s3_file_test SET pdf_s3_url = NULL WHERE id = %s"
    cursor.execute(update_query, (file_id,))
    conn.commit()

def read_last_processed_id():
    try:
        with open(LAST_PROCESSED_FILE, 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

def write_last_processed_id(file_id):
    with open(LAST_PROCESSED_FILE, 'w') as f:
        f.write(str(file_id))

def main():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            port=PORT,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        last_processed_id = read_last_processed_id()

        while True:
            cursor.execute("SELECT id, pdf_s3_url FROM s3_file_test WHERE id > %s ORDER BY id ASC LIMIT %s", 
                           (last_processed_id, BATCH_SIZE))
            records = cursor.fetchall()

            if not records:
                print("All records processed.")
                break

            for record in records:
                file_id, s3_url = record
                if s3_url and not file_exists_in_s3(s3_url):
                    update_pdf_url_to_null(cursor, conn, file_id)
    
                last_processed_id = file_id
                write_last_processed_id(last_processed_id)

            print(f"Batch processed up to ID: {last_processed_id}")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    main()
