import boto3
import os
import logging

logger = logging.getLogger(__name__)

s3 = boto3.client('s3',
                  endpoint_url='http://minio:9000',
                  aws_access_key_id='minio',
                  aws_secret_access_key='minio123',
                  region_name='us-east-1')


def create_bucket(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        logger.info(f"Bucket {bucket_name} already exists")
    except Exception as e:
        s3.create_bucket(Bucket=bucket_name)
        logger.info(f"Created bucket {bucket_name}")


def upload_file(file, bucket_name, object_name=None):
    try:
        create_bucket(bucket_name)
        if object_name is None:
            object_name = file.filename
        logger.info(f"Uploading file {file.filename} to bucket {bucket_name} as {object_name}")
        s3.upload_fileobj(file.file, bucket_name, object_name)
        url = f"{s3.meta.endpoint_url}/{bucket_name}/{object_name}"
        logger.info(f"File uploaded successfully, URL: {url}")
        return url
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        raise
