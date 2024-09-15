import json

# Function to remove a specific prefix from the keys
def remove_specific_prefix(paths, specific_prefix):
    cleaned_paths = {}
    for key, value in paths.items():
        # If the key starts with the specific prefix, remove it
        if key.startswith(specific_prefix):
            cleaned_key = key[len(specific_prefix):].strip(" -> ")
        else:
            cleaned_key = key
        cleaned_paths[cleaned_key] = value
    return cleaned_paths

# Load the previously created JSON file
with open('output_trimmed_path_based_structure.json', 'r') as json_file:
    path_based_json = json.load(json_file)

# Define the specific prefix you want to remove
specific_prefix = """
ul -> li -> div -> div -> ul -> li -> div -> li -> div -> div[2] -> section -> div -> div -> div -> div -> div -> section -> 
"""

# Clean up the path-based JSON by removing the specific prefix
cleaned_path_based_json = remove_specific_prefix(path_based_json, specific_prefix)

# Save the cleaned path-based JSON to a new file
output_cleaned_path_file = "output_trimmed_path_based_structure_1.json"
with open(output_cleaned_path_file, 'w') as outfile:
    json.dump(cleaned_path_based_json, outfile, indent=4)

# Print the cleaned output JSON to verify
print(json.dumps(cleaned_path_based_json, indent=4))
