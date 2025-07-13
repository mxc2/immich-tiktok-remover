#!/bin/bash

while true
do 
    python3 immich_tiktok_remover.py --output-all ${OUTPUT_ALL} --archive ${ARCHIVE} --search-archived ${SEARCH_ARCHIVED} --file-types ${FILE_TYPES} --file-name-length ${FILE_NAME_LENGTH} --file-name-is-not-alumn ${FILE_NAME_IS_NOT_ALUMN} --file-created-after ${FILE_CREATED_AFTER} --text-to-check ${TEXT_TO_CHECK} --avoid-image-recognition ${AVOID_IMAGE_RECOGNITION}
    sleep $RESTART_TIMEOUT
done