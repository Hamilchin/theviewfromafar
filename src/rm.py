import os

root_dir = "../poems"  # Change this

for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
    if not dirnames:  # No subdirectories
        html_files = [f for f in filenames if f.endswith('.html')]
        if html_files and len(html_files) == len(filenames):
            for f in html_files:
                print("s.path.join(dirpath, f)")
                #os.remove(os.path.join(dirpath, f))  # Delete each .html file
            os.rmdir(dirpath)  # Now remove the empty directory
            print(f"Deleted dir: {dirpath}")