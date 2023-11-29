import subprocess
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initialize the Slack client with the token
client = WebClient(token="XXX")
CHANNEL_ID = "XXX"  

def send_message_to_slack(message):
    """Send a message to the specified Slack channel."""
    try:
        response = client.chat_postMessage(channel=CHANNEL_ID, text=message)
        assert response["message"]["text"] == message
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")

def run_script(script_name, wait_time):
    """Run the script and wait for the specified time after its completion."""
    print(f"Running {script_name}...")
    send_message_to_slack(f"Running {script_name}...")
    
    result = subprocess.call(["python3", script_name])
    
    if result == 0:
        print(f"{script_name} completed successfully!")
        send_message_to_slack(f"{script_name} completed successfully!")
    else:
        print(f"{script_name} encountered an error!")
        send_message_to_slack(f"{script_name} encountered an error!")
        
    print(f"Waiting for {wait_time} seconds before running the next script.")
    send_message_to_slack(f"Waiting for {wait_time} seconds before running the next script.")
    time.sleep(wait_time)

if __name__ == "__main__":
    scripts_and_wait_times = [("slack_conveyor_v2.py", 30), ("slack_csvtoxlsx_count.py", 60), ("slack_excel_handler.py", 0)]

    for script, wait_time in scripts_and_wait_times:
        run_script(script, wait_time)
