# ds2002-project
Project 1: File Converter

# How to Use


Querying the Processing Log:
Uses the script query_processing_log.py.
You may need to run pip install pymysql if it is not already installed.
You will need the following environment variables for this to run correctly:
    DB_HOST      - MySQL host/endpoint (your-rds-instance.rds.amazonaws.com)
    DB_PORT      - MySQL port (default is 3306)
    DB_USER      - MySQL username  
    DB_PASSWORD  - MySQL password  
    DB_NAME      - MySQL database
Enter this line in the terminal to run the script: python query_processing_log.py <input_key_or_prefix>.
