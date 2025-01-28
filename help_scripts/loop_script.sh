#!/bin/bash

# Directory containing the files
DIRECTORY="../Raw_data/reclassified2"

# Check if the directory exists
if [ -d "$DIRECTORY" ]; then
    # Loop over the files in the directory
    for SUB_DIR in "$DIRECTORY"/*; do
        if [ -d "$SUB_DIR" ]; then
		BASE_NAME=$(basename "$SUB_DIR")
		# Check that the dir not starts with "Output_"
		if [[ ! $BASE_NAME == Output2_* ]]; then
			python main.py -raw_dir $SUB_DIR
		fi
        fi
    done
else
    echo "Directory $DIRECTORY does not exist."
fi
