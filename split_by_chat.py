#!/usr/bin/python3
import json
import os
import re

def sanitize_filename(filename):
    # Replace characters that are invalid in filenames with underscores.
    return re.sub(r'[\\/:"*?<>|]+', '_', filename)

def split_json_by_chat_id(input_file, output_dir):
    # Load the JSON data.
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Group objects by their chat_id.
    groups = {}
    for obj in data:
        chat_id = obj.get('chat_id')
        if chat_id:
            groups.setdefault(chat_id, []).append(obj)
        else:
            print("Warning: An object without a 'chat_id' field was skipped.")
    
    # Create the output directory if it doesn't exist.
    os.makedirs(output_dir, exist_ok=True)
    
    # Write each group to its own JSON file.
    for chat_id, items in groups.items():
        filename = sanitize_filename(chat_id) + '.json'
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2)
        print(f"Created file: {filepath}")

def main():
    input_file = 'bestflowers_clean.json'         # Your input JSON file.
    output_dir = 'split_by_chat_id'     # Directory to store the output JSON files.
    split_json_by_chat_id(input_file, output_dir)

if __name__ == '__main__':
    main()
