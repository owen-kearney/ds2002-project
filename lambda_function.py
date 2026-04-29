import boto3
import os
import traceback
from datetime import datetime, timezone
from fpdf import FPDF
import pymysql  

s3 = boto3.client("s3")

OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET", "cloud-crew-file-converter-team3")
OUTPUT_PREFIX = os.environ.get("OUTPUT_PREFIX", "output/")
TABLE_NAME    = os.environ.get("DYNAMODB_TABLE", "processing-log")

connection = pymysql.connect(
    host="ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com",
    user="cloud_crew",
    password="cloud_crew",
    database="group_3"
)

def convert_txt_to_pdf(text: str, source_filename: str) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"File: {source_filename}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    converted_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    pdf.cell(0, 6, f"Converted: {converted_at}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Courier", "", 11)
    for line in text.splitlines():
        pdf.multi_cell(0, 6, line if line.strip() else " ")
    return bytes(pdf.output())


def log_to_mysql(input_bucket, input_key, output_bucket, output_key,
                timestamp, status, error_message=""):

    cursor = connection.cursor()

    sql = """
    INSERT INTO processing_log 
    (input_key, input_bucket, output_key, output_bucket, filename, timestamp, status, error_message)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    filename = os.path.basename(input_key)

    cursor.execute(sql, (
        input_key,
        input_bucket,
        output_key,
        output_bucket,
        filename,
        timestamp,
        status,
        error_message
    ))

    connection.commit()

def lambda_handler(event, context):
    for record in event.get("Records", []):
        input_bucket = record["s3"]["bucket"]["name"]
        input_key = record["s3"]["object"]["key"].replace("+", " ")
        base_name  = os.path.splitext(os.path.basename(input_key))[0]
        output_key = f"{OUTPUT_PREFIX}{base_name}.pdf"
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        print(f"[Lambda] Received  : s3://{input_bucket}/{input_key}")
        print(f"[Lambda] Output    : s3://{OUTPUT_BUCKET}/{output_key}")

        try:
            response  = s3.get_object(Bucket=input_bucket, Key=input_key)
            raw_bytes = response["Body"].read()

            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = raw_bytes.decode("latin-1")

            print(f"[Lambda] Read {len(raw_bytes)} bytes from input")

            pdf_bytes = convert_txt_to_pdf(text, os.path.basename(input_key))
            print(f"[Lambda] PDF generated: {len(pdf_bytes)} bytes")

            s3.put_object(
                Bucket=OUTPUT_BUCKET,
                Key=output_key,
                Body=pdf_bytes,
                ContentType="application/pdf",
            )

            print(f"[Lambda] Uploaded to s3://{OUTPUT_BUCKET}/{output_key}")

            log_to_mysql(
                input_bucket=input_bucket,
                input_key=input_key,
                output_bucket=OUTPUT_BUCKET,
                output_key=output_key,
                timestamp=timestamp,
                status="Success",
            )

        except Exception:
            error_msg = traceback.format_exc()
            print(f"[Lambda] ERROR:\n{error_msg}")

            log_to_mysql(
                input_bucket=input_bucket,
                input_key=input_key,
                output_bucket=OUTPUT_BUCKET,
                output_key=output_key,
                timestamp=timestamp,
                status="Failed",
                error_message=error_msg[:1000],
            )

            raise