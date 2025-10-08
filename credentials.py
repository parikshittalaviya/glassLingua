import json
from google.oauth2 import service_account
import os

def get_credentials():
    if not hasattr(get_credentials, "credentials"):
        with open(r"C:\Users\parik\Desktop\Glass Lingua\Google Cloud\newToken.json") as source:
            info = json.load(source)
            get_credentials.credentials = service_account.Credentials.from_service_account_info(info)
    return get_credentials.credentials