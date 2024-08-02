import csv
import json

def csv_to_nested_json(csv_file_path):
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = {}
        for row in reader:
            current_level = data
            for key in row:
                if row[key] != '':
                    if key not in current_level:
                        current_level[key] = {}
                    current_level = current_level[key]
            current_level.update(row)
    return data

# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'your_file.csv'
nested_json = csv_to_nested_json(csv_file_path)

# Pretty-print the JSON data
print(json.dumps(nested_json, indent=4))

# Optionally, write the JSON data to a file
with open('output.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(nested_json, jsonfile, indent=4)
