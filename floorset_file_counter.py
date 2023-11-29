'''This script create a single csv file of all 3 brand floorsets and show the total unique number of articles
that were uploaded '''

import os
import csv
import re
from datetime import datetime

csv_dir = 'XXX'
output_csv = 'XXX'

# Regular expression pattern to extract the article number
pattern = re.compile(r'([^_]+)')

def get_article_number(filename):
    '''Extract article number from filename'''
    match = pattern.match(filename)
    return match.group(1) if match else None

def count_unique_articles(floorset_name):
    '''Count unique articles in a given floorset csv'''
    csv_file_path = os.path.join(csv_dir, f"{floorset_name}.csv")
    print(f"Counting unique article numbers in {floorset_name}...")
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Use a set to keep track of unique article numbers
        articles = set(get_article_number(row[0]) for row in reader if row)
    return len(articles)

def write_counts_to_csv():
    '''Write the counts of unique articles for each floorset to the output csv'''
    print("Writing counts to output CSV...")
    with open(output_csv, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Floorset", "count"])
        for floorset_file in os.listdir(csv_dir):
            if floorset_file.endswith('.csv'):
                floorset_name = os.path.splitext(floorset_file)[0]
                count = count_unique_articles(floorset_name)
                print(f"Writing count for {floorset_name}: {count}")
                writer.writerow([floorset_name, count])
    print("Writing completed.")

def main():
    start_time = datetime.now()
    print(f"Program started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    print("Counting unique article numbers for each floorset...")
    write_counts_to_csv()
    
    end_time = datetime.now()
    print(f"Counting completed at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
