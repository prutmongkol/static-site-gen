import os
import shutil

from copy_contents import copy_files, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
file_path_template = "./template.html"
dir_path_public = "./public"


def main():
    if os.path.exists(dir_path_public):
        print(f"Removing public directory...")
        shutil.rmtree(dir_path_public)
        
    print("Copying static files to public directory...")
    copy_files(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, file_path_template, dir_path_public)
    

main()
