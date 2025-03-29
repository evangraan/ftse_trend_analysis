#!/bin/bash

base_url="https://docs.londonstockexchange.com/sites/default/files/reports/FTSE%20Index%20values_"

for i in $(seq 0 1217); do
    filename="FTSE%20Index%20values_${i}.xlsx"
    if [ -f "$filename" ]; then
        echo "Skipping (already exists): $filename"
    else
        url="${base_url}${i}.xlsx"

        echo "Downloading: $filename"
        curl -O "$url"
        sleep 2
    fi
done

