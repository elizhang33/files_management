"""
Excel-to-SharePoint Slack Bot

This script automatically detects new Excel files uploaded to a specified Slack channel,
uploads them to designated SharePoint folders, and posts the SharePoint links back to the Slack channel.

Dependencies: slack_sdk, office365, requests, datetime, logging
"""

from slack_sdk import WebClient
import datetime
import logging
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.runtime.auth.user_credential import UserCredential
import requests
from office365.runtime.auth.authentication_context import AuthenticationContext

# Initialize logging
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='slack_excel_to_sharepoint.log',  # Name of the log file
                        filemode='a')  # Append mode, so log messages don't overwrite previous


sharepoint_site_url = 'XXX'

# Initialize SharePoint context
user_credentials = UserCredential("XXX", "XXX")
auth_ctx = AuthenticationContext(sharepoint_site_url)
auth_ctx.acquire_token_for_user("XXX", "XXX")
ctx = ClientContext(sharepoint_site_url, auth_ctx)

# Slack API token and channel ID
slack_token = "XXX"
channel_id = "XXX"

# Initialize Slack client
slack_client = WebClient(token=slack_token)

def upload_to_sharepoint_and_return_links(files):
    links = []
    for file_info in files:
        folder_name = None
        if file_info['name'].startswith("XXX"):
            folder_name = "XXX"
        elif file_info['name'].startswith("XXX"):
            folder_name = "XXX"
        elif file_info['name'].startswith("XXX"):
            folder_name = "XXX"
        else:
            logging.warning(f"Unexpected file name {file_info['name']}, skipping.")
            continue

        if folder_name:
            # Here you specify the relative folder path where the files should be uploaded
            relative_folder_url = f"XXX/{folder_name}"
            
            folder = ctx.web.get_folder_by_server_relative_url(relative_folder_url)
            ctx.load(folder)
            try:
                ctx.execute_query()
            except Exception as e:
                print(f"Error while executing SharePoint query: {e}")

            # Download the file from Slack
            file_data = download_from_slack(file_info['url'], slack_token)

            if file_data:
                # Upload to SharePoint
                target_file = folder.upload_file(file_info['name'], file_data)
                ctx.execute_query()
                # Generate a SharePoint share link
                share_link = f"{sharepoint_site_url}/{relative_folder_url}/{file_info['name']}"
                share_link_encoded = share_link.replace(" ", "%20")
                links.append(share_link_encoded)
            else:
                logging.warning(f"Failed to download file {file_info['name']} from Slack.")

    return links


def download_from_slack(file_url, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(file_url, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        logging.error(f"Failed to download file from Slack. Status code: {response.status_code}")
        return None

def main():
    now = datetime.datetime.now()
    five_minutes_ago = now - datetime.timedelta(minutes=20)
    unix_time_five_minutes_ago = int(five_minutes_ago.timestamp())

    response = slack_client.files_list(channel=channel_id, ts_from=unix_time_five_minutes_ago)
    # print("response", response)
    files = [{'name': f['name'], 'url': f['url_private']} for f in response['files'] if f['filetype'] == 'xlsx']
    # print("files", files)

    if files:
        share_links = upload_to_sharepoint_and_return_links(files)
        message = "Uploaded Excel files to SharePoint. Links: " + ', '.join(share_links)
        slack_client.chat_postMessage(channel=channel_id, text=message)
    else:
        slack_client.chat_postMessage(channel=channel_id, text="No new Excel files to upload.")

if __name__ == '__main__':
    main()



'''Excel-to-SharePoint Slack Bot
Overview
This script performs the automated task of detecting new Excel files (*.xlsx) uploaded to a Slack channel, then uploads those files to specific folders within a SharePoint site. After successfully uploading the files to SharePoint, the script sends a message back to the Slack channel containing the SharePoint links to the uploaded files.

Dependencies
slack_sdk: Slack API client for Python
office365: Python library for working with Microsoft Office 365
requests: HTTP library for Python
datetime: Standard Python library for working with dates and times
logging: Standard Python library for generating log files
How It Works
Initialize Logging: Logs are saved to excel_to_sharepoint.log.
Set Credentials & Context: Initializes SharePoint and Slack API contexts with user credentials and API tokens.
Main Functionality:
Fetches recent Excel files from the Slack channel within the last 5 minutes.
For each file:
Determines the target SharePoint folder based on the file name prefix (CHI, SOM, WHI).
Downloads the file from Slack.
Uploads the file to SharePoint.
Sends a message to the Slack channel with links to the uploaded SharePoint files.
Functions
upload_to_sharepoint_and_return_links(files): Uploads files to SharePoint and returns the SharePoint URLs.
download_from_slack(file_url, token): Downloads a file from Slack.
main(): Orchestrates the whole process.
Environmental Variables
slack_token: Slack API token
channel_id: Slack channel ID
sharepoint_site_url: SharePoint site URL
user_credentials: SharePoint user credentials  '''
