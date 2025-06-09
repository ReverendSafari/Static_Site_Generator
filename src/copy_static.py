import os
import re
import shutil
from block_md import *

def copy_directory(given_dir, dest_dir):
    #Get files
    file_list = os.listdir(given_dir)

    for file in file_list:
        file_path = os.path.join(given_dir, file)
        dest_path = os.path.join(dest_dir, file)

        if os.path.isfile(file_path):
            shutil.copy(file_path, dest_path)
            continue
        if os.path.isdir(file_path):
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            copy_directory(file_path, dest_path)

def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines: 
        if re.match(r"^\#\s+.+$", line):
            return line.replace("# ", "", 1).strip()
    
    raise ValueError("No Title Found")

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, 'r') as file:
            regular_content = file.read()
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error has occured: {e}")

    try:
        with open(template_path, 'r') as file:
            template_content = file.read()
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error has occured: {e}")

    html_string = markdown_to_html_node(regular_content).to_html()
    title = extract_title(regular_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}" , html_string)
    template_content = template_content.replace("href=\"/", f"href=\"{base_path}")
    template_content = template_content.replace("src=\"/", f"src=\"{base_path}")

    #Make sure directories exist
    directory_path = os.path.dirname(dest_path)
    os.makedirs(directory_path, exist_ok=True)

    #Write content to file
    with open(dest_path, "w") as file:
        file.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    file_list = os.listdir(dir_path_content)

    for file in file_list:
        file_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file.replace(".md", ".html"))

        if os.path.isfile(file_path):
            generate_page(file_path, template_path, dest_path, base_path)
            continue

        if os.path.isdir(file_path):
            generate_pages_recursive(file_path, template_path, dest_path, base_path)
