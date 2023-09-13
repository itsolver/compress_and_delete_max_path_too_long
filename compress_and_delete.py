import os
import zipfile
from datetime import datetime
import json
import shutil
from pushover import send_pushover

from dotenv import load_dotenv

load_dotenv()

PUSHOVER_USER_KEY = os.getenv('PUSHOVER_USER_KEY')
PUSHOVER_API_TOKEN = os.getenv('PUSHOVER_API_TOKEN')


def scan_compress_delete(base_dir, available_path_length, dry_run=True):
    try:
        # Initialize a list to store paths that exceed the allowed length
        long_paths = []
        longest_path = ""
        longest_path_length = 0
        
        # Walk through the directory and find paths exceeding the available path length
        for root, dirs, files in os.walk(base_dir):
            for name in dirs:
                path = os.path.join(root, name)
                path_length = len(path)
                if path_length > available_path_length:
                    long_paths.append(path)
                if path_length > longest_path_length:
                    longest_path = path
                    longest_path_length = path_length
        
        # Initialize log dictionary
        log_dict = {"pre_scan": {"long_paths": long_paths, "longest_path": longest_path, "longest_path_length": longest_path_length}, "main_process": []}
        
        # Write pre-scan results to log file
        with open("compress_delete_log.json", "w") as log_file:
            json.dump(log_dict, log_file, indent=4)
        
        # Notify user of pre-scan completion
        prescan_completed_message = "Pre-scan completed. Review the log file for details."
        send_pushover(prescan_completed_message, PUSHOVER_USER_KEY, PUSHOVER_API_TOKEN)
        
        if not long_paths:
            print("No paths exceed the max path length available.")
            print(f"Longest path ({longest_path_length}): {longest_path}")

        # Prompt user to confirm before proceeding with the main process
        if not dry_run:
            confirmation = input("Are you sure you want to proceed with the main processing? (y/n): ")
            if confirmation.lower() != "y":
                print("Main processing aborted.")
                return
        
        # Main processing: compress and delete folders
        for path in long_paths:
            try:
                # Get folder details
                folder_details = {"path": path, "files": []}
                
                # Get details of files in the folder
                for root, dirs, files in os.walk(path):
                    for name in files:
                        file_path = os.path.join(root, name)
                        file_stat = os.stat(file_path)
                        file_details = {
                            "path": file_path,
                            "original_size": file_stat.st_size,
                            "modified_date": datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        }
                        folder_details["files"].append(file_details)
                
                # Compress the folder
                zipf = zipfile.ZipFile(f"{path}.zip", "w", zipfile.ZIP_DEFLATED)
                for root, dirs, files in os.walk(path):
                    for file in files:
                        zipf.write(os.path.join(root, file))
                zipf.close()
                
                # Delete the original folder
                if not dry_run:
                    shutil.rmtree(path)
                
                # Add folder details to log
                log_dict["main_process"].append(folder_details)
            except Exception as e:
                print(f"An error occurred while processing the path {path}: {e}")
        
        # Write final log details to log file
        with open("compress_delete_log.json", "w") as log_file:
            json.dump(log_dict, log_file, indent=4)
        
        # Notify user of main processing completion
        if not dry_run:
            mainscan_completed_message = "Main processing completed. Review the final log file for details."
            send_pushover(mainscan_completed_message, PUSHOVER_USER_KEY, PUSHOVER_API_TOKEN)
        else:
            dry_run_completed_message = "Dry run completed. No folders were compressed or deleted."
            send_pushover(dry_run_completed_message, PUSHOVER_USER_KEY, PUSHOVER_API_TOKEN)
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    try:
        # Prompt user for the base directory
        base_dir = input("Please provide the base directory path to scan: ")
        print("Now lets consider your longest username, organization name, and library name to calculate the available path length.")
        # Get inputs for calculating the available path length
        longest_username = input("Longest username in your organization (exclude `@domain`): ")
        org_name = input("Organization name as in Azure Portal: ")
        longest_site_name = input("Longest site name: ")        
        longest_library_name = input("Longest library name: ")

        # Construct a sample path
        sample_path = f"C:\\Users\\{longest_username}\\{org_name}\\{longest_site_name} - {longest_library_name}\\"
        path_length = len(sample_path)

        # Calculate the available path length
        print("Base path length = ", path_length)
        print("Available path length = 255 - ", path_length)
        available_path_length = 255 - path_length
        print(f"The available path length considering the longest username, organization name, and library name is: {available_path_length} characters")

       
        
        # Run the main function
        scan_compress_delete(base_dir, available_path_length)
    except Exception as e:
        print(f"An error occurred: {e}")
