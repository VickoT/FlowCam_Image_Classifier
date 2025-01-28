#!/bin/bash

# Directory containing the output files
DIRECTORY="/media/local_3/users/viktor/Documents/Classifier/Raw_data/reclassified_2024-10-15"
# Absolute path to re_eval.py script
SCRIPT_PATH="/media/local_3/users/viktor/Documents/Classifier/Classifier_v2/re_eval.py"

# Check if the directory exists
if [ -d "$DIRECTORY" ]; then
    # Loop over the files in the directory
    for SUB_DIR in "$DIRECTORY"/*; do
        if [ -d "$SUB_DIR" ]; then
            BASE_NAME=$(basename "$SUB_DIR")
            # Enter the subdirectory and run re_eval.py
            echo "Entering $SUB_DIR and running re_eval.py"
            (cd "$SUB_DIR" && python3 "$SCRIPT_PATH")
        fi
    done
else
    echo "Directory $DIRECTORY does not exist."
fi
