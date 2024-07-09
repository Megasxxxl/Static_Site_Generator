from markdown_blocks import markdown_to_html_node, extract_title
from copy_files_func import copy_files
import os
import shutil
import htmlnode
from pathlib import Path

public_dir = "./public"
static_dir = "./static"

def main(): 
    print("Deleting public directory")
    if os.path.exists(public_dir):    
        shutil.rmtree(public_dir)

    print("Copying files from static to public directory")
    copy_files(static_dir, public_dir)
    create_page_recursive('content', 'template.html', 'public')


def create_page(from_path, template_path, dest_path):
    print(f"Generate page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as file:
        content_from_path = file.read()
        
    with open(template_path, "r") as file:
        content_template_path = file.read()
        
    markdown_converter = markdown_to_html_node(content_from_path)
    title = extract_title(content_from_path)
    html_string = ""

    for node in markdown_converter.children:
        html_string += node.to_html()

    content_template_path = content_template_path.replace("{{ Title }}", title)
    content_template_path = content_template_path.replace("{{ Content }}", html_string)
    dest_directory = os.path.dirname(dest_path)

    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    print(dest_path)
    with open(dest_path, "w") as file:
        file.write(content_template_path)
        file.close

def create_page_recursive(dir_path_content, template_path, dest_dir_path):
    dir_path_content = Path(dir_path_content)
    template_path = Path(template_path)
    dest_dir_path = Path(dest_dir_path)
    files = os.listdir(dir_path_content)

    for file in files:
        formatted_path_dir = os.path.join(dir_path_content, file)
        
        
        if not os.path.isfile(formatted_path_dir):
            formatted_dest_dir = os.path.join(dest_dir_path, file)
            create_page_recursive(formatted_path_dir, template_path, formatted_dest_dir)

        if file.endswith(".md"):
            formatted_dest_dir = os.path.join(dest_dir_path, file.replace(".md", ".html"))
            create_page(formatted_path_dir, template_path, formatted_dest_dir)

if __name__ == "__main__":
    main()