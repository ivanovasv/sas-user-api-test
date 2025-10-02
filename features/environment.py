import os

from common.api_client import ApiClient

def before_all(context):
    base_url = "https://fakestoreapi.com"
    token = os.getenv("API_TOKEN")

    context.api_client = ApiClient(base_url=base_url, token=token)
