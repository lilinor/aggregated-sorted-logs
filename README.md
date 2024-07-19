# Aggregate timelined logs from different files
A python script that scans several log files and sorts the logs by its timestamp in a single file for better debugging

### Timestamps format supported :
- YYY-MM-DDTHH:MM:SSZ
- YYYY-MM-DDTHH:MM:SS.mmmZ
- YYYY-MM-DD HH:MM:SS.mmm
- MM-DD HH:MM:SS.mmm (Current year is used) 

For other timestamps, you can add your own regexp in the ```extract_timestamp``` function and change the code accordingly.

## Prerequisites

Python min. version : 3.9

Have all the logs in one folder and copy the ```generate_sorted_logs.py``` in this folder.
You can test with the logs example provided in the [dataset_example folder](https://github.com/lilinor/aggregated-sorted-logs/tree/main/dataset_example).

## Usage

Run 

### Without parameters

```bash 
python aggregated-sorted-logs.py
````
It will scan all the logs and aggregate all the logs sorted by time in a single file ```aggregated_logs.log``` in the ```output``` folder.

### With parameters (optional)

- `-p` : Only extract the logs with a specific string pattern. Every string pattern is separated by a space if you have more than one string to filter.
- `-o` : Name the output file

For example (using the logs in the dataset folder) 

```bash
python generate_sorted_logs.py -p pattern1 pattern2  -o aggregated_logs_pattern1_2.log
````

It will scan all the logs, select the lines containing `pattern1` or `pattern2` and aggregate all the logs sorted by time in a single file `aggregated_logs_pattern1_2.log` in the output folder.

### Contributing

Pull requests are welcome.

