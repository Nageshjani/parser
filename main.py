from html.parser import HTMLParser
import json

class HierarchicalTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_hierarchy = []
        self.indent_level = 0
        self.in_script_or_style = False
        self.text_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'span', 'a', 'strong']  # Tags of interest

    def handle_starttag(self, tag, attrs):
        # Ignore script and style tags
        if tag in ['script', 'style']:
            self.in_script_or_style = True
        # Add hierarchy for the text-relevant tags
        elif tag in self.text_tags:
            self.indent_level += 1

    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.in_script_or_style = False
        elif tag in self.text_tags:
            self.indent_level -= 1

    def handle_data(self, data):
        # Append the text content, formatted with proper indentation
        if not self.in_script_or_style and data.strip():
            #indent = '  ' * self.indent_level  # Two spaces per level
            self.text_hierarchy.append(f"{data.strip()}")

# Load the HTML content from the JSON file
with open('data.json') as json_file:
    data = json.load(json_file)
    html_content = data['results'][0]['content']

# Initialize and feed the hierarchical text parser with the HTML content
hierarchical_text_parser = HierarchicalTextParser()
hierarchical_text_parser.feed(html_content)

# Join the extracted hierarchical text into a single string
hierarchical_text_output = '\n'.join(hierarchical_text_parser.text_hierarchy)

# Save the hierarchical text output to a file
output_hierarchical_text_file_path = 'hierarchical_text_content_1   .txt'

with open(output_hierarchical_text_file_path, 'w') as outfile:
    outfile.write(hierarchical_text_output)
