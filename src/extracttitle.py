def extract_title(markdown):
    if not "#" in markdown[0]:
        raise Exception("No # detected")
    else:
        title = markdown.strip("# ")
    return title