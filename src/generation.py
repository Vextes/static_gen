import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split('\n'):
        if (line.startswith('# ')):
            return line.split(' ', 1)[1]
    raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as md_file:
        markdown_content = md_file.read()

    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    html_node = markdown_to_html_node(markdown_content)
    html = html_node.to_html()

    title = extract_title(markdown_content)

    replaced_title_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)
    full_html = replaced_title_content.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as to_file:
        to_file.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_list = os.listdir(dir_path_content)
    print(f"filename: {content_list}")
    for item in content_list:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            filename = item.split('.')[0]
            print(f"filename: {filename}")
            generate_page(
                os.path.join(dir_path_content, item),
                template_path,
                os.path.join(dest_dir_path, f"{filename}.html"),
                basepath
            )
        else:
            generate_pages_recursive(
                os.path.join(dir_path_content, item),
                template_path,
                os.path.join(dest_dir_path, item),
                basepath
            )