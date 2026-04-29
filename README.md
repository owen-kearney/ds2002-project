# ds2002-project
Project 1: File Converter

# How to Use

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
