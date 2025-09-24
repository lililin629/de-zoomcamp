#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import pandas as pd
from time import time
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # keep file extension
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    # download file
    os.system(f"wget {url} -O {csv_name}")

    # connect to Postgres
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # use iterator for large files, plain read for small
    try:
        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
        use_chunks = True
    except Exception:
        df_iter = [pd.read_csv(csv_name)]
        use_chunks = False

    # process first chunk
    df = next(iter(df_iter))

    # parse datetimes only if columns exist
    for col in ["tpep_pickup_datetime", "tpep_dropoff_datetime"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # create table schema
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
    # insert first chunk
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    if use_chunks:
        while True:
            try:
                t_start = time()
                df = next(df_iter)

                for col in ["tpep_pickup_datetime", "tpep_dropoff_datetime"]:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col])

                df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
                t_end = time()
                print(f"Inserted another chunk, took {t_end - t_start:.3f} sec")
            except StopIteration:
                print("Finished ingesting data.")
                break
    else:
        print("Finished ingesting small CSV (single batch).")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--db', required=True)
    parser.add_argument('--table_name', required=True)
    parser.add_argument('--url', required=True)
    args = parser.parse_args()

    main(args)
