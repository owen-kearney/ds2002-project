# ds2002-project
Project 1: File Converter

# How to Use

## S3 Bucket Setup and Upload Trigger
This project uses an Amazon S3 bucket to store both input text files and converted PDF outputs. 

Bucket name:

```bash
cloud-crew-file-converter-team3 
```
The S3 bucket is structured with two folders to seperate input and output data:
* input/ — stores uploaded .txt files that will be processed
* output/ — stores the generated .pdf files after conversion

This structure ensures a clear separation between raw input data and processed output, making the pipeline easier to manage and debug. 
An S3 event notification is configured so that when a .txt file is uploaded to the input/ folder, the Lambda function is automatically triggered. 

Trigger configuration:
```bash
Prefix: input/
Suffix: .txt
Event type: ObjectCreated
```
This ensures that only valid input files (such as input/example.txt) trigger the pipeline, while other files (e.g, non-.txt files or files outside the input folder) are ignored. 

## Uploading Files to S3
Files can be uploaded manually through the AWS Console or using the AWS CLI. 
Example AWS CLI upload: 
```bash
aws s3 cp your_file.txt s3://cloud-crew-file-converter-team3/input/your_file.txt
```

Once uploaded, the Lambda function will automatically process the file and generate a corresponding PDF in the output folder.
To check the output folder:

```bash
aws s3 ls s3://cloud-crew-file-converter-team3/output/
```

## Uploading Files with Boto3
Files can also be upload programmatically using Boto3. Uploading a '.txt' file to the 'input/' folder triggers the Lambda function automatically. 

Example: 
```python
import boto3
import os

BUCKET_NAME = "cloud-crew-file-converter-team3"

s3 = boto3.client("s3")
s3.upload_file("test.txt", BUCKET_NAME, "input/test.txt")
```

## S3 Permissions and Access
The Lambda execution role is configured with permissions to:
* Read '.txt' files from the 'input/' folder
* Write '.pdf' files to the 'output/' folder



## Lambda File Conversion

Uses `lambda_function.py` to convert `.txt` files to `.pdf` files.

You may need to run:
```bash
pip install fpdf2
```

Setup:
```bash
pip install -r requirements.txt --target ./lambda_package
cp lambda_function.py lambda_package/
cd lambda_package
zip -r ../lambda_deployment.zip .
cd ..
aws lambda update-function-code --function-name txt-to-pdf-converter --zip-file fileb://lambda_deployment.zip --region us-east-1
```

Test:
```bash
aws s3 cp your_file.txt s3://cloud-crew-file-converter-team3/input/your_file.txt
aws s3 ls s3://cloud-crew-file-converter-team3/output/
```

The converted file will appear as `your_file.pdf`.


## Querying the Processing Log

Uses the script `query_processing_log.py`.

You may need to run:

```bash
pip install pymysql
```

if it is not already installed.

You will need the following environment variables:

- **DB_HOST** — MySQL host/endpoint (`your-rds-instance.rds.amazonaws.com`)
- **DB_PORT** — MySQL port (default: `3306`)
- **DB_USER** — MySQL username
- **DB_PASSWORD** — MySQL password
- **DB_NAME** — MySQL database

Run the script with:

```bash
python query_processing_log.py <input_key_or_prefix>
```
