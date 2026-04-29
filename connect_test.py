import pymysql

connection = pymysql.connect(
    host="ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com",
    user="cloud_crew",
    password="cloud_crew",
    database="group_3"
)

print("Connected!")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS processing_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input_key VARCHAR(255),
    input_bucket VARCHAR(100),
    output_key VARCHAR(255),
    output_bucket VARCHAR(100),
    filename VARCHAR(255),
    timestamp DATETIME,
    status VARCHAR(25),
    error_message TEXT
);
""")

connection.commit()
print("Table ready!")


cursor.execute("SELECT * FROM processing_log")
rows = cursor.fetchall()

print("\nDatabase Records:")

if len(rows) == 0:
    print("No records found.")
else:
    for row in rows:
        print(row)

connection.close()
print("\nDone.")