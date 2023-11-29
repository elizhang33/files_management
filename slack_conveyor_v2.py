'''This script is used to collect file names that will be moved to the two automation folders.
It will save the names into csv files. 
Specifically, it traverses all directories of the 3 brands and looks for files in the 
Uploaded folder and Do Not Need folder and do the work on them repectively.
 '''

import os
import re
import datetime
from pathlib import Path
import xlsxwriter
from dateutil.parser import parse
import datefinder 
import shutil
import multiprocessing
import time
import csv
from time import strftime, localtime
import logging
from slack_sdk import WebClient

# Slack API token and channel ID
slack_token = "XXX"
channel_id = "XXX"

# Initialize Slack client
slack_client = WebClient(token=slack_token)

LOCK_FILE = "XXX"


DES_PATH_DELIVERED = "XXX"

DES_PATH_NOTNEEDED = "XXX"


#get today's date info in the format of MM_DD_YYYY
def date_info():
	current_day = datetime.date.today()

	today_date = datetime.date.strftime(current_day, "%m/%d/%Y")

	date_in_file_name_format = datetime.date.strftime(current_day, "%m_%d_%Y")

	return date_in_file_name_format 


#Extract the date info in the path, re.findall returns a list
def date_extractor(in_puts):
	date_del = re.findall(r'\d{2}_\d{2}_\d{4}', in_puts)

	if len(date_del) != 0:

		return date_del[0]
	else:
		return ""


#Justify if a file is uploaded
def uploaded_justify(in_puts):
	if "Assets_Delivered" in in_puts:
		return True
	return False

def do_not_need_justify(in_puts):
	if "Do" in in_puts:
		return True
	return False

def date_justify(in_puts):
	date_del = re.findall(r'\d{2}_\d{2}_\d{4}', in_puts)
	if len(date_del) > 0:
		if date_del[0] != "":
			return True
	return False


def move_file(src, des):
	
	shutil.move(src, des)


def file_in_csv(csv_path):

	existing_filenames = set()  # Set to store existing filenames

	if os.path.isfile(csv_path):
	    # Read existing filenames from the CSV file
	    with open(csv_path, 'r') as csvfile:
	        reader = csv.reader(csvfile)
	        next(reader)  # Skip the header row
	        for row in reader:
	            if len(row) > 1:
	            	existing_filenames.add(row[1])  #filename is in the second column (index 1)

	return existing_filenames


#Traverse all directories to collect the image names and insert the info into the sheet
def dir_traverse(user_input, start_dir, csv_files_path):
	upload_count = 0
	notNeed_count = 0
	
	for root, dirs, files in os.walk(start_dir, topdown = True):
		for d in dirs:
			if date_justify(d):
				  # construct full source path
				src_path = os.path.join(root, d)
				# print('src_path', src_path)
				if uploaded_justify(src_path):
					date_del = date_extractor(src_path)
					
					# get list of files in source folder
					files = os.listdir(src_path)

					if len(files) > 0 and date_del == user_input:
						# row = 1
						temp = src_path.replace("./", "").replace("/!", "/").replace("!", "")
						root_parts = re.split(r',|/',  temp) 
						floorset = "_".join(root_parts[5:7])
						floorset_temp = floorset.replace('-', '_').replace('–', '_').replace('—', '_')
						# if len(files) > 0:
							
						full_name = floorset_temp + "_" + date_del 

						csv_path = os.path.join(csv_files_path, (full_name + ".csv"))
						file_exists = os.path.isfile(csv_path)
						
						# create a set which has all filename that already be collected
						existing_filenames = file_in_csv(csv_path)
						
						with open(csv_path, 'a', newline = '') as csvfile1:
							writer = csv.writer(csvfile1)

							if not file_exists:
									
								writer.writerow(['Brand and Floorset', 'File name', 'Straub Number', 'Article Number', 'View Code', 'Date Delivered'])
							
							# print("src_path", src_path)
							# print("files", files)
							for file in files:

								straub_number = file.split("_")[0]
								article_number = file[:9]

								view_code = re.split(r'_|-', file)[1]
								# print("file", file)

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


def move_old_csv_files(csv_files_path):
    # Get today's date
    today = datetime.date.today()
    
    # Define the directory where old files would be moved
    old_files_dir = os.path.join(csv_files_path, 'old_files')
    
    # If the directory doesn't exist, create it
    if not os.path.exists(old_files_dir):
        os.makedirs(old_files_dir)
        
    # Iterate over all files in the csv_files_path
    for filename in os.listdir(csv_files_path):
        if filename.endswith(".csv"):
            # Extract the date from the filename
            try:
                date_str = re.search(r'(\d{2}_\d{2}_\d{4})\.csv$', filename).group(1)
                file_date = datetime.datetime.strptime(date_str, '%m_%d_%Y').date()
                
                # If the file_date is older than today, move the file to old_files_dir
                if file_date < today:
                    src = os.path.join(csv_files_path, filename)
                    dest = os.path.join(old_files_dir, filename)
                    shutil.move(src, dest)
                    print(f"Moved old CSV file: {filename} to old_files directory.")
                
            except (AttributeError, ValueError) as e:
                print(f"Error processing filename {filename}: {str(e)}")

						
def check_lock():
    return os.path.exists(LOCK_FILE)

def acquire_lock():
    with open(LOCK_FILE, "w") as f:
        f.write("Locked")

def release_lock():
    os.remove(LOCK_FILE)

def main():
    if check_lock():
        print("Script is currently in use by someone else.")
        return

    acquire_lock()

    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='slack_conveyor.log', filemode='a')

    try:
        start_time = time.time()
        print("start_time", strftime('%Y-%m-%d %H:%M:%S', localtime(start_time)))
        
        print("Filname collection and moving process started...")
        
        user_input = date_info()
        start_dir = "XXX"
        csv_files_path = 'XXX'
        
        # Call the move_old_csv_files function
        move_old_csv_files(csv_files_path)

        upload_count, notNeed_count = dir_traverse(user_input, start_dir, csv_files_path)
        
        print(upload_count, " files moved to [a]_UpdateSF_Delivered. \n")
        message_upload_count = f"{upload_count} files moved to [a]_UpdateSF_Delivered. \n"
        slack_client.chat_postMessage(channel=channel_id, text=message_upload_count)

        print(notNeed_count, " files moved to [a]_UpdateSF_NotNeeded. \n")
        message_notNeed_count = f"{notNeed_count}  files moved to [a]_UpdateSF_NotNeeded. \n"
        slack_client.chat_postMessage(channel=channel_id, text=message_notNeed_count)
        
        end_time = time.time()
        
        print("end_time", strftime('%Y-%m-%d %H:%M:%S', localtime(end_time)))
        
        elapsed_time = end_time - start_time
        
        print(f"Elapsed time: {elapsed_time} seconds")

    finally:
        release_lock()


if __name__ == "__main__":
    main()


