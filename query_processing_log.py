#!/usr/bin/env python3
"""
Usage:
    python query_processing_log.py <input_key_or_prefix>
 
Environment variables (uses a hard coded default if not set):
    DB_HOST      - MySQL host/endpoint (e.g. your-rds-instance.rds.amazonaws.com)
    DB_PORT      - MySQL port (default: 3306)
    DB_USER      - MySQL username  (e.g. cloud_crew)
    DB_PASSWORD  - MySQL password  (e.g. cloud_crew)
    DB_NAME      - MySQL database  (e.g. group_3)
"""
 
import os
import sys
import pymysql
from pymysql import Error
 
def get_connection():
    #creates a MySQL connection using environment variables
    host     = os.environ.get("DB_HOST", "ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com")
    port     = int(os.environ.get("DB_PORT", 3306))
    user     = os.environ.get("DB_USER", "cloud_crew")
    password = os.environ.get("DB_PASSWORD", "cloud_crew")
    database = os.environ.get("DB_NAME", "group_3")
 
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connect_timeout=10,
            cursorclass=pymysql.cursors.DictCursor,
        )
        return conn
    except Error as e:
        print(f"[ERROR] Could not connect to database: {e}")
        print(
            "\nMake sure the following environment variables are set:\n"
            "  DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME"
        )
        sys.exit(1)
 
def query_by_input_key(input_key_or_prefix: str) -> list[dict]:
    """
    Query the processing-log table for rows where input_key matches
    the given value exactly, OR starts with the given prefix.
 
    Returns a list of result dicts.
    """
    conn   = get_connection()
    cursor = conn.cursor()
 
    like_pattern = input_key_or_prefix + "%" if not input_key_or_prefix.endswith("%") else input_key_or_prefix
 
    sql = """
        SELECT
            input_key,
            input_bucket,
            output_key,
            output_bucket,
            filename,
            timestamp,
            status,
            error_message
        FROM processing_log
        WHERE input_key LIKE %s
        ORDER BY timestamp DESC
    """
 
    try:
        cursor.execute(sql, (like_pattern,))
        rows = cursor.fetchall()
    except Error as e:
        print(f"[ERROR] Query failed: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()
 
    return rows

def print_results(rows: list[dict], search_term: str) -> None:
    #print the query results
    if not rows:
        print(f"No processing record found for: '{search_term}'")
        print("The file may not have been uploaded yet, or processing may still be in progress.")
        return
 
    print(f"\nFound {len(rows)} record(s) matching '{search_term}':\n")
    print("=" * 70)
 
    for i, row in enumerate(rows, start=1):
        status = row.get("status", "Unknown")
 
        print(f"Record {i}:  {status.upper()}")
        print(f"  Timestamp     : {row.get('timestamp', 'N/A')}")
        print(f"  Input file    : {row.get('filename', 'N/A')}")
        print(f"  Input  S3     : s3://{row.get('input_bucket', '?')}/{row.get('input_key', '?')}")
 
        if status.lower() == "success":
            print(f"  Output S3     : s3://{row.get('output_bucket', '?')}/{row.get('output_key', '?')}")
        else:
            error = row.get("error_message") or "No error message recorded."
            print(f"  Error         : {error[:200]}")
 
        print("-" * 70)
 
def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
 
    search_term = sys.argv[1].strip()
 
    if not search_term:
        print("[ERROR] Search term cannot be empty.")
        sys.exit(1)
 
    rows = query_by_input_key(search_term)
    print_results(rows, search_term)
 
    #exit with code 1 if nothing was found
    if not rows:
        sys.exit(1)
 

if __name__ == "__main__":
    main()
