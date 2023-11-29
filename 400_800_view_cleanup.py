''' This script will be used as a tool to move XXX and XXX view images inside working folders to designed folders'''

import os
import shutil
import time
from datetime import timedelta
import errno
import re

def get_target_dirs(root_dir):
    return [os.path.join(root_dir, name) for name in ["XXX", "XXX", "XXX"]]

def get_dest_dirs(root_dir):
    return {400: os.path.join(root_dir, "XXX"), 
            800: os.path.join(root_dir, "XXX"),
            810: os.path.join(root_dir, "XXX")}

def move_files(target_dirs, dest_dirs):
    view400_count = 0
    view800_count = 0
    view810_count = 0
    # Iterate through target directories
    for target_dir in target_dirs:
        # Iterate through floorset directories in each target directory
        for floorset in os.listdir(target_dir):
            floorset_dir = os.path.join(target_dir, floorset)
            if os.path.isdir(floorset_dir):
                # Iterate through files in floorset directory
                for filename in os.listdir(floorset_dir):
                    file_path = os.path.join(floorset_dir, filename)
                    # Ensure it's a file, not a subdirectory
                    if os.path.isfile(file_path):
                        # Check if file matches pattern and get the view size (XXX or XXX)
                        if filename.endswith(".jpg"):
                            # print("filename0", filename)
                            parts = re.split(r"_|-", filename)
                            # print("parts", parts)
                            if len(parts) > 1 and parts[1] in ['XXX', 'XXX', 'XXX']:
                                # print("filename", filename)
                                view_size = int(parts[1])
                                # Determine destination directory, create if doesn't exist
                                # print('view_size', view_size)
                                brand = os.path.basename(target_dir)
                                dest_dir = os.path.join(dest_dirs[view_size], brand + '_' + floorset)
                                # print("dest_dir", dest_dir)
                                os.makedirs(dest_dir, exist_ok=True)
                                dest_file = os.path.join(dest_dir, filename) 
                                # Move file
                                if (parts[1] == 'XXX'):
                                    view400_count += 1
                                elif (parts[1] == 'XXX'):
                                    view800_count += 1
                                else:
                                    view810_count += 1
                                shutil.move(file_path, dest_file)
                                print(f"Moved {filename} from {floorset_dir} to {dest_dir}")
    print(f"{view400_count} XXX_view files moved, {view800_count} XXX_view files moved , {view810_count} XXX_view files moved")

def main():
    # Lock file mechanism
    lock_file = "XXX"
    try:
        # Try to create the lock file
        with open(lock_file, 'x') as f:
            pass
    except FileExistsError:
        print("Another instance of the program is running. Exiting.")
        return

    start_time = time.time()
    print(f"Program started at {time.ctime(start_time)}")

    root_dir = "XXX"
    target_dirs = get_target_dirs(root_dir)
    dest_dirs = get_dest_dirs(root_dir)

    move_files(target_dirs, dest_dirs)

    end_time = time.time()
    print(f"Program ended at {time.ctime(end_time)}")
    elapsed_time = timedelta(seconds=end_time - start_time)
    print(f"Total time elapsed: {elapsed_time}")

    # Remove the lock file when done
    os.remove(lock_file)

if __name__ == "__main__":
    main()

