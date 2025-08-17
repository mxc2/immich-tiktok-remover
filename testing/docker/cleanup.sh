#!/bin/bash

cd tmp && docker compose down # Take down Immich
cd .. && docker compose down # Take down ITR

rm -r tmp # Remove immich directory