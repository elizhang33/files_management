'''This script is used to sort files into two different group so that the files uploading process can be easier'''

import os
import glob
import shutil
import time
from datetime import timedelta
import csv


def handle_debut_case(current_dir, image_name):
    view_codes = ['100', '110', '120', '130', 'swatch']
    matches = []
    missing_views = []
    for view_code in view_codes:
        match = glob.glob(os.path.join(current_dir, f"{image_name}*_{view_code}-*"))
        if match:
            matches.append(match[0])
        else:
            missing_views.append(view_code)

    if len(matches) == len(view_codes):
        dest_dir = os.path.join(current_dir, "Debut")
        os.makedirs(dest_dir, exist_ok=True)
        for match in matches:
            #this code will not handle dups in dest
            # shutil.move(match, dest_dir)
            # print(f'Moved: {match} to Debut')

            #following code will overwrite the same file in the dest
            dest_file = os.path.join(dest_dir, os.path.basename(match))
            shutil.copy2(match, dest_file)  # copy file to destination, overwrite if exists
            os.remove(match)  # remove the source file
            print(f'Moved: {match} to {dest_dir}')

    if missing_views:
        print(f'Missing views {missing_views} for article number: {image_name} in Debut')

#The flow case still needs revise to include all situation
def handle_flow_case(current_dir, image_name):
    view_codes = ['000', '100', 'swatch']
    matches = []
    missing_views = []
    for view_code in view_codes:
        match = glob.glob(os.path.join(current_dir, f"{image_name}*_{view_code}-*"))
        if match:
            matches.append(match[0])
        else:
            missing_views.append(view_code)

    if len(matches) >= 2:
        dest_dir = os.path.join(current_dir, "Flow")
        os.makedirs(dest_dir, exist_ok=True)
        for match in matches:
            # No handle with dups in dest
            # shutil.move(match, dest_dir)
            # print(f'Moved: {match} to Flow')

            #following code will overwrite the same file in the dest
            dest_file = os.path.join(dest_dir, os.path.basename(match))
            shutil.copy2(match, dest_file)  # copy file to destination, overwrite if exists
            os.remove(match)  # remove the source file
            print(f'Moved: {match} to {dest_dir}')

    if missing_views:
        print(f'Missing views {missing_views} for article number: {image_name} in Flow')

def handle_flow_alts_case(current_dir, image_name):
    view_codes2 = ['110', '120', '130']
    matches2 = []
   
    for view_code2 in view_codes2:
        match2 = glob.glob(os.path.join(current_dir, f"{image_name}*_{view_code2}-*"))
        if match2:
            matches2.append(match2[0])
   
    dest_dir2 = os.path.join(current_dir, "Flow_Alts")
    os.makedirs(dest_dir2, exist_ok=True)
    for match2 in matches2:
        #following code will overwrite the same file in the dest
        dest_file2 = os.path.join(dest_dir2, os.path.basename(match2))
        shutil.copy2(match2, dest_file2)  # copy file to destination, overwrite if exists
        os.remove(match2)  # remove the source file
        print(f'Moved: {match2} to {dest_dir2}')


def main():

    start_time = time.time()
    print(f"Program started at {time.ctime(start_time)}")

    floorset = input("Which floorset you are looking for? ")
    csv_filename = input("Enter the CSV file name: ")

    current_dir = f"XXX/{floorset}"

    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            task_type = row[0].lower()
            image_name = row[1]
            if task_type == "debut":
                handle_debut_case(current_dir, image_name)
            elif task_type == "flow":
                handle_flow_case(current_dir, image_name)
                handle_flow_alts_case(current_dir, image_name)
            else:
                print(f"Unknown task type {task_type} for article number: {image_name}")

    end_time = time.time()
    print(f"Program ended at {time.ctime(end_time)}")
    elapsed_time = timedelta(seconds=end_time - start_time)
    print(f"Total time elapsed: {elapsed_time}")

if __name__ == '__main__':
    main()