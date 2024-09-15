from html.parser import HTMLParser
import json

class HierarchicalTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []  # Stack to keep track of open tags
        self.json_structure = {}  # Final JSON structure
        self.current_node = self.json_structure  # Pointer to the current node in the structure
        self.current_text = ''  # To hold the text temporarily
        self.in_ignored_tag = False  # Flag to ignore script/style content

    def handle_starttag(self, tag, attrs):
        # Ignore <script> and <style> tags and their content
        if tag in ['script', 'style']:
            self.in_ignored_tag = True
            return

        # When a new tag is encountered, create a new node (dictionary)
        new_node = {}
        # Push the current tag to the stack
        self.tag_stack.append((tag, new_node))
        # If there's text collected before the tag, add it as text content of the current node
        if self.current_text.strip():
            self.current_node["_text"] = self.current_text.strip()
        # Now, point the current node to the new node created
        if isinstance(self.current_node, dict):
            # If current node is a dict, assign the new node as a child
            if tag in self.current_node:
                if isinstance(self.current_node[tag], list):
                    self.current_node[tag].append(new_node)
                else:
                    self.current_node[tag] = [self.current_node[tag], new_node]
            else:
                self.current_node[tag] = new_node
        # Reset current text buffer
        self.current_text = ''
        # Update the pointer to the new node
        self.current_node = new_node

    def handle_endtag(self, tag):
        # If we are inside a <script> or <style>, exit it when the tag ends
        if tag in ['script', 'style']:
            self.in_ignored_tag = False
            return

        # When closing a tag, we move back to the parent node
        if self.current_text.strip():
            self.current_node["_text"] = self.current_text.strip()
        # Pop the last tag from the stack and reset the current node to its parent
        if self.tag_stack:
            self.tag_stack.pop()
        # Reset text buffer
        self.current_text = ''
        # Reset current node pointer to the last open tag's node
        if self.tag_stack:
            self.current_node = self.tag_stack[-1][1]
        else:
            self.current_node = self.json_structure  # Back to root

    def handle_data(self, data):
        # Collect text data, but ignore if inside <script> or <style>
        if not self.in_ignored_tag:
            self.current_text += data

# Sample HTML input
with open('data.json') as json_file:
    data = json.load(json_file)
    html_content = data['results'][0]['content']

# Initialize and feed the hierarchical text parser with the HTML content
hierarchical_text_parser = HierarchicalTextParser()
hierarchical_text_parser.feed(html_content)




# Save the hierarchical JSON structure to a .json file
output_file_path = "output_hierarchical_structure.json"
with open(output_file_path, 'w') as json_file:
    json.dump(hierarchical_text_parser.json_structure, json_file, indent=4)

