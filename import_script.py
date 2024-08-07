import csv
import json
import pandas as pd


def csv_to_nested_json(csv_file_path):
    df = pd.read_csv(csv_file_path)

    all_series = {} # create an empty dictionary 

    # TODO: make fixed information dynamic
    # TODO: handle img urls in own object
    # TODO: handle video upload urls in own object 
    # make these dynamic later


    organisation_id = 119463
    visibility = 'open'
    owner_id = 1
    series_type = 'symposium'
    organisers = [ # the static organiser information
        {'user_id': 1, 'credited_organiser': False},
        {'user_id': 36670, 'credited_organiser': True},
        {'user_id': 36752, 'credited_organiser': True},
    ]


    for index, row in df.iterrows(): # loops through all rows in the CSV file
        if row['series_name'] not in all_series: # if series_name not already in dict...
            # all_series[row['series_name']] = { 'description': 'There will be a description here soon', 'events': [] }

            all_series[row['series_name']] = {'events': [] }


        series = all_series[row['series_name']]

        series['name'] = row['series_name']
        series['owner_id'] = owner_id
        series['type'] = series_type
        series['description'] = row['description']
        series['organisers'] = organisers
        series['organisation_id'] = organisation_id
        series['visibility'] = visibility

        series['events'].append({
            'start': row['start'],
            'end': row['end'],
            'timezone': row['event_timezone'],
            'status': row['status'],
            'talks': [
                {
                    'title': row['talk_title'],
                    'abstract': row['abstract'],
                    'speakers': [{

                        'email': row['email'],
                        'record_meta': [{
                            'title': row['speaker_title'],
                            'name': row['speaker_name'],
                            'homepage_url': row['homepage_url'],
                            'department': row['department'],
                            'position': row['position'],
                            'affiliations': [
                                row['affiliations']
                            ]
                        }],
                        'record_image_file': {
                            'url': row['_url']
                        }

                    }],
                }
            ],

        })

    output = {
        'event_series': list(all_series.values())
    }

    return output



# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'input.csv'
json_data = csv_to_nested_json(csv_file_path) # 

# Pretty-print the JSON data
print(json.dumps(json_data, indent=4))

# Optionally, write the JSON data to a file
with open('output.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(json_data, jsonfile, indent=4)
