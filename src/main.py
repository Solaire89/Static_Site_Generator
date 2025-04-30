import shutil
import os

from generatepage import generate_page
from copystatic import copy_static

def main():
    copy_static("static", "public")
    print("Copying static files to public directory...")
    # This part should still be in your code somewhere
    generate_page("content/index.md", "template.html", "public/index.html")

    # Now handle all markdown files
    for root, dirs, files in os.walk("content"):
        # Get the full path to the markdown file
        for file in files:
            if file.endswith(".md"):
                markdown_path = os.path.join(root, file) # Not using dirname because we want to join the file to the directory

                # Calculate the corresponding HTML output path
                # Replace 'content' with 'public' and '.md' with '.html'
                relative_path = os.path.relpath(markdown_path)
                html_path = os.path.join("public", os.path.splitext(relative_path)[0] + ".html")
                

                # Ensure the directory exists
                os.makedirs(os.path.dirname(html_path), exist_ok=True)

                # Generate the page
                generate_page(markdown_path, "template.html", html_path)
                print(f"Generate {html_path} from {markdown_path}")
main()