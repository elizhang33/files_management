import os

def rename_files_in_directory(directory):
    # Iterate over all the entries
    for filename in os.listdir(directory):
        # If entry is a file and ends with .csv
        if os.path.isfile(os.path.join(directory, filename)) and filename.endswith(".csv"):
            # Replace hyphen with underscore
            new_filename = filename.replace("-", "_")
            if new_filename != filename:
                # Rename file
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
                print(f"Renamed file {filename} to {new_filename}")

def main():
    directory = 'XXX'
    rename_files_in_directory(directory)

if __name__ == "__main__":
    main()
