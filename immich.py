import requests
import json
from dotenv import dotenv_values
from python_params import get_config_params

params = get_config_params()

def pingServer():
    config = dotenv_values(".env")
    url = config.get("DOMAIN") + "api/server-info/ping"
    API_KEY = config.get("API_KEY")

    payload = {}
    headers = {
        'x-api-key': API_KEY,
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if (response.status_code == 200):
        return True
    return False

def getAllAssets():
    config = dotenv_values(".env")
    searchArchived = params["searchArchived"]
    if searchArchived:
        url = config.get("DOMAIN") + "api/asset"
    else:
        url = config.get("DOMAIN") + "api/asset?isArchived=false"
        
    API_KEY = config.get("API_KEY")

    payload = {}
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error while trying to connect to Immich:", response.text)

def serveVideo(id):
    config = dotenv_values(".env")
    url = config.get("DOMAIN") + "api/asset/file/" + id
    API_KEY = config.get("API_KEY")

    payload = {}
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.content
    else:
        print("Error while trying to serve video:", response.text)

def trashVideo(id):
    config = dotenv_values(".env")
    url = config.get("DOMAIN") + "api/asset"
    API_KEY = config.get("API_KEY")

    payload = {
        "force": False,
        "ids": [id]
    }
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    # Convert payload to JSON
    json_payload = json.dumps(payload)

    # Send the request
    response = requests.delete(url, headers=headers, data=json_payload)

    if response.status_code == 204:
        print("Successfully trashed video.")
    else:
        print("Error while trying to trash video: ", response.text)
        
def archiveVideo(id):
    config = dotenv_values(".env")
    url = config.get("DOMAIN") + "api/asset"
    API_KEY = config.get("API_KEY")

    payload = {
    "ids": [id],
    "isArchived": True,
    }
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json',
    }

    # Convert payload to JSON
    json_payload = json.dumps(payload)

    response = requests.request("PUT", url, headers=headers, data=json_payload)

    if response.status_code == 204:
        print("Successfully archived video.")
    else:
        print("Error while trying to archive video:", response.text)