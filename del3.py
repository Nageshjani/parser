import json

# Function to find the longest common prefix among all keys
def find_longest_common_prefix(paths):
    if not paths:
        return ""
    
    # Split the paths into components based on " -> " separator
    split_paths = [path.split(" -> ") for path in paths]
    
    # Find the shortest path to limit the comparison
    shortest_path = min(split_paths, key=len)
    
    longest_common_prefix = []
    
    for i in range(len(shortest_path)):
        # Get the ith component from all paths
        current_component = split_paths[0][i]
        
        # Check if all paths have the same component at this position
        if all(path[i] == current_component for path in split_paths):
            longest_common_prefix.append(current_component)
        else:
            break  # Stop when a difference is found

    # Join the longest common components back into a string
    return " -> ".join(longest_common_prefix) + " -> " if longest_common_prefix else ""

# Function to remove the common prefix from all paths
def remove_common_prefix(paths, common_prefix):
    cleaned_paths = {}
    for key, value in paths.items():
        # If the key starts with the common prefix, remove it
        if key.startswith(common_prefix):
            cleaned_key = key[len(common_prefix):].strip(" -> ")
        else:
            cleaned_key = key
        cleaned_paths[cleaned_key] = value
    return cleaned_paths

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

# Find the longest common prefix across all paths
longest_common_prefix = find_longest_common_prefix(list(path_based_json.keys()))

# Clean up the path-based JSON by removing the longest common prefix
cleaned_path_based_json = remove_common_prefix(path_based_json, longest_common_prefix)

# Save the cleaned path-based JSON to a new file
output_cleaned_path_file = "output_cleaned_path_based_structure_3.json"
with open(output_cleaned_path_file, 'w') as outfile:
    json.dump(cleaned_path_based_json, outfile, indent=4)

# Print the cleaned output JSON to verify
print(json.dumps(cleaned_path_based_json, indent=4))
