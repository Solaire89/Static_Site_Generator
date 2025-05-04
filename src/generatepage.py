import os
from markdowntohtmlnode import markdown_to_html_node
from extracttitle import extract_title

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Storing the contents of the from_path to the read_from variable
    with open(from_path, 'r') as file:
        read_from = file.read()
    # Storing the contents of the template_path to the read_template variable
    with open(template_path, 'r') as template:
        read_template = template.read()
    created_html_node = markdown_to_html_node(read_from).to_html()
    title = extract_title(read_from)
    modified_template = (read_template
                         .replace("{{ Title }}", title)
                         .replace("{{ Content }}", created_html_node))
    # Add debug statements here:
    print(f"Original template contained: <link href=\"/index.css\"")
    print(f"Modified template contains: {modified_template}")
    print(f"Base path being used: {base_path}")
          
    modified_template = (read_template
                         .replace('href="/', 'href="' + base_path)
                         .replace('src="/', 'src="' + base_path))

    print(f"After replacements: {modified_template}")
    # Write the content to the dest_path
    dir_path = os.path.dirname(dest_path)
    if dir_path:  # If there is a directory component
        os.makedirs(dir_path, exist_ok=True) # Make the directory, and we don't care if the directory exists already
    
    # After replacing placeholders in the template
    with open(dest_path, 'w') as dest_file:
        dest_file.write(modified_template)  # Write the modified template to the file