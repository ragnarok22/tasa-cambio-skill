import logging
import random
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
    url = "https://tasa-cambio-cuba.vercel.app/api/exchange-rate"

    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    currencies = {
        "USD": data["usd"],
        "EUR": data["eur"],
        "MLC": data["mlc"],
    }
    
    return currencies


def get_random_greating():
    greatings_list = ["Asere que bolá? Los precios están mandáo", "En talla asere", "Ufff, los precios están por las nubes", "Saludos broder"]
    return random.choice(greatings_list)
