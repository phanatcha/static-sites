import os
from block_markdown import markdown_to_html_node
from htmlnode import *

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# '):
            return stripped[1:].strip()
    raise Exception("no h1 header")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()
    
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    try:
        title = extract_title(markdown_content)
    except Exception as e:
        title = "Untitled"

    final_html = template_content.replace('{{ Title }}', title)
    final_html = final_html.replace('{{ Content }}', html_content)
    
    final_html = final_html.replace('href="/', 'href="/static-sites/')
    final_html = final_html.replace('src="/', 'src="/static-sites/')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w', encoding='utf-8') as output_file:
        output_file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for entry in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        
        if os.path.isdir(content_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(content_path, template_path, dest_path, basepath)
        elif entry.endswith(".md"):
            html_filename = os.path.splitext(entry)[0] + ".html"
            html_dest_path = os.path.join(dest_dir_path, html_filename)
            generate_page(content_path, template_path, html_dest_path, basepath)
