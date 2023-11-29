import os
import re
import csv
import shutil
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Configure logging
logging.basicConfig(filename='process_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

DES_PATH_DELIVERED = ""
DES_PATH_NOTNEEDED = ""


def date_info():
    return datetime.datetime.now().strftime("%m_%d_%Y")


def date_extractor(inputs):
    date_del = re.findall(r'\d{2}_\d{2}_\d{4}', inputs)
    return date_del[0] if date_del else ""


def uploaded_justify(inputs):
    return "Uploaded" in inputs


def do_not_need_justify(inputs):
    return "Do" in inputs


def date_justify(inputs):
    return bool(re.findall(r'\d{2}_\d{2}_\d{4}', inputs))


def move_file(src, des):
    shutil.move(src, des)


def file_in_csv(csv_path):
    existing_filenames = set()
    if os.path.isfile(csv_path):
        with open(csv_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            existing_filenames = {row[1] for row in reader if len(row) > 1}
    return existing_filenames


def dir_traverse(user_input, start_dir, csv_files_path):
	upload_count = 0
	notNeed_count = 0
	
	for root, dirs, files in os.walk(start_dir, topdown = True):
		for d in dirs:
			if date_justify(d):
				# construct full source path
				src_path = os.path.join(root, d)
				if uploaded_justify(src_path):
					date_del = date_extractor(src_path)
					
					# get list of files in source folder
					files = os.listdir(src_path)

					if len(files) > 0 and date_del == user_input:
						temp = src_path.replace("./", "").replace("/!", "/").replace("!", "")
						root_parts = re.split(r',|/',  temp) 
						floorset = "_".join(root_parts[5:7])
						floorset_temp = floorset.replace('-', '_').replace('–', '_').replace('—', '_')
							
						full_name = floorset_temp + "_" + date_del 

						csv_path = os.path.join(csv_files_path, (full_name + ".csv"))
						file_exists = os.path.isfile(csv_path)
						
						# create a set which has all filename that already be collected
						existing_filenames = file_in_csv(csv_path)
						
						with open(csv_path, 'a', newline = '') as csvfile1:
							writer = csv.writer(csvfile1)

							if not file_exists:	
								writer.writerow(['Brand and Floorset', 'File name', 'Straub Number', 'Article Number', 'View Code', 'Date Delivered'])

							for file in files:
								straub_number = file.split("_")[0]
								article_number = file[:9]
								view_code = re.split(r'_|-', file)[1]
								src_path1 = os.path.join(src_path, file)
								des_path1 = os.path.join(DES_PATH_DELIVERED, file)
								# check if the filename is in CSV file already
								if file in existing_filenames:
									move_file(src_path1, des_path1)
									print(floorset, 'file moved: ', file)
									upload_count += 1
									continue
									
								else:
									writer.writerow([floorset, file, straub_number, article_number, view_code, date_del])
									move_file(src_path1, des_path1)
									upload_count += 1
									print(floorset, 'file moved: ', file)
									print(floorset, " file inserted:", file)
					else:
						continue

			elif do_not_need_justify(d):
				src_path_notneed = os.path.join(root, d)
				
				# get list of files in source folder
				files = os.listdir(src_path_notneed)

				if len(files) > 0:
					temp = src_path_notneed.replace("./", "").replace("/!", "/").replace("!", "")
					root_parts = re.split(r',|/',  temp) 
					floorset = "_".join(root_parts[:2])
					
					for file in files:
						if len(files) > 0 and ((file.endswith('.jpg') or file.endswith( '.gif')) and len(file) > 9):
							src_path2 = os.path.join(src_path_notneed, file)
							des_path2 = os.path.join(DES_PATH_NOTNEEDED, file)
							move_file(src_path2, des_path2)
							notNeed_count += 1
							print(file, " is moved to", des_path2)

	return upload_count, notNeed_count


def yesterday_date():
    current_weekday = datetime.now().weekday()  # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
    days_to_subtract = 3 if current_weekday == 0 else 1  # If today is Monday, go back to Friday, else go back one day.
    
    yesterday = datetime.now() - timedelta(days=days_to_subtract)
    return yesterday.strftime("%m_%d_%Y")


def main():
    processed_yesterday = False  # Flag to check if yesterday's folder was processed

    while True:
        current_datetime = datetime.now()
        current_time = current_datetime.time()
        current_weekday = current_datetime.weekday()  # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday

        if current_weekday in range(0, 5) and current_time >= time(9, 0) and current_time <= time(16, 0):

            # If it's a new day and yesterday's folder was not processed yet, process it first
            if not processed_yesterday:
                logging.info("Checking for files from yesterday's folder...")

                yesterday_date_str = yesterday_date()
                upload_count, notNeed_count = dir_traverse(yesterday_date_str, start_dir, csv_files_path)
                logging.info(f"Processed {upload_count} files from yesterday's folder to [a]_UpdateSF_Delivered.")
                logging.info(f"Processed {notNeed_count} files from yesterday's folder to [a]_UpdateSF_NotNeeded.")

                processed_yesterday = True  # Set flag to True so this block doesn't run again today
            
            try:
                start_time = time.time()

                logging.info("Filename collection and moving process started...")

                user_input = date_info()
                start_dir = "/Volumes/Chicos-SF/5_Delivery/_Delivery_In_Process_ATG"
                csv_files_path = '/Volumes/Chicos-SF/5_Delivery/_Delivery_In_Process_ATG/_python_script/csv_files'
                
                upload_count, notNeed_count = dir_traverse(user_input, start_dir, csv_files_path)
                
                logging.info(f"{upload_count} files moved to [a]_UpdateSF_Delivered.")
                logging.info(f"{notNeed_count} files moved to [a]_UpdateSF_NotNeeded.")
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                logging.info(f"Elapsed time: {elapsed_time} seconds")
                time.sleep(1800)  # Sleep for 30 minutes

            except Exception as e:
                logging.error(f"An error occurred: {e}")
                current_time = datetime.now().time()
                end_time = time(16, 0)
                time_to_end = datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), current_time)
                
                if time_to_end < timedelta(minutes=10):
                    logging.info("Near the end of the operating hours. Will resume operation tomorrow.")
                    break
                else:
                    logging.info("Sleeping for 10 minutes before retrying.")
                    time.sleep(600)  # Sleep for 10 minutes
        else:
            processed_yesterday = False  # Reset the flag for the new day
            logging.info("Outside of operating hours. Sleeping until next operating day/hour.")
            time.sleep(3600)  # Sleep for 1 hour and check again

if __name__ == "__main__":
    main()



'''Script Description:
This script is designed to automate the process of moving files located in specific folders to two distinct automation folders. It operates on weekdays between 9am and 4pm and logs all significant events and errors.

Key Features:
Scheduled Operation: The script runs on weekdays between 9am to 4pm.
File Movement: Files are moved from source folders to two target folders, [a]_UpdateSF_Delivered and [a]_UpdateSF_NotNeeded, based on certain conditions.
CSV File Logging: A CSV file is generated to log filenames that are moved. The CSV file includes details like brand, floorset, Straub number, article number, view code, and the date delivered.
Error Handling: If the script encounters an error, it logs the error and attempts to restart in 10 minutes. If the program is interrupted close to the end of its scheduled time (4pm), it will terminate and resume the next day.
Daily Check: At the start of each new day, the script checks and processes files from yesterday's folder, if any.
Logging: All events, errors, and other useful information are logged to process_log.log.
How It Works:
The script performs the following steps in its main loop:

Checks whether the current time is within its scheduled operation window.
If it's the start of a new day, it first processes files from yesterday's folder.
Executes the main file moving and logging routine for the current day.
Sleeps for 30 minutes before running the loop again.
The script uses Python's built-in os, csv, logging, datetime, and shutil libraries for its operations.'''
