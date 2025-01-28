
#!/bin/bash

# Directory containing the report subdirectories
OUTPUT_DIRECTORY="../Output"
# Output file to store the extracted lines
EXTRACTED_FILE="../extracted_lines.txt"

# Empty the output file if it already exists
> "$EXTRACTED_FILE"

# Check if the directory exists
if [ -d "$OUTPUT_DIRECTORY" ]; then
    # Loop over the subdirectories in the output directory
    for SUB_DIR in "$OUTPUT_DIRECTORY"/*; do
        if [ -d "$SUB_DIR" ]; then
            # Loop over the report files in the subdirectory
            for REPORT_FILE in "$SUB_DIR"/*; do
                if [ -f "$REPORT_FILE" ]; then
                    # Extract the last line of the file
                    LAST_LINE=$(tail -n 1 "$REPORT_FILE")
                    # Append the last line to the output file
                    echo "$LAST_LINE" >> "$EXTRACTED_FILE"
                fi
            done
        fi
    done
    echo "Extraction complete. All lines have been saved to $EXTRACTED_FILE."
else
    echo "Directory $OUTPUT_DIRECTORY does not exist."
fi
