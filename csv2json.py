import csv
import json
import argparse


def csv_to_json(input_file, output_file):
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        field_names = next(reader)  # Read the first row as field names
        data = [row for row in reader]

    json_data = []
    for row in data:
        item = {}
        for i, field in enumerate(field_names):
            item[field] = row[i]
        json_data.append(item)

    with open(output_file, 'w') as jsonfile:
        json.dump(json_data, jsonfile, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert CSV to JSON')
    parser.add_argument('-f', '--input-file',
                        required=True, help='Input CSV file')
    parser.add_argument('-o', '--output-file',
                        required=True, help='Output JSON file')

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    csv_to_json(input_file, output_file)
