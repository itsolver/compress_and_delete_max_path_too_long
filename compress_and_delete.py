import os
import zipfile
from datetime import datetime
import json
import shutil
from pushover import Client
from dotenv import load_dotenv
load_dotenv()

PUSHOVER_API_TOKEN = os.getenv('PUSHOVER_API_TOKEN')
PUSHOVER_USER_KEY = os.getenv('PUSHOVER_USER_KEY')

# Initialize Pushover client with your user key and API token
client = Client(PUSHOVER_USER_KEY, api_token=PUSHOVER_API_TOKEN)

def scan_compress_delete(base_dir, available_path_length):
    try:
        # Initialize a list to store paths that exceed the allowed length
        long_paths = []
        
        # Walk through the directory and find paths exceeding the available path length
        for root, dirs, files in os.walk(base_dir):
            for name in dirs:
                path = os.path.join(root, name)
                if len(path) > available_path_length:
                    long_paths.append(path)
        
        # Initialize log dictionary
        log_dict = {"pre_scan": {"long_paths": long_paths}, "main_process": []}
        
        # Write pre-scan results to log file
        with open("compress_delete_log.json", "w") as log_file:
            json.dump(log_dict, log_file, indent=4)
        
        # Notify user of pre-scan completion
        client.send_message("Pre-scan completed. Review the log file before proceeding.", title="Pre-scan Completion")

        # Prompt user to proceed with the main process
        input("Press Enter to continue with the main processing...")
        
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
                shutil.rmtree(path)
                
                # Add folder details to log
                log_dict["main_process"].append(folder_details)
            except Exception as e:
                print(f"An error occurred while processing the path {path}: {e}")
        
        # Write final log details to log file
        with open("compress_delete_log.json", "w") as log_file:
            json.dump(log_dict, log_file, indent=4)
        
        # Notify user of main processing completion
        client.send_message("Main processing completed. Review the final log file for details.", title="Main Processing Completion")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        # Get inputs for calculating the available path length
        longest_username = input("Please provide the longest username in your organization: ")
        org_name = input("Please provide your organization name as in Azure Portal: ")
        longest_library_name = input("Please provide the longest library name: ")

        # Construct a sample path
        sample_path = f"C:\\Users\\{longest_username}\\{org_name} - {longest_library_name}\\"
        path_length = len(sample_path)

        # Calculate the available path length
        available_path_length = 255 - path_length
        print(f"The available path length considering the longest username, organization name, and library name is: {available_path_length} characters")

        # Prompt user for the base directory
        base_dir = input("Please provide the base directory path to scan: ")
        
        # Run the main function
        scan_compress_delete(base_dir, available_path_length)
    except Exception as e:
        print(f"An error occurred: {e}")
