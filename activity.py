#python3
import json
import pandas as pd

# Define the log file path
log_file = "bestflowers_clean.json"  # Change this to your actual file path
output_file = "chat_activity.json"

# Read and parse the file
with open(log_file, 'r') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert timestamp column to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S")

# Grouping data by sender_alias
summary = {}
print("Processing sender data...")
for sender, group in df.groupby("sender_alias"):
    summary[sender] = {
        "first_seen": str(group["timestamp"].min()),
        "last_seen": str(group["timestamp"].max()),
        "chat_ids": list(group["chat_id"].unique()),
        "monthly_message_counts": {str(k.date()): v for k, v in group.set_index("timestamp").resample("ME").size().items()}
    }

print("Sender data processing completed.")

# Write output to a JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4)

print(f"Data has been saved to {output_file}")

