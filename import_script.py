import csv
import json
import pandas as pd

def replace_blanks(row):
    return {k: v if v != 'unknown' else None for k, v in row.items()}

def clean_json(data):
    """
    Recursively removes keys with empty lists, empty dictionaries, None, null values,
    lists that only contain an empty dictionary, or dictionaries that only contain an empty list
    from a JSON object.
    
    :param data: The JSON object (dict) or list to clean.
    :return: The cleaned JSON object.
    """
    if isinstance(data, dict):
        # Recursively clean the dictionary
        cleaned_dict = {}
        for k, v in data.items():
            cleaned_value = clean_json(v)
            if isinstance(cleaned_value, dict) and not cleaned_value:
                # Remove if it's an empty dict
                continue
            elif isinstance(cleaned_value, list) and (not cleaned_value or cleaned_value == [{}]):
                # Remove if it's an empty list or a list with an empty dict
                continue
            elif cleaned_value == []:
                # Remove if it's an empty list
                continue
            elif cleaned_value is not None:
                cleaned_dict[k] = cleaned_value
        return cleaned_dict
    elif isinstance(data, list):
        # Recursively clean the list
        cleaned_list = [clean_json(item) for item in data if item not in ([], {}, None)]
        if cleaned_list == [{}] or cleaned_list == [{}] * len(cleaned_list):
            return []  # Remove list if it only contains empty dictionaries
        return cleaned_list
    else:
        # Return the value itself if it's not a list or dict
        return data

def csv_to_nested_json(csv_file_path):
    df = pd.read_csv(csv_file_path)

    all_series = {} # create an empty dictionary 
    all_img_urls = [] 
    all_import_urls = []

    # static organiser information
    series_organisers = [ 
        {'user_id': 1, 'credited_organiser': False},
        {'user_id': 36670, 'credited_organiser': True},
        {'user_id': 36752, 'credited_organiser': True},
    ]

    for index, unclean_row in df.iterrows(): # loops through all row in the CSV file
        row = replace_blanks(unclean_row) # replaces all blank cells with empty string
        if row['series_name'] not in all_series: # if series_name not already in dict...

            all_series[row['series_name']] = {'events': [] }

        series = all_series[row['series_name']] # so this sets series to MVIF.1, MVIF.2, etc, for the following lines of code

        series['name'] = row['series_name']
        series['owner_id'] = row['owner_id']
        series['type'] = row['type']
        series['series_organisers'] = series_organisers        
        series['description'] = row['description']
        series['visibility'] = row['visibility']
        series['organisation_id'] = row['organisation_id']
        # series['organisation_id'] = 1

        series['events'].append({
            'start': row['start'],
            'end': row['end'],
            'timezone': row['event_timezone'],
            'status': row['status'],
            'import_url': row['import_url'],
            'talks': [
            {
                'title': row['talk_title'],
                'abstract': row['abstract'],
                'references': 
                [
                    {
                    'type': row['reference_type'],
                    'value': row['reference_value'],
                    'featured': row['reference_featured']   
                    }
                    
                ],
                'speakers': [{

                'email': row['email'],
                'record_meta': {
                    'title': row['speaker_title'],
                    'name': row['speaker_name'],
                    'homepage_url': row['homepage_url'],
                    'biography': row['biography'],
                    'department': row['department'],
                    'position': row['position'],
                    'affiliations': [row['affiliations']]
                },
                'record_image_file': {
                    '_url': row['_url']
                }

                }],
            }
            ] if any(row.values()) else None,

        })

        all_img_urls.append({"_url": row['_url']})
        all_import_urls.append({"video_url": row['import_url'], 'event_import_url': row['import_url']})

    output = {
        'event_series': list(all_series.values()),
        'files': all_img_urls,
        'video_import_jobs': all_import_urls
    }

    output = clean_json(output)

    return output

# so this is returning each MVIF separately but sequentially

# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'MVIF 1-5'
json_data = csv_to_nested_json(csv_file_path + '.csv') # this is where it actually becomes json data

# Pretty-print the JSON data
print(json.dumps(json_data, indent=4))

# Optionally, write the JSON data to a file
with open(csv_file_path + '.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(json_data, jsonfile, indent=4)