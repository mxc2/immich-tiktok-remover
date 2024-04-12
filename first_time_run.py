from immich import pingServer

def firstLines():
    print("\nLooks like this is your first time running this script. Let's set up some things.")
    print("First, we need to set up the configuration file. This file will store your API key and the Immich domain.")
    print("This file will be stored in the same directory as this script.")

    print("Don't know where to get a API key? Documentation is here: https://immich.app/docs/features/command-line-interface/#obtain-the-api-key")

def configureImmich():
    print("\nPlease enter your Immich URL, with http/https and port (e.g. http://192.168.1.4:2283): ")
    immich_domain = input()
    print("Please enter your Immich API key: ")
    immich_api_key = input()

    # Format domain
    if not immich_domain.startswith("http"):
        immich_domain = "http://" + immich_domain
    if not immich_domain.endswith("/"):
        immich_domain += "/"

    env_vars = {
        "DOMAIN": immich_domain,
        "API_KEY": immich_api_key
    }

    # Write the envirohttp://192.168.1.39:2283nment variables to the .env file
    with open(".env", "w") as env_file:
        for key, value in env_vars.items():
            env_file.write(f"{key}={value}\n")

    print("Configuration file has been created successfully.")
    return immich_domain, immich_api_key

def firstTimeRunning():
    firstLines()
    configureImmich()

    print("\nTrying to ping the server to check if everything is working.")
    try:
        pingServer()
        print("Successfully connected to the Immich server. \n")
    except Exception as e:
        print("Error while trying to connect to the Immich server.")
        retry = input("Do you want to retry configuration? (yes/no): ")
        if retry.lower() == "yes" or retry.lower() == "y":
            # Retry configuration
            firstTimeRunning()
        else:
            print("Exiting...")
            exit()
