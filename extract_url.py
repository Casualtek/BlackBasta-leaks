#!/usr/bin/python3
import os
import json
import re
import argparse

# Updated regex pattern to match standard URLs and .onion URLs
URL_REGEX = r'\b(?:https?://[^\s<>|`"]+|[a-zA-Z0-9-]+\.onion(?:/[^\s<>|`"]*)?)'

def extract_urls(text):
    """Extracts all URLs from a given text using regex, cleans them, and splits by '|' if needed."""
    if not text:
        return set()
    
    urls = re.findall(URL_REGEX, text)
    cleaned_urls = set()
    
    for url in urls:
        url = url.replace("`", "")  # Remove backticks
        split_urls = url.split("|")  # Split URLs by '|'
        cleaned_urls.update(split_urls)  # Add all split parts
    
    return cleaned_urls

def extract_date(timestamp):
    """Extracts the date (YYYY-MM-DD) from a timestamp formatted as 'YYYY-MM-DD HH:MM:SS'."""
    return timestamp[:10] if isinstance(timestamp, str) and len(timestamp) >= 10 else "Unknown Date"

def process_json_files(input_folder, output_file, output_format="md"):
    """Processes all JSON files in the given folder, extracting URLs, sender aliases, and dates."""
    results = []
    seen_urls = set()  # Track unique URLs
    file_count = 0
    url_count = 0

    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist.")
        return

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)
            file_count += 1

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            message = item.get("message", "")
                            sender_alias = item.get("sender_alias", "Unknown")
                            timestamp = item.get("timestamp", "")

                            urls = extract_urls(message)
                            date = extract_date(timestamp)

                            for url in urls:
                                url = url.strip()  # Ensure no leading/trailing spaces
                                if url and url not in seen_urls:  # Keep only first occurrence
                                    seen_urls.add(url)
                                    results.append((sender_alias, url, date))
                                    url_count += 1

            except json.JSONDecodeError:
                print(f"Error: Invalid JSON format in file {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    if results:
        results.sort(key=lambda x: x[2])  

        if output_format == "md":
            save_as_markdown(results, output_file)
        elif output_format == "csv":
            save_as_csv(results, output_file)
        else:
            print(f"Error: Unsupported output format '{output_format}'")

        print(f"Extraction complete: {file_count} files processed, {url_count} unique URLs found. Data saved to {output_file}")

    else:
        print("No URLs found in the dataset.")

def save_as_markdown(results, output_file):
    """Saves extracted results in Markdown format."""
    with open(output_file, "w", encoding="utf-8") as mdfile:
        mdfile.write("# Extracted Unique URLs\n\n")
        mdfile.write("| Sender Alias | URL | Date |\n")
        mdfile.write("|-------------|-----|------|\n")

        for sender, url, date in results:
            mdfile.write(f"| {sender} | `{url}` | {date} |\n")

def save_as_csv(results, output_file):
    """Saves extracted results in CSV format."""
    import csv
    with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Sender Alias", "URL", "Date"])
        writer.writerows(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract unique URLs (including .onion) from JSON files and save in Markdown or CSV format.")
    parser.add_argument("input_folder", type=str, help="Path to the folder containing JSON files")
    parser.add_argument("output_file", type=str, help="Path to the output file (without extension)")
    parser.add_argument("--format", type=str, choices=["md", "csv"], default="md", help="Output format (md or csv)")

    args = parser.parse_args()
    process_json_files(args.input_folder, args.output_file + "." + args.format, args.format)
