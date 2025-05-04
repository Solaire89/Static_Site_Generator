import shutil
import os

from generatepagesrecursive import generate_pages_recursive
from copystatic import copy_static

def main():
    # Clear and recreate the public directory
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public")
    
    # Copy static files
    copy_static("static", "public")
    print("Copying static files to public directory...")
    
    # Generate all pages recursively
    generate_pages_recursive("content", "template.html", "public")
    print("Generated pages from markdown files...")

main()