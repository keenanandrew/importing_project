import csv
import json
import pandas as pd


def csv_to_nested_json(csv_file_path):
    df = pd.read_csv(csv_file_path)

    all_series = {}

    organisers = [
        {'user_id': 1, 'credited_organiser': False},
        {'user_id': 36670, 'credited_organiser': True},
        {'user_id': 36752, 'credited_organiser': True},
    ]

    organisation_id = 119463
    visibility = 'open'
    owner_id = 1
    series_type = 'symposium'

    for index, row in df.iterrows():
        if row['series_name'] not in all_series:
            all_series[row['series_name']] = { 'description': 'There will be a description here soon', 'events': [] }

        series = all_series[row['series_name']]

        series['name'] = row['series_name']
        series['owner_id'] = owner_id
        series['type'] = series_type
        series['description'] = row['description']
        series['organisers'] = organisers,

        series['events'].append({
            'start': row['event_start'],
            'end': row['event_end'],
            'timezone': row['event_timezone'],
            'status': row['event_status'],
            'talks': [
                {
                    'title': row['talk_title'],
                    'abstract': row['talk_abstract'],
                    'speakers': [{
                        'name': row['speaker_name'],
                        'email': row['speaker_email'],

                    }],
                }
            ],
            'organisers': organisers,
            'organisation_id': organisation_id,
            'visibility': visibility
        })

    output = {
        'event_series': list(all_series.values())
    }

    return output



# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'file_for_import1.csv'
json_data = csv_to_nested_json(csv_file_path) # 

# Pretty-print the JSON data
print(json.dumps(json_data, indent=4))

# Optionally, write the JSON data to a file
with open('output.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(json_data, jsonfile, indent=4)
