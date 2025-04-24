def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            return title
    raise Exception("No header found.")