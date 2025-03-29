#!/bin/bash

# Usage: ./etl.sh input.csv 1 output.csv
# This will extract the date/time and the first data column (which is column 3 in the CSV)

INPUT_FILE="$1"
DATA_COLUMN_INDEX="$2"
OUTPUT_FILE="$3"

if [[ -z "$INPUT_FILE" || -z "$DATA_COLUMN_INDEX" || -z "$OUTPUT_FILE" ]]; then
    echo "Usage: $0 input.csv column_number output.csv"
    exit 1
fi

# The actual data column in the CSV is offset by +2 (due to leading comma and date/timestamp)
CSV_COLUMN_INDEX=$((DATA_COLUMN_INDEX + 2))

# Read the file line-by-line, skipping empty lines and printing date/timestamp and selected column
awk -F',' -v col="$CSV_COLUMN_INDEX" '
    NF > col { 
        # remove time portion if needed: split($2, dt, " "); print dt[1], $col
        print $2 "," $col
    }
' "$INPUT_FILE" > $OUTPUT_FILE

