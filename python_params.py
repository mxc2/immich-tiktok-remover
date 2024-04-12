import sys

def get_config_params():
    config_params = {
        "outputAllVideos": False,
        "archiveVideos": False,
        "avoidImageRecognition": False, # Currently unused
        "fileTypesToCheckFor": ["mp4"], # Default file type for TikTok videos
        "fileNameLength": 36, # 36 seems to be the length of TikTok video names
        "fileCreatedAfter": 1472688000, # 1472688000 is the timestamp for September 1, 2016
    }

    if "--output-all" in sys.argv:
        config_params["outputAllVideos"] = True
    if "--archive" in sys.argv:
        config_params["archiveVideos"] = True
    if "--avoid-image-recognition" in sys.argv: # Currently unused
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
    if "--file-created-after" in sys.argv:
        index = sys.argv.index("--file-created-after") + 1
        if index < len(sys.argv):
            config_params["fileCreatedAfter"] = int(sys.argv[index])

    return config_params
