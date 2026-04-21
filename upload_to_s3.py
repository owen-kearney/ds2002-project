import boto3
import sys
from pathlib import Path

BUCKET_NAME = "cloud-crew-file-converter-team3"
INPUT_PREFIX = "input/"

s3 = boto3.client("s3")

def upload_file(local_file_path):
    path = Path(local_file_path)

    if not path.exists():
        print(f"File not found: {local_file_path}")
        return

    if path.suffix.lower() != ".txt":
        print("Only .txt files should be uploaded for this project.")
        return

    s3_key = INPUT_PREFIX + path.name

    s3.upload_file(
        Filename=str(path),
        Bucket=BUCKET_NAME,
        Key=s3_key
    )

    print(f"Uploaded: {local_file_path}")
    print(f"S3 location: s3://{BUCKET_NAME}/{s3_key}")
    print("This upload should trigger the Lambda function automatically.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_to_s3.py <local_txt_file>")
        sys.exit(1)

    upload_file(sys.argv[1])
