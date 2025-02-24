#python3
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import random

# Load the JSON data
file_path = "chat_activity.json"  # Update with the correct file path if needed
with open(file_path, "r") as file:
    data = json.load(file)

# Extract sender_id, first_seen, and last_seen
activity_data = []
for sender_id, details in data.items():
    first_seen = datetime.datetime.strptime(details["first_seen"], "%Y-%m-%d %H:%M:%S")
    last_seen = datetime.datetime.strptime(details["last_seen"], "%Y-%m-%d %H:%M:%S")
    activity_data.append((sender_id, first_seen, last_seen))

# Convert to DataFrame
df = pd.DataFrame(activity_data, columns=["Sender ID", "First Seen", "Last Seen"])

# Convert first_seen and last_seen to months for a clearer time axis
df["First Seen Month"] = df["First Seen"].dt.to_period("M")
df["Last Seen Month"] = df["Last Seen"].dt.to_period("M")

# Convert periods to datetime for plotting
df["First Seen Month"] = df["First Seen Month"].dt.to_timestamp()
df["Last Seen Month"] = df["Last Seen Month"].dt.to_timestamp()

# Sort by first seen time (earliest first)
df = df.sort_values(by="First Seen Month")

# Generate random colors for each sender (except the highlighted one)
unique_senders = df["Sender ID"].unique()
color_map = {sender: (random.random(), random.random(), random.random()) for sender in unique_senders}
color_map["@usernamessd"] = "red"  # Highlighting specific sender

# Plot horizontal bar graph with colors
fig, ax = plt.subplots(figsize=(12, 10))
for index, row in df.iterrows():
    ax.barh(row["Sender ID"], (row["Last Seen Month"] - row["First Seen Month"]).days, 
            left=row["First Seen Month"], color=color_map[row["Sender ID"]])

# Format and label the graph
ax.set_xlabel("Months")
ax.set_ylabel("Sender ID")
ax.set_title("Activity Time Frame of Each Sender (Sorted by First Seen)")
ax.grid(axis="x", linestyle="--", alpha=0.7)

# Show the plot
plt.show()
