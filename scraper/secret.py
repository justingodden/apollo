import json

from sqlalchemy.engine import URL
import boto3


def get_secret() -> URL:
    secret_name = "apollo-rds-secret"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    secret = get_secret_value_response['SecretString']
    connection_settings = json.loads(secret)

    connection_uri = URL.create(
        drivername="mysql+mysqlconnector",
        host=connection_settings["host"],
        port=connection_settings["port"],
        database=connection_settings["dbname"],
        username=connection_settings["username"],
        password=connection_settings["password"],
    )

    return connection_uri
