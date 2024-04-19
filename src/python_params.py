import sys

def get_config_params():
    """
    Retrieves configuration parameters based on command-line arguments and default values.
    """
    config_params = {
        "outputAllVideos": False,
        "archiveVideos": False,
        "avoidImageRecognition": False, # Skips image recognition for archiving/deletion
        "searchArchived": False,
        "fileTypesToCheckFor": ["mp4"], # Default file type for TikTok videos
        "fileNameLength": 32, # 32 seems to be the length of TikTok video names
        "fileNameIsAlumn": True,
        "fileCreatedAfter": 1472688000, # 1472688000 is the timestamp for September 1, 2016
        "textToCheckFor": "TikTok",
    }

    if "--output-all" in sys.argv:
        config_params["outputAllVideos"] = True
    if "--archive" in sys.argv:
        config_params["archiveVideos"] = True
    if "--search-archived" in sys.argv:
        config_params["searchArchived"] = True
        config_params["archiveVideos"] = False
    if "--avoid-image-recognition" in sys.argv:
        config_params["avoidImageRecognition"] = True
    if "--file-types" in sys.argv:
        config_params["fileTypesToCheckFor"] = []
        index = sys.argv.index("--file-types") + 1
        if index < len(sys.argv):
            file_types = sys.argv[index].split(',')
            config_params["fileTypesToCheckFor"].extend(file_types)
    if "--file-name-length" in sys.argv:
        index = sys.argv.index("--file-name-length") + 1
        if index < len(sys.argv):
            config_params["fileNameLength"] = int(sys.argv[index])
    if "--file-name-is-not-alumn" in sys.argv:
        config_params["fileNameIsAlumn"] = False
    if "--file-created-after" in sys.argv:
        index = sys.argv.index("--file-created-after") + 1
        if index < len(sys.argv):
            config_params["fileCreatedAfter"] = int(sys.argv[index])
    if "--text-to-check" in sys.argv:
        index = sys.argv.index("--text-to-check") + 1
        if index < len(sys.argv):
            config_params["textToCheckFor"] = sys.argv[index]

    return config_params
