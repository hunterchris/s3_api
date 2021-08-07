import os
from flask import Flask, jsonify
import boto3
import botocore
import logging

AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET=os.getenv('BUCKET')
app = Flask(__name__)
@app.route('/')
def home():
    logger = logging.getLogger()
    s3 = boto3.client('s3')
    keys = []
    try:
        logger.info('Listing contents of bucket',BUCKET)
        result = s3.list_objects_v2(Bucket=BUCKET)
        for obj in result['Contents']:
            keys.append(obj['Key'])
        return jsonify({"Bucket": str(BUCKET), "Contents": str(keys)})
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'NoSuchBucket':
            logger.warn('The bucket requested was not found:',BUCKET)
            return jsonify('Not found')
        else:
            raise error 
