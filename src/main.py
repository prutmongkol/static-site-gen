import os
import shutil

from copy_contents import copy_contents

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    if os.path.exists(dir_path_public):
        print(f"Removing public directory...")
        shutil.rmtree(dir_path_public)
        
    print("Copying static files to public directory...")
    copy_contents(dir_path_static, dir_path_public)


main()
