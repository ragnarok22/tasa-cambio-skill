import logging
import os
import random

import boto3
import requests
from botocore.exceptions import ClientError


def create_presigned_url(object_name):
    """Generate a presigned URL to share an S3 object.

    Currently unused but ready for future features requiring temporary S3 links.

    Args:
        object_name: S3 object key

    Returns:
        Presigned URL string (60 second expiration), or None if error occurs
    """
    s3_client = boto3.client(
        "s3",
        region_name=os.environ.get("S3_PERSISTENCE_REGION"),
        config=boto3.session.Config(
            signature_version="s3v4", s3={"addressing_style": "path"}
        ),
    )
    try:
        bucket_name = os.environ.get("S3_PERSISTENCE_BUCKET")
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=60,
        )
    except ClientError as e:
        logging.error(e)
        return None

    return response


def get_exchange_rates():
    """Fetch current exchange rates from the proxy API.

    Returns:
        dict: Exchange rates with keys 'USD', 'EUR', 'MLC' (float values)
        Returns None if API request fails

    Raises:
        None - errors are caught and None is returned
    """
    url = "https://tasa-cambio-cuba.vercel.app/api/exchange-rate"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            "USD": data["usd"],
            "EUR": data["eur"],
            "MLC": data["mlc"],
        }
    except (requests.RequestException, KeyError, ValueError) as e:
        logging.error(f"Error fetching exchange rates: {e}")
        return None


def get_random_greeting():
    """Return a random Cuban Spanish greeting phrase.

    Returns:
        str: Random greeting from predefined list of Cuban expressions
    """
    greetings_list = [
        "Asere que bolá? Los precios están mandáo",
        "En talla asere",
        "Ufff, los precios están por las nubes",
        "Saludos broder",
    ]
    return random.choice(greetings_list)
