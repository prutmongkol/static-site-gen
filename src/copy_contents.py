import os
import shutil


from markdown_blocks import markdown_to_html_node


def copy_files(src, dst):
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
            copy_files(src_path, dst_path)
            

def extract_title(markdown):
    first_line = markdown.readline()
    if first_line[0:2] != "# ":
        raise ValueError("First line must be h1 header (# )")
    return first_line[2:]


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    template = None
    with open(template_path) as f:
        template = f.read()
    
    markdown = open(from_path)
    title = extract_title(markdown)
    content = markdown.read()
    markdown.close()
    
    content_html = markdown_to_html_node(content).to_html()
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content_html)
    
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    
    with open(dest_path, 'w') as f:
        f.write(template)
