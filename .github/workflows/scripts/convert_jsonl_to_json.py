import json
import argparse

def convert_json_lines_to_json(input_path, output_path):
    with open(input_path, 'r') as infile:
        lines = infile.readlines()

    json_objects = [json.loads(line.strip()) for line in lines]

    json_array = json.dumps(json_objects, indent=4)

    with open(output_path, 'w') as outfile:
        outfile.write(json_array)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JSON Lines to JSON')
    parser.add_argument('--input', required=True, help='Path to input JSON Lines file')
    parser.add_argument('--output', required=True, help='Path to output JSON file')

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    convert_json_lines_to_json(input_path, output_path)
