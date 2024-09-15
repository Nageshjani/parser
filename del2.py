import json

def extract_paths(node, current_path=""):
    paths = {}

    # Iterate through the current node's keys
    for key, value in node.items():
        # Skip over keys that store text values
        if key == "_text":
            # Store the text value with the current path as the key
            paths[current_path.strip(" -> ")] = value
        elif isinstance(value, dict):
            # If the value is a dictionary, recurse and build the path
            new_path = current_path + f"{key} -> "
            paths.update(extract_paths(value, new_path))
        elif isinstance(value, list):
            # Handle lists of dictionaries (e.g., multiple child elements with the same tag)
            for index, item in enumerate(value):
                new_path = current_path + f"{key}[{index}] -> "
                paths.update(extract_paths(item, new_path))

    return paths

# Load the hierarchical JSON structure from the previously created file
with open('output_hierarchical_structure.json', 'r') as json_file:
    hierarchical_json = json.load(json_file)

# Extract paths and text content from the hierarchical JSON
path_based_json = extract_paths(hierarchical_json)

# Save the path-based JSON to a new file
output_path_file = "output_path_based_structure.json"
with open(output_path_file, 'w') as outfile:
    json.dump(path_based_json, outfile, indent=4)

# Print the output JSON to verify
print(json.dumps(path_based_json, indent=4))
