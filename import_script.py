import csv
import json

def csv_to_json(csv_file_path):
    data = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'test_info1.csv'
json_data = csv_to_json(csv_file_path)

# Pretty-print the JSON data
print(json.dumps(json_data, indent=4))

# Optionally, write the JSON data to a file
with open('output.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(json_data, jsonfile, indent=4)
