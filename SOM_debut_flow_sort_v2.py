import os
import glob
import shutil
import time
import csv
from datetime import timedelta

def handle_case(current_dir, image_name, view_codes, dest_folder):
    matches = []
    missing_views = []
    for view_code in view_codes:
        pattern = os.path.join(current_dir, f"{image_name}*_{view_code}-*")
        match = glob.glob(pattern)
        if match:
            matches.append(match[0])
        else:
            missing_views.append(view_code)

    if (len(matches) == len(view_codes) or dest_folder == "Flow") and len(matches) >= 2:
        dest_dir = os.path.join(current_dir, dest_folder)
        os.makedirs(dest_dir, exist_ok=True)
        for match in matches:
            dest_file = os.path.join(dest_dir, os.path.basename(match))
            shutil.move(match, dest_file)  # Move file to destination, overwrite if exists
            print(f'Moved: {match} to {dest_dir}')

    if missing_views:
        print(f'Missing views {missing_views} for article number: {image_name} in {dest_folder}')

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
                handle_case(current_dir, image_name, ['100', '110', '120', '130', 'swatch'], "Debut")
            elif task_type == "flow":
                handle_case(current_dir, image_name, ['000', '100', 'swatch'], "Flow")
                handle_case(current_dir, image_name, ['110', '120', '130'], "Flow_Alts")
            else:
                print(f"Unknown task type {task_type} for article number: {image_name}")

    end_time = time.time()
    print(f"Program ended at {time.ctime(end_time)}")
    elapsed_time = timedelta(seconds=end_time - start_time)
    print(f"Total time elapsed: {elapsed_time}")

if __name__ == '__main__':
    main()
