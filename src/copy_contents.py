import os
import shutil


def copy_contents(src, dst):
    ls = os.listdir(src)
    
    if not os.path.exists(dst):
        os.mkdir(dst)
    
    for item in ls:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            print(f'Copying: {src_path} -> {dst_path}')
            shutil.copy(src_path, dst_path)
        else:
            copy_contents(src_path, dst_path)