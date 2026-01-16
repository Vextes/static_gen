import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split('\n'):
        if (line.startswith('# ')):
            return line.split(' ', 1)[1]
    raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as md_file:
        markdown_content = md_file.read()

    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    html_node = markdown_to_html_node(markdown_content)
    html = html_node.to_html()
    #print(f"farthest: {html}")

    title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as to_file:
        to_file.write(full_html)