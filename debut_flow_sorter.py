# import os
# import re
# import time
# from time import strftime, localtime
# import shutil
# import datetime


# IMG_EXTENSIONS = ['.gif', '.jpg']

# BRAND = ['CHI', 'WHI', 'SOM']


# def date_info():
#     current_day = datetime.date.today()

#     today = datetime.date.strftime(current_day, "%m_%d_%Y")

#     return today

# def get_file_info(filepath):
#     """
#     Extracts file information from file path
#     Returns a tuple containing (article_number, color_code, view_code)
#     """
#     filename = os.path.basename(filepath)
#     # print("filename", filename)
#     extension = os.path.splitext(filename)[1]

#     # Check if the file is an image file
#     if extension.lower() not in IMG_EXTENSIONS:
#         return None, None, None

#     # Extract article number, color code, and view code or swatch
#     pattern = re.compile(r"[-._]")
#     filename_parts = pattern.split(filename)
#     view_code = None
#     swatch = False

#     if filename_parts[-1].endswith(".gif"):
#         swatch = True
#         view_code = 'swatch'
#     elif filename_parts[-1].endswith(".jpg"):
#         view_code = filename_parts[1]
    

#     if not swatch:
#         article_number = filename_parts[0][:9]
#         color_code = filename_parts[0][9:]
#         view_code = filename_parts[1]
#     else:
#         article_number = filename_parts[0][:9]
#         color_code = filename_parts[0][9:]
#         view_code = 'swatch'

#     return article_number, color_code, view_code

# def get_brand_floorset(filepath):
#     """
#     Extracts brand and floorset information from file path
#     Returns a tuple containing (brand, floorset)
#     """
#     path_parts = filepath.split(os.sep)
        
#     brand, floorset = path_parts[5:7]
#     return (brand, floorset)
    


# def is_full_set(article_images):
#     """
#     Determines if a set of images for an article constitutes a full set
#     Returns True if it is a full set, False otherwise
#     """
#     view_codes = set(get_file_info(img)[2] for img in article_images)
#     # color_codes = set(get_file_info(img)[1] for img in article_images)
#     if 'swatch' not in view_codes:
#         return False
#     else:
#         if (('100' in view_codes and '110' in view_codes and '120' in view_codes and '130' in view_codes) or \
#             ('100' in view_codes and '000' in view_codes and '010' in view_codes) or \
#             ('000' in view_codes and '010' in view_codes and '020' in view_codes and '100' in view_codes)):
#             return True

#     # return False

# def count_images_and_full_sets(start_dir):
#     """
#     Counts the number of images and full sets in each floorset of each brand
#     """
    
#     new_files = [f for f in os.listdir(start_dir)]
#     new_files.sort()

#     set_count = 0
    
#     if len(new_files) > 0:
#         for filename in new_files:
            
#             ext = os.path.splitext(filename)[1].lower()
#             if ext not in ['.jpg', '.gif'] :
#                 continue

#             else:
#                 filepath = os.path.join(start_dir, filename)

#                 parts = re.split(r"_|-", filename)

#                 full_name = parts[0]

#                 article_images = [img for img in new_files if full_name in img]
                
#                 if is_full_set(article_images):
#                     dest_dir = os.path.join(start_dir, "Debut")

#                     os.makedirs(dest_dir, exist_ok=True)
#                     for item in article_images:
#                         src_dir = os.path.join(start_dir, item)
#                         shutil.move(src_dir, dest_dir)
#                         new_files.remove(item)
#                         print(f'Moved: {item} to Debut')
#                     set_count += 1
                                    
       
#     return set_count


# def main():

#     start_dir = input("What is the path to the floorset you are looking for? ")

#     start_time = time.time()
#     print("start_time", strftime('%Y-%m-%d %H:%M:%S', localtime(start_time)))

#     set_count = count_images_and_full_sets(start_dir)

#     print(set_count, " sets were moved to Debut folder.")

#     end_time = time.time()

#     print("end_time", strftime('%Y-%m-%d %H:%M:%S', localtime(end_time)))

#     elapsed_time = end_time - start_time

#     print(f"Elapsed time: {elapsed_time} seconds")

# if __name__ == "__main__":
#          main()

import os
import re
import time
import shutil
import datetime
from collections import defaultdict

IMG_EXTENSIONS = ['.gif', '.jpg']
BRAND = ['XXX', 'XXX', 'XXX']

def is_full_set(view_codes):
    return 'swatch' in view_codes and (('100' in view_codes and '110' in view_codes and '120' in view_codes and '130' in view_codes) or \
        ('100' in view_codes and '000' in view_codes and '010' in view_codes) or \
        ('000' in view_codes and '010' in view_codes and '020' in view_codes and '100' in view_codes))

def count_images_and_full_sets(start_dir):
    set_count = 0
    article_info = defaultdict(set)
    
    new_files = os.listdir(start_dir)
    new_files.sort()

    for filename in new_files:
        filepath = os.path.join(start_dir, filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext not in IMG_EXTENSIONS:
            continue
        
        # Extract article_number, color_code, view_code
        pattern = re.compile(r"[-._]")
        filename_parts = pattern.split(filename)
        article_number = filename_parts[0][:9]
        view_code = ""

        print("filename_parts", filename_parts[-1])
        if filename_parts[-1] == "jpg":
            view_code = filename_parts[1]
            article_info[article_number].add(view_code)
            print("view_code_jpg", view_code)
        elif filename_parts[-1] == "gif":
            article_info[article_number].add('swatch')
            print("view_code", view_code)

        
        article_info[article_number].add(view_code)

    print("article_info", article_info)  
        
    for article_number, view_codes in article_info.items():
        if is_full_set(view_codes):

            set_count += 1
            debut_dir = os.path.join(start_dir, "Debut")
            os.makedirs(debut_dir, exist_ok=True)
            for filename in new_files:
                if article_number in filename:
                    src_path = os.path.join(start_dir, filename)
                    shutil.move(src_path, debut_dir)
                    print(f'Moved: {src_path} to Debut')
    
    return set_count

def main(): 
    start_dir = input("What is the path to the floorset you are looking for? ")

    start_time = time.time()
    print("start_time", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))

    set_count = count_images_and_full_sets(start_dir)

    print(set_count, " sets were moved to Debut folder.")

    end_time = time.time()
    print("end_time", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

if __name__ == "__main__":
    main()