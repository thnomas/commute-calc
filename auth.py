import requests
from manage_tokens import *
import time
from dotenv import load_dotenv
import os

# client_id = '13718'
# client_secret = 'ad3bb9fabcafb01d9f2f8a2871d23f5c1a8825a7'
# code = '1b8b42e5629962fb59425d0e9aba7764573570b3'

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
CODE = os.getenv("STRAVA_CODE")

info = read_from_file()
refresh_token = info['refresh_token']

def generate_new_token():
    url = f"https://www.strava.com/oauth/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={CODE}&grant_type=refresh_token&refresh_token={refresh_token}"

    payload = {}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()

    print(data)
    write_to_file(data)
    return data

def check_token_expiration(info):
    now = int(time.time())
    if now >= int(info["expires_at"]):
       print("Token expired...")
       print("Generating new token...")
       generate_new_token()
       return True
    else:
        print("Valid Token")

