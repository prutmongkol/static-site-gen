import os
import shutil

from copy_contents import copy_files, generate_page

dir_path_static = "./static"
dir_path_public = "./public"
file_path_content = "./content/index.md"
file_path_template = "./template.html"
file_path_public = "./public/index.html"


def main():
    if os.path.exists(dir_path_public):
        print(f"Removing public directory...")
        shutil.rmtree(dir_path_public)
        
    print("Copying static files to public directory...")
    copy_files(dir_path_static, dir_path_public)

    generate_page(file_path_content, file_path_template, file_path_public)
    

main()
