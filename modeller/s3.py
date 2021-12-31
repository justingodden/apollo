import boto3


BUCKET_NAME = "apollo-ml-artifacts"

client = boto3.client("s3")


def upload_file(file_path, key_name) -> None:
    """Uploads the file to s3"""
    client.upload_file(file_path, BUCKET_NAME, key_name)
