import logging
import os
import boto3
import requests
from botocore.exceptions import ClientError


def create_presigned_url(object_name):
    """Generate a presigned URL to share an S3 object with a capped expiration of 60 seconds

    :param object_name: string
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3',
                             region_name=os.environ.get('S3_PERSISTENCE_REGION'),
                             config=boto3.session.Config(signature_version='s3v4',s3={'addressing_style': 'path'}))
    try:
        bucket_name = os.environ.get('S3_PERSISTENCE_BUCKET')
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=60*1)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def get_exchange_rates():
    url = "https://exchange-rate.decubba.com/api/informal/cup"

    response = requests.get(url)
    data = response.json()
    currencies = {}
    for exchange_rate in data["exchange_rate"]:
        source_currency = exchange_rate["source_currency"]
        mid_value = exchange_rate["mid"]
        currencies[source_currency] = mid_value
    
    return currencies
    