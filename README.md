# SP-MaxPathLengthFixer

Python utility to fix max path length issues before migrating a file share to SharePoint. It identifies, compresses, and deletes overlong paths based on user-defined parameters, aiding smooth OneDrive synchronization. Features include detailed logging and Pushover notifications.

- **Custom path length calculation** based on user-defined organizational parameters
- **255-character limit adherence** to comply with Microsoft's SharePoint and OneDrive sync requirements
- **Directory scanning** to identify paths exceeding the defined max path length
- **Folder compression** and deletion to resolve max path length issues
- **Detailed logging** of compressed and deleted folders, including affected files, their original sizes, and modification dates
- **Pushover notifications** at the completion of pre-scan and main processing stages

#### Requirements
- Python 3.x
- See step 4 to install necessary Python packages

#### Setup and Usage
1. Clone the repository:
   ```
   git clone https://github.com/itsolver/SP-MaxPathLengthFixer.git
   ```
2. Navigate to the script’s directory:
   ```
   cd SP-MaxPathLengthFixer
   ```
3. Setup a Python virtual environment and activate it:
   - On Windows:
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```
   - On Linux/Mac:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
5. (Optional) Configure Pushover notifications:
   - Create a `.env` file in the project root directory with the following structure:
      ```
      PUSHOVER_API_TOKEN=YourPushoverApiTokenHere
      PUSHOVER_USER_KEY=YourPushoverUserKeyHere
      ```
   - Note: To maintain security, ensure `.env` is your `.gitignore` file to prevent it from being tracked in your Git repository.
6. Run the script with:
   ```
   python compress_and_delete.py
   ```
   
#### Notifications
Configure your Pushover API token and user key in the script to receive notifications upon the completion of pre-scan and main processing stages.

#### Logging
The script logs details of compressed and deleted folders, including the list of all affected files, their original sizes, and modification dates, to a log file located in the script’s base directory.

#### Contributing
Feel free to fork the repository and submit pull requests for any enhancements, bug fixes, or other contributions.
