# Feed

These files were found on the London stock exchange document site.
Google search query: "ftse100 filetype:csv OR filetype:xls OR filetype:xlsx 2023"
The files are XLSX and contain daily closing prices for FTSE indexes. Each incremental file has newer data. At the time of this writing the latest (2025/03) was inxedex 1217.

The feed.sh script downloads all of them up to 1217. Update the script or directly download the one you want.

# Convert to CSV

In the CSV directory are converted versions of these files to CSV. This was accomplished using python as below:

```
cd csv
python3 -m venv venv
source venv/bin/activate
pip install pandas openpyxl
python3 convert.py
```

# Aggregation

Each file has all the data up till that file's date.To extract a particular index's closing price (e.g. FTSE 100) note that each CSV has 17 lines of headers (various high and lows and their dates, as well as the closing value header). From row 18 onward the closing values are present and the index's columnar value data appears. FTSE 100 for example is the first column of data after the date and timestamp. The last 2 lines of data forms a footer

The trim.sh script removes the header and footer from a file and produces an aggregate.csv file as output.

```
./trim.sh input-file.csv
```

# ETL on FTSE 100 data

Use the etl.py script (it operates on the aggregate.csv file) and provide the column number and the desired filename:

```
./etl.sh 1 ftse100.csv
```

This outputs the desired index's closing values in the output file by cutting the date and selected column value fields from the aggregated source.
