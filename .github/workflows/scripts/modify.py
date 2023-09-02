import json
import argparse

def add_source_key(input_path, output_path, source_value):
    with open(input_path, 'r') as infile:
        data = json.load(infile)

    for item in data:
        if "revid" in item:
            del item["revid"]
        if "url" in item:
            del item["url"]
        
        item["source"] = source_value

    with open(output_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add source key to JSON objects')
    parser.add_argument('--input', required=True, help='Path to input JSON file')
    parser.add_argument('--output', required=True, help='Path to output JSON file')
    parser.add_argument('--source', required=True, help='Value for the source key')

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    source_value = args.source

    add_source_key(input_path, output_path, source_value)
