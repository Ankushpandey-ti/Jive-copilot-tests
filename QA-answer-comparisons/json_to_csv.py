import json
import csv


def json_to_csv(json_file_path, csv_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            # Write the header using the keys from the first JSON object
            writer.writerow(data[0].keys())

            # Write the data rows
            for item in data:
                writer.writerow(item.values())

        print("Conversion from JSON to CSV completed successfully.")
    except IOError:
        print("An error occurred while converting JSON to CSV.")


# Example usage
## FILENAME SHOULD BE WITHOUT EXTENSION (FILE TYPE)
FILENAME = './question_search_phrase_sources'
json_file_path = f'{FILENAME}.json'
csv_file_path = f'{FILENAME}.csv'

json_to_csv(json_file_path, csv_file_path)
