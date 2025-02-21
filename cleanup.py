#!/usr/bin/python3
import json

def parse_object(lines):
    """
    Given a list of lines corresponding to a single object (including the outer { and }),
    parse each key-value pair. Keys are expected to be the text before the first colon.
    Values are trimmed and treated as strings. If a value starts with triple backticks,
    we accumulate lines until the closing triple backticks.
    """
    result = {}
    in_code_block = False
    current_key = None
    current_value_lines = []

    # Process each line except the first and last (which are the braces).
    for line in lines:
        stripped = line.strip()
        if stripped == "{" or stripped == "}":
            continue

        if in_code_block:
            # Append the current line to the current value.
            current_value_lines.append(line.rstrip("\n"))
            # If we see closing triple backticks, end code block.
            if "```" in line:
                in_code_block = False
                # Join the accumulated code block lines, preserving newlines.
                value = "\n".join(current_value_lines)
                result[current_key] = value
                current_key = None
                current_value_lines = []
            continue

        # Look for a colon to separate key from value.
        if ":" in line:
            # Split on the first colon.
            key_part, value_part = line.split(":", 1)
            key = key_part.strip()
            # Remove a trailing comma from the value, if any.
            value = value_part.strip().rstrip(",")
            if value.startswith("```"):
                # Begin a code block value.
                in_code_block = True
                current_key = key
                current_value_lines = [value]
            else:
                result[key] = value
        else:
            # If there is no colon and we are not in a code block, assume it's a continuation
            # of the previous value (this might not be needed if your file is well-behaved).
            if current_key is not None:
                current_value_lines.append(line.rstrip("\n"))
    # In case the file ends while still in a code block.
    if current_key is not None and current_value_lines:
        result[current_key] = "\n".join(current_value_lines)
    return result

def split_into_objects(file_content):
    """
    Splits the file content into a list of objects.
    We assume each object is wrapped between a line starting with '{' and a line starting with '}'.
    """
    lines = file_content.splitlines()
    objects = []
    current_obj = []
    in_object = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("{") and not in_object:
            in_object = True
            current_obj = [line]
        elif in_object:
            current_obj.append(line)
            if stripped.startswith("}"):
                objects.append(current_obj)
                in_object = False
                current_obj = []
    return objects

def main():
    input_file = 'bestflowers.json'    # Replace with your file name.
    output_file = 'bestflowers_clean.json'  # Output file for the valid JSON.

    # Read the entire file content.
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split the content into object blocks.
    objects_lines = split_into_objects(content)
    parsed_objects = []
    for obj_lines in objects_lines:
        parsed = parse_object(obj_lines)
        # Ensure all keys and values are strings.
        parsed = {str(k): str(v) for k, v in parsed.items()}
        parsed_objects.append(parsed)

    # Write the list of objects to a JSON file.
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_objects, f, indent=2)

    print(f"Successfully created valid JSON in {output_file}")

if __name__ == '__main__':
    main()
