import os
import re
import csv
from collections import defaultdict
import time
from time import strftime, localtime
import datetime


IMG_EXTENSIONS = ['.gif', '.jpg']

BRAND = ['XXX', 'XXX', 'XXX']


def date_info():
    current_day = datetime.date.today()

    today = datetime.date.strftime(current_day, "%m_%d_%Y")

    return today

def get_file_info(filepath):
    """
    Extracts file information from file path
    Returns a tuple containing (article_number, color_code, view_code)
    """
    filename = os.path.basename(filepath)
    # print("filename", filename)
    extension = os.path.splitext(filename)[1]

    # Check if the file is an image file
    if extension.lower() not in IMG_EXTENSIONS:
        return None, None, None

    # Extract article number, color code, and view code or swatch
    pattern = re.compile(r"[-._]")
    filename_parts = pattern.split(filename)
    view_code = None
    swatch = False

    if filename_parts[-1].endswith(".gif"):
        swatch = True
        view_code = 'swatch'
    elif filename_parts[-1].endswith(".jpg"):
        view_code = filename_parts[1]
    

    if not swatch:
        article_number = filename_parts[0][:9]
        color_code = filename_parts[0][9:]
        view_code = filename_parts[1]
    else:
        article_number = filename_parts[0][:9]
        color_code = filename_parts[0][9:]
        view_code = 'swatch'

    return article_number, color_code, view_code

def get_brand_floorset(filepath):
    """
    Extracts brand and floorset information from file path
    Returns a tuple containing (brand, floorset)
    """
    path_parts = filepath.split(os.sep)
        
    brand, floorset = path_parts[5:7]
    return (brand, floorset)
    


def is_full_set(article_images):
    """
    Determines if a set of images for an article constitutes a full set
    Returns True if it is a full set, False otherwise
    """
    view_codes = set(get_file_info(img)[2] for img in article_images)
    # color_codes = set(get_file_info(img)[1] for img in article_images)
    if 'swatch' not in view_codes:
        return False
    else:
        if (('100' in view_codes and '110' in view_codes and '120' in view_codes and '130' in view_codes) or \
            ('100' in view_codes and '000' in view_codes and '010' in view_codes) or \
            ('000' in view_codes and '010' in view_codes and '020' in view_codes and '100' in view_codes)):
            return True

    # return False

def count_images_and_full_sets(start_dir):
    """
    Counts the number of images and full sets in each floorset of each brand
    """
    image_counts = defaultdict(int)
    full_set_counts = defaultdict(int)
    max_depth = 1

    for root, dirs, files in os.walk(start_dir):
        uni_article_num = set()

        uni_image_count = set()

        floorset_path = re.split('/', root)

        if root[len(start_dir) + 1:].count(os.sep) < max_depth:
            for d in dirs:
                path = os.path.join(root, d)
                # start_time = time.time()
                # print(path, " ", "start_time", strftime('%Y-%m-%d %H:%M:%S', localtime(start_time)))
                # if ('CHI' in root or 'WHI' in root or 'SOM' in root):
                temp_path = re.split('/', path)
                if temp_path[5] in BRAND:
                    new_files = [f for f in os.listdir(path)]
                    new_files.sort()
                    
                    if len(new_files) > 0:
                        for filename in new_files:
                            
                            ext = os.path.splitext(filename)[1].lower()
                            if ext not in ['.jpg', '.gif'] :
                                continue

                            else:
                                filepath = os.path.join(root, filename)
                                
                                brand, floorset = get_brand_floorset(path)

                                image_counts[(brand, floorset)] += 1

                                article_number = get_file_info(filepath)[0]

                                color_code = get_file_info(filepath)[1]

                                full_name = article_number + color_code

                                article_images = [img for img in new_files if full_name in img]
                                
                                if is_full_set(article_images):
                                    if full_name not in uni_article_num:
                                        # print("full_name", full_name)
                                        # print('article_images', article_images)
                                        full_set_counts[(brand, floorset)] += 1
                                        uni_article_num.add(full_name)
                else:
                    continue

                # end_time = time.time()

                # print(path, " ", "end_time", strftime('%Y-%m-%d %H:%M:%S', localtime(end_time)))

                # elapsed_time = end_time - start_time

                # print(f"Elapsed time: {elapsed_time} seconds")
        else:
            dirs[:]
        
            
                    

    return image_counts, full_set_counts

def write_results_to_csv(image_counts, full_set_counts, output_path):
    """
    Writes the image counts and full set counts to a CSV file
    """
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Brand', 'Floorset', 'Image Count', 'Full Set Count'])
        for (brand, floorset), count in image_counts.items():
            full_set_count = full_set_counts[(brand, floorset)]
            writer.writerow([brand, floorset, count, full_set_count])

def main():
    start_time = time.time()
    print("start_time", strftime('%Y-%m-%d %H:%M:%S', localtime(start_time)))

    start_dir = "XXX"
    end_dir = 'XXX'
    
    today = date_info()
    output_file_filename = end_dir + "/images_count_" + today + ".csv"
    output_path = output_file_filename

    image_counts, full_set_counts = count_images_and_full_sets(start_dir)

    # Print results to terminal
    for (brand, floorset), count in image_counts.items():
        full_set_count = full_set_counts[(brand, floorset)]
        print('{:<8} {:<40} {:<8} {:<8}'.format(brand, floorset, str(count) + ' images', str(full_set_count) + ' full sets'))

    # Write results to CSV file
    write_results_to_csv(image_counts, full_set_counts,output_path)

    end_time = time.time()

    print("end_time", strftime('%Y-%m-%d %H:%M:%S', localtime(end_time)))

    elapsed_time = end_time - start_time

    print(f"Elapsed time: {elapsed_time} seconds")

if __name__ == "__main__":
         main()
