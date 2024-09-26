  import pandas as pd
from sqlalchemy import create_engine, text
import sys

def clean_dataframe(df):
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: x.replace('\x00', '') if isinstance(x, str) else x)
    return df

def migrate_data(mysql_db_name, postgres_db_name):
    mysql_user = 'root'
    mysql_password = '123'
    mysql_host = '127.0.0.1'
    mysql_port = '3306'  

    postgres_user = 'pgloader_pg'
    postgres_password = '123'
    postgres_host = 'localhost'
    postgres_port = '5432'  

    target_schema = 'sample_mysql_db_stage'
    
    mysql_engine = create_engine(f'mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db_name}')

    postgres_engine = create_engine(f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db_name}')
    
    with postgres_engine.connect() as connection:
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {target_schema}"))

    
    with mysql_engine.connect() as connection:
        tables = connection.execute(text("SHOW TABLES")).fetchall()
        table_names = [table[0] for table in tables]

    for table in table_names:
        print(f'Migrating table: {table}')
        
        df = pd.read_sql_table(table, mysql_engine)
        
        df = clean_dataframe(df)
        
        table_lower = table.lower()  
        df.to_sql(table_lower, postgres_engine, if_exists='replace', index=False, schema=target_schema)
        
        print(f'Table {table_lower} migrated successfully to schema {target_schema}!')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python migrate.py <mysql_db_name> <postgres_db_name>")
        sys.exit(1)

    mysql_db = sys.argv[1]
    postgres_db = sys.argv[2]

    migrate_data(mysql_db, postgres_db)
