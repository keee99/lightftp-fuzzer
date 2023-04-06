import os
import json
import pandas as pd

# Set the folder path
folder_path = '../../new/output'

# Get a list of all files in the folder
all_files = os.listdir(folder_path)

# Filter out the JSON files
json_files = [f for f in all_files if f.endswith('.json')]

total_time = 0
total_inputs = 0

# Loop through the JSON files and run your script for each file
for file_name in json_files:
    # Open the JSON file
    with open(os.path.join(folder_path, file_name)) as f:
        # Load the JSON data
        data = json.loads(f.read())
        df = pd.json_normalize(data, max_level=3)
        if (df.index.stop >= 100):
            size = len(data)
            total_inputs += size

            time_taken = data[-1]['time'] - data[0]['time']
            total_time += time_taken

            average_time_taken = time_taken/size
            print("average time taken with", size, "inputs ran:", average_time_taken)
            f.close()

print("\n")
average_time = total_time/total_inputs
print("Overall average time for", total_inputs, "inputs:", average_time)