import shutil
import os

from generatepage import generate_page
from copystatic import copy_static

def main():
    copy_static("static", "public")
    print("Copying static files to public directory...")
    # Generate a page from `content/index.md` using `template.html` and write it to `public/index.html`
    generate_page("content/index.md", "template.html", "public/index.html")

main()