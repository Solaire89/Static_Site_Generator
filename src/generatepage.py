from markdowntohtmlnode import markdown_to_html_node
from extracttitle import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    read_from = from_path.read()
    read_template = template_path.read()
    html_node = markdown_to_html_node(read_from).to_html()
    title = extract_title(read_from)