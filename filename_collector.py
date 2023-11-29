'''This is just a simple filename collector to collect the file names from 7_Delivered directory and does not \
consider the duplicated file names'''

import os
import csv

root_dir = 'XXX'
csv_dir = 'XXX'

def is_target_folder(folder_name):
    return '-' in folder_name and 'ATG' in folder_name and 'NOT UPLOADED' not in folder_name

def is_target_file(file_name):
    return file_name.endswith('.jpg') or file_name.endswith('.gif')

def collect_files(root_dir):
    floorset_dict = {}
    for root, dirs, files in os.walk(root_dir):
        path = root.split(os.sep)
        if is_target_folder(path[-1]):
            floorset_name = path[-2]
            if floorset_name not in floorset_dict:
                floorset_dict[floorset_name] = []
            print(f"Processing floorset: {floorset_name}")
            for file in files:
                if is_target_file(file):
                    print(f"Collecting file: {file}")
                    floorset_dict[floorset_name].append(file)
    return floorset_dict

def write_to_csv(floorset_dict):
    for floorset_name_orig, file_list in floorset_dict.items():
        floorset_name = floorset_name_orig.replace('-', '_').replace('–', '_').replace('—', '_')
        csv_file_path = os.path.join(csv_dir, f"{floorset_name}.csv")
        if os.path.exists(csv_file_path):
            with open(csv_file_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                existing_files = list(reader)
            file_list = [file for file in file_list if file not in existing_files]
        with open(csv_file_path, 'a') as csvfile:
            writer = csv.writer(csvfile)
            for file in file_list:
                print(f"Writing file: {file} to CSV")
                writer.writerow([file])

def main():
    floorset_dict = collect_files(root_dir)
    write_to_csv(floorset_dict)

if __name__ == "__main__":
    main()
