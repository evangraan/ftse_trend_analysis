#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_csv_file>"
    exit 1
fi

INPUT_FILE="$1"
AGGREGATE_FILE="aggregate.csv"
> "$AGGREGATE_FILE"

if [ -f "$INPUT_FILE" ]; then
    echo "Processing: $INPUT_FILE"

    TMP_FILE=$(mktemp)
    grep -v '^[[:space:]]*$' "$INPUT_FILE" > "$TMP_FILE"

    TOTAL_LINES=$(wc -l < "$TMP_FILE")
    START_LINE=18
    END_LINE=$((TOTAL_LINES - 2))

    if [ "$END_LINE" -ge "$START_LINE" ]; then
        sed -n "${START_LINE},${END_LINE}p" "$TMP_FILE" >> "$AGGREGATE_FILE"
    else
        echo "Skipping $INPUT_FILE: Not enough data lines"
    fi

    rm "$TMP_FILE"
else
    echo "File not found: $INPUT_FILE"
    exit 1
fi

sort -t',' -k2 aggregate.csv -o aggregate.csv
