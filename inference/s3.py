import boto3

BUCKET_NAME = "apollo-ml-artifacts"

client = boto3.client("s3")


def download_file(file_path: str, key_name: str) -> None:
    """Downloads the file from s3"""
    client.download_file(Bucket=BUCKET_NAME, Key=key_name, Filename=file_path)
