import os
import csv
import shutil
import time
from time import strftime, localtime
import datetime

def read_filenames_from_csv(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        return [row[1] for row in reader if row]

def find_and_move_images(filenames, working_directory):
    target_folder = os.path.join(working_directory, 'Target Files')
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    for file in os.listdir(working_directory):
        full_file_path = os.path.join(working_directory, file)
        if os.path.isfile(full_file_path) and file.endswith(('.gif', '.jpg')):
            for filename in filenames:
                if filename in file:
                    shutil.move(full_file_path, os.path.join(target_folder, file))
                    print(f"{file} has been moved to {target_folder}")
                    break

def main():
    csv_file = input("Please enter the full path to the CSV file (including its extension): ")
    if not os.path.exists(csv_file):
        print("The CSV file does not exist.")
        return
    
    working_directory = input("Please enter the full path to the working directory: ")
    if not os.path.exists(working_directory):
        print("The working directory does not exist.")
        return
    
    start_time = time.time()
    print("start_time", strftime('%Y-%m-%d %H:%M:%S', localtime(start_time)))

    filenames = read_filenames_from_csv(csv_file)
    find_and_move_images(filenames, working_directory)

    end_time = time.time()

    print("end_time", strftime('%Y-%m-%d %H:%M:%S', localtime(end_time)))

    elapsed_time = end_time - start_time

    print(f"Elapsed time: {elapsed_time} seconds")

if __name__ == '__main__':
    main()
