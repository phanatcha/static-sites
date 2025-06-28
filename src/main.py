import os
import shutil
import sys
from copystatic import copy_files_recursive
from generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"  # Changed from public to docs
template_path = "./template.html"
dir_path_content = "./content"

def main():
    # Get basepath from CLI args or default to /
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    print("Deleting docs directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages from markdown files...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

    print("Build complete!")

if __name__ == "__main__":
    main()