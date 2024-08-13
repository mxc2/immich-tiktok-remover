"""
Holds the logic for interacting with the Immich API.
"""

import requests
import json
from dotenv import dotenv_values
from python_params import get_config_params

params = get_config_params()

def pingServer():
    """
    Ping the server to check if it's reachable.
    """
    config = dotenv_values(".env")
    url = config.get("DOMAIN") + "api/server-info/ping"
    API_KEY = config.get("API_KEY")

    payload = {}
    headers = {
        'x-api-key': API_KEY,
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return True
    return False

def getAllAssets():
    """
    Retrieve all assets from the server with paginated requests.
    """
    config = dotenv_values(".env")
    searchArchived = params["searchArchived"]

    url = config.get("DOMAIN") + "api/search/metadata"
    API_KEY = config.get("API_KEY")
    
    headers = {
        'x-api-key': API_KEY,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    all_assets = []
    next_page = 1
    payload = {
        "type": "VIDEO",
        "page": 1
    }
        
    if searchArchived:
        payload["isArchived"] = True

    while next_page:
        
        payload["page"] = next_page
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            assets = data.get("assets", {})
            items = assets.get("items", [])
            all_assets.extend(items)
            next_page = assets.get("nextPage")
        else:
            print("Error while trying to connect to Immich:", response.text)
            break

    return all_assets

def serveVideo(id: str):
    """
    Serve video content based on the provided ID.
    """
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

def trashVideo(id: str):
    """
    Trash a video based on the provided ID.
    """
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
        print("\n If this error persists, please check .env file for correct URL and API key.\n")
        
def archiveVideo(id: str):
    """
    Archive a video based on the provided ID.
    """
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
        print("\n If this error persists, please check .env file for correct URL and API key.\n")
