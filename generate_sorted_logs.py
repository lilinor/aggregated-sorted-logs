import glob
import re
import os
import argparse
from datetime import datetime

# Parse arguments passed at the run of the script
def parse_arguments ():
    parser = argparse.ArgumentParser(description='Filter and sort log files based on a specified pattern')
    parser.add_argument('--search-patterns', '-p', nargs='+', type=str, help='Patterns to search in log lines')
    parser.add_argument('--output-file', '-o', type=str, default='aggregated_logs.log', help='Output file name for sorted logs')
    return parser.parse_args()

# Extracts timestamp from a line of a log
def extract_timestamp(log_line):

    #get current year
    year = datetime.now().year

    # Regex for "MM-DD HH:MM:SS.mmm"
    match = re.search(r'\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}', log_line)
    if match:
        timestamp_str = match.group()
        return datetime.strptime(f"{year}-" + timestamp_str, '%Y-%m-%d %H:%M:%S.%f')

    # Regex for "YYYY-MM-DDTHH:MM:SSZ" or "YYYY-MM-DDTHH:MM:SS.mmmZ" or "MM-DD HH:MM:SS.mmm"
    match = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?(?:Z)?', log_line)
    if match:
        timestamp_str = match.group()
        # Remove the 'Z' at the end if present
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1]
        if '.' in timestamp_str:
            return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')
        else:
            return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')

#Creates the complete output file path for the aggregated logs - Will create an output directory if different search patterns need to be stored at the same place
#Returns its complete path
def create_output_file (output_file_name):

    # Get current path
    log_dir = os.getcwd()
    
    # Checks if the output directory exists otherwise creates it
    output_directory =  os.getcwd() + "/output"
    print(f"Sorted logs are generated in {output_directory}")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Gets the absolute output file path
    return os.path.join(output_directory, output_file_name)

args = parse_arguments()
    
search_patterns = args.search_patterns
# Read all log files
scanned_log_files = glob.glob(os.getcwd()+ '/*.log')
log_entries = []

for log_file in scanned_log_files:
    print(f"Reading log file: {log_file}")  # Displays the scanned log files
    with open(log_file, 'r') as file:
        for line in file:
            if not search_patterns or any(pattern in line for pattern in search_patterns): #handles if there's no need to filter the logs
                timestamp = extract_timestamp(line)
                if timestamp:
                    log_entries.append((timestamp, line))

# Sort logs by timestamps
sorted_logs = sorted(log_entries, key=lambda x: x[0])

output_file_path = create_output_file(args.output_file)

with open(output_file_path, 'w') as output_file:
    for entry in sorted_logs:
        output_file.write(entry[1])

if search_patterns:
    print(f"All sorted logs matching '{search_patterns}' are written in {output_file_path}")
else: 
    print(f"All sorted logs are written in {output_file_path}")
