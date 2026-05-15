from utilities import markdown_to_blocks 

def extract_title(markdown):
    
    blocks = markdown_to_blocks(markdown)
    h1 = ""

    level = 0
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()

    raise ValueError("No H1 header found") 

def generate_page(from_path, template_path, dest_path):
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

def generate_page_recursive(content_directory_path, template_path, destination_directory_path):
    pass 


