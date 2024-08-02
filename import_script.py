import csv
import json
from collections import defaultdict

def csv_to_json(csv_file_path):
    data = [] # create an empty list
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data # now it's a list of dictionaries

def csv_to_nested_json(csv_file_path):
    root = defaultdict(list)  # Using defaultdict to automatically create lists for new keys
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            conference_name = row.pop('name')  # Remove the 'name' key from the row and get its value
            root[conference_name].append(row)  # Add the row (talk details) under the appropriate conference

    return root



# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'test_info1.csv'
json_data = csv_to_nested_json(csv_file_path) # the function returns a list of dictionaries

# Pretty-print the JSON data
print(json.dumps(json_data, indent=4))

# Optionally, write the JSON data to a file
with open('output.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(json_data, jsonfile, indent=4)
