#!/usr/bin/python3
import os
import json
import re
import argparse

# Regex pattern to match Bitcoin addresses (P2PKH, P2SH, Bech32)
BTC_ADDRESS_REGEX = r'\b(?:bc1|[13])[a-km-zA-HJ-NP-Z0-9]{25,39}\b'

def extract_bitcoin_addresses(text):
    """Extracts Bitcoin addresses from a given text using regex."""
    if not text:
        return set()  # Return an empty set
    return set(re.findall(BTC_ADDRESS_REGEX, text))  # Use set to remove duplicates

def extract_date(timestamp):
    """Extracts the date (YYYY-MM-DD) from a timestamp formatted as 'YYYY-MM-DD HH:MM:SS'."""
    if isinstance(timestamp, str) and len(timestamp) >= 10:
        return timestamp[:10]  # Extract only the 'YYYY-MM-DD' part
    return "Unknown Date"

def process_json_files(input_folder, output_file):
    """Processes all JSON files in the given folder, extracting Bitcoin addresses, sender aliases, and dates."""
    results = []

    # Ensure the folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist.")
        return

    # Iterate over JSON files in the folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Ensure data is a list of messages
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            message = item.get("message", "")
                            sender_alias = item.get("sender_alias", "Unknown")
                            timestamp = item.get("timestamp", "")

                            # Extract Bitcoin addresses
                            btc_addresses = extract_bitcoin_addresses(message)
                            date = extract_date(timestamp)

                            # Store results if any Bitcoin address is found
                            for btc_address in btc_addresses:
                                results.append((sender_alias, btc_address, date))

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    # Save results to Markdown
    if results:
        # Sort by date for better readability
        results.sort(key=lambda x: x[2])  

        with open(output_file, "w", encoding="utf-8") as mdfile:
            mdfile.write("# Extracted Bitcoin Addresses\n\n")
            mdfile.write("| Sender Alias | Bitcoin Address | Date |\n")
            mdfile.write("|-------------|----------------|------|\n")

            for sender, address, date in results:
                mdfile.write(f"| {sender} | `{address}` | {date} |\n")

        print(f"Extraction complete. Data saved to {output_file}")
    else:
        print("No Bitcoin addresses found in the dataset.")

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Extract Bitcoin addresses from JSON files and save as Markdown.")
    parser.add_argument("input_folder", type=str, help="Path to the folder containing JSON files")
    parser.add_argument("output_file", type=str, help="Path to the output Markdown file")

    args = parser.parse_args()
    
    # Run processing
    process_json_files(args.input_folder, args.output_file+".md")
