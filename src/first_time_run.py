"""
Holds functions that are called when the script is run for the first time.
"""

import sys
from immich import pingServer

def firstIntroductionLines():
    """
    Print introduction lines for the first run of the script.
    """

    print("\nLooks like this is your first time running this script. Let's set up some things.")
    print("First, we need to set up the configuration file. This file will store your API key and the Immich domain.")
    print("This file will be stored in the same directory as this script.")

    print("Don't know where to get a API key? Documentation is here: https://immich.app/docs/features/command-line-interface/#obtain-the-api-key")

def askForHttpOrHttps(immich_domain: str):
    """
    Ask the user to enter http or https for the domain and then return the formatted domain URL.
    """

    while True:
        print("\nFor domain you entered:", immich_domain)
        print("Entered domain does not start with http/https. It is needed for archiving/trashing videos to work. Insert 1 for http, 2 for https: ")
        http_or_https = input()
        match http_or_https:
            case "1":
                immich_domain = "http://" + immich_domain
                break
            case "2":
                immich_domain = "https://" + immich_domain
                break
            case _:
                print("Invalid input. Trying again...")
                continue

    return immich_domain

def configureImmich():
    """
    Configure Immich settings.

    This function prompts the user to enter their Immich URL and API key. 
    It formats the domain URL and writes the environment variables to the .env file.
    """

    print("\nPlease enter your Immich URL, with http/https and port (e.g. http://192.168.1.4:2283): ")
    immich_domain = input()
    print("Please enter your Immich API key: ")
    immich_api_key = input()

    # Format domain
    if not immich_domain.startswith("http"):
        immich_domain = askForHttpOrHttps(immich_domain)
    if not immich_domain.endswith("/"):
        immich_domain += "/"

    env_vars = {
        "DOMAIN": immich_domain,
        "API_KEY": immich_api_key
    }

    # Write the environment variables to the .env file
    with open(".env", "w", encoding="utf-8") as env_file:
        for key, value in env_vars.items():
            env_file.write(f"{key}={value}\n")


    print("Configuration file has been created successfully.")
    return immich_domain, immich_api_key

def firstTimeRunning():
    """
    Perform setup and check server connection for first-time run.

    This function calls the 'configureImmich()' function to set up Immich settings.
    Then it attempts to ping the server to check if the configuration is successful.
    If there's an error during the connection attempt, it prompts the user to retry configuration.
    """

    configureImmich()

    print("\nTrying to ping the server to check if everything is working.")
    try:
        pingServer()
        print("Successfully connected to the Immich server. \n")
    except Exception as e:
        print("Error while trying to connect to the Immich server: ", e)
        retry = input("Do you want to retry configuration? (yes/no): ")
        if retry.lower() == "yes" or retry.lower() == "y":
            # Retry configuration
            firstTimeRunning()
        else:
            print("Exiting...")
            sys.exit()
