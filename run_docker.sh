#!/bin/bash

while true
do
    ARGS=()

    # Boolean flags
    [ "${OUTPUT_ALL,,}" = "true" ] && ARGS+=(--output-all)
    [ "${ARCHIVE,,}" = "true" ] && ARGS+=(--archive)
    [ "${SEARCH_ARCHIVED,,}" = "true" ] && ARGS+=(--search-archived)
    [ "${FILE_NAME_IS_NOT_ALUMN,,}" = "true" ] && ARGS+=(--file-name-is-not-alumn)
    [ "${AVOID_IMAGE_RECOGNITION,,}" = "true" ] && ARGS+=(--avoid-image-recognition)
    [ "${CHECK_FOR_IMAGES,,}" = "true" ] && ARGS+=(--check-images)

    # Value arguments
    [ -n "$FILE_TYPES" ] && ARGS+=(--file-types "$FILE_TYPES")
    [ -n "$FILE_NAME_LENGTH" ] && ARGS+=(--file-name-length "$FILE_NAME_LENGTH")
    [ -n "$FILE_CREATED_AFTER" ] && ARGS+=(--file-created-after "$FILE_CREATED_AFTER")
    [ -n "$TEXT_TO_CHECK" ] && ARGS+=(--text-to-check "$TEXT_TO_CHECK")

    python3 immich_tiktok_remover.py "${ARGS[@]}"

    sleep "${RESTART_TIMEOUT:-3600}"
done