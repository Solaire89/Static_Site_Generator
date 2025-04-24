from copystatic import copy_static

def main():
    copy_static("static", "public")
    print("Copying static files to public directory...")

main()