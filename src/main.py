import shutil
import os
import sys

from generatepagesrecursive import generate_pages_recursive
from copystatic import copy_static

default_base_path = "/"

def main():
    base_path = default_base_path
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    if not base_path.startswith('/'):
        base_path = '/' + base_path
    if not base_path.endswith('/'):
        base_path = base_path + '/'
    # Clear and recreate the docs directory
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.makedirs("docs")
    
    # Copy static files
    copy_static("static", "docs")
    print("Copying static files to public directory...")
    
    # Generate all pages recursively
    generate_pages_recursive("content", "template.html", "docs", base_path)
    print("Generated pages from markdown files...")

main()