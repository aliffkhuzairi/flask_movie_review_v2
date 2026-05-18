import boto3
import os
from botocore.exceptions import ClientError

S3_BUCKET = os.getenv('AWS_S3_BUCKET')
S3_REGION = os.getenv('AWS_REGION', 'ap-southeast-5')


def get_s3_client():
    return boto3.client(
        's3',
        region_name=S3_REGION,
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )


def upload_to_s3(file_data, filename, folder='avatars', content_type='image/jpeg'):
    s3 = get_s3_client()
    key = f"{folder}/{filename}"

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=file_data,
        ContentType=content_type
    )

    return f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{key}"


def delete_from_s3(url):
    if not url or not url.startswith('https://'):
        return

    s3 = get_s3_client()
    prefix = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/"

    if url.startswith(prefix):
        key = url[len(prefix):]
        try:
            s3.delete_object(Bucket=S3_BUCKET, Key=key)
        except ClientError:
            pass