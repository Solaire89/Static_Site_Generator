import os
from markdowntohtmlnode import markdown_to_html_node
from extracttitle import extract_title

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    # Get all entries in the content directory
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        # Create full path for current entry
        entry_path = os.path.join(dir_path_content, entry)
        
        # If entry is a file
        if os.path.isfile(entry_path):
            # If entry is a markdown file
            if entry_path.endswith(".md"):
                # Read markdown content
                with open(entry_path, 'r') as f:
                    markdown_content = f.read()
                
                # Convert to HTML node
                html_node = markdown_to_html_node(markdown_content)
                
                # Calculate destination path
                rel_path = os.path.relpath(entry_path, start=dir_path_content)
                base_name, _ = os.path.splitext(rel_path)
                html_file = base_name + ".html"
                dest_file_path = os.path.join(dest_dir_path, html_file)
                
                # Generate HTML using template
                # (This is where you'd use your existing generate_page logic)
                with open(template_path, 'r') as f:
                    template = f.read()
                
                # Extracting the title
                title = extract_title(markdown_content)
                # You'd need to replace a placeholder in the template with the HTML content
                final_html = (template.replace("{{ Title }}", title)
                              .replace("{{ Content }}", html_node.to_html()))

                # Right before you do path replacements
                print(f"Before replacements: {'href=\"/index.css\"' in content}")
                print(f"Base path being used: {base_path}")

                # Your path replacement code here
                content = (content.replace('href="/', 'href="' + base_path)
                              .replace('src="/', 'src="' + base_path))

                # After replacements
                print(f"After replacements: {'href=\"/index.css\"' in content}")
                print(f"New content contains: {'href=\"' + base_path + 'index.css\"' in content}")
                # Create directories if they don't exist
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                
                # Write to destination file
                with open(dest_file_path, 'w') as f:
                    f.write(final_html)
                
        # If entry is a directory, recurse into it
        elif os.path.isdir(entry_path):
            # Create corresponding directory in destination if it doesn't exist
            sub_dest_dir = os.path.join(dest_dir_path, entry)
            if not os.path.exists(sub_dest_dir):
                os.makedirs(sub_dest_dir)
            
            # Recurse into subdirectory
            generate_pages_recursive(entry_path, template_path, sub_dest_dir, base_path)