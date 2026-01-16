import os
from copystatic import setup_dest_dir, copy_static_files
from generation import generate_page, generate_pages_recursive


dest_path = './public'
src_path = './static'
content_path = './content'
template_path = './template.html'

def main():
    print(f"deleting public directory")
    setup_dest_dir(src_path, dest_path)

    print(f"copying static files")
    copy_static_files(dest_path, src_path)

    print(f"generating pages")

    generate_pages_recursive(content_path, template_path, dest_path)


if __name__=="__main__":
    main()