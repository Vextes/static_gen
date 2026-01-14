import os, shutil
from textnode import TextNode, TextType

def main():
    setup_dest_dir()

def setup_dest_dir():
    dest_path = './public'
    src_path = './static'
    if (os.path.exists(dest_path)):
        del_contents = os.listdir(dest_path)
        print(f"removing the following from {dest_path}: {del_contents}")
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    copy_static_files(dest_path, src_path)


def copy_static_files(dest_path, src_path):
    copy_contents = os.listdir(src_path)
    for item in copy_contents:
        item_path = os.path.join(src_path, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_path)
        else:
            new_dest_path = os.path.join(dest_path, item)
            os.mkdir(new_dest_path)
            copy_static_files(new_dest_path, item_path)



if __name__=="__main__":
    main()