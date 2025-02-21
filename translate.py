#!/usr/bin/python3
import argparse
import deepl
import json
import os
import time

deeplAuth_key  = ''
language       = 'EN-US'

def translate(text):
    translator = deepl.Translator(deeplAuth_key)
    result = translator.translate_text(text , target_lang=language)
    print(result.text)
    return result.text

def process_json_file(input_path):
    # Load JSON data
    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Process each item
    for item in data:
        if 'message' in item:
            original_message = item['message']
            if original_message != '':
                processed_message = translate(original_message)
            else:
                processed_message = original_message
            item['message'] = processed_message
    
    # Save modified data
    with open(base_filename+'_en.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translating a JSON transcript')
    parser.add_argument('file', help='The file to translate.')
    args = parser.parse_args()
    process_json_file(args.file)
