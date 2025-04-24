import os, shutil

# Writing a function that copies the source directory and pastes the content to a new directory
def copy_static(source_dir, dest_dir):
    # Clear destination directory if it exists
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)


    # Create destination directory
    os.mkdir(dest_dir)

    # Go through each item in the source directory
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

         # If it's a file, copy it
        if os.path.isfile(source_path):
            shutil.copyfile(source_path, dest_path)
            print(f"Copied file: {source_path} to {dest_path}")
         # If it's a directory, recursively copy it
        else:
            copy_static(source_path, dest_path)