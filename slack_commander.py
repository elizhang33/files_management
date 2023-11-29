import os
import logging
import sys
import subprocess
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
import datetime
from threading import Thread
import uuid

client = WebClient(token="XXX")

# Maintain a global last_run_time variable initialized to a time far in the past
last_run_time = datetime.datetime.min

# Cooldown interval in minutes
COOLDOWN_MINUTES = 5

channel_id = 'XXX'

ALLOWED_SCRIPTS = {'slack_files_report.py', 'slack_csvtoxlsx_count.py', 'csvtoxlsx_count.py', 'slack_excel_handler.py', 'conveyor_v2.py', 'slack_conveyor_v2.py', 'tio.py'}

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='slack_listener_log.log',
                    filemode='a')

app_token = "XXX" #command_listener


def send_error_to_slack(error_message):
    try:
        client.chat_postMessage(channel= channel_id, text=f"Error: {error_message}")
    except Exception as e:
        logging.error(f"Failed to send error message to Slack: {e}")

def is_connected():
    try:
        # Try to establish an HTTPS connection to one of the big tech giants.
        subprocess.check_output(['curl', 'https://www.google.com'], stderr=subprocess.STDOUT, timeout=5)
        return True
    except subprocess.CalledProcessError as e:
        return False  # If curl command fails, it's likely an internet problem.
    except Exception as e:
        return False  # General exception means we couldn't determine status. Assuming no internet.


def can_run_script():
    global last_run_time
    current_time = datetime.datetime.now()
    time_difference = current_time - last_run_time
    # Convert the time difference to minutes
    minutes_passed = time_difference.total_seconds() / 60

    if minutes_passed < COOLDOWN_MINUTES:
        logging.info("Script call skipped due to cooldown.")
        return False
    
    last_run_time = current_time
    return True

def run_program(program, unique_id):
    unique_id = uuid.uuid4()
    logging.info(f"Executing with unique ID: {unique_id}")

    try:
        logging.info(f"Executing script: {program}")

        # Notify Slack that the program has started
        client.chat_postMessage(channel= channel_id, text=f"Starting script: {program}")

        subprocess.call([sys.executable, program])

        logging.info(f"Finished executing script: {program}")

        # Notify Slack that the program has finished
        client.chat_postMessage(channel= channel_id, text=f"Finished executing script: {program}")
    except Exception as e:
        logging.error(f"Error while executing script {program}. Error: {e}")
        client.chat_postMessage(channel= channel_id, text=f"Failed to run {program}. Error: {e}")


def handle_command(text):
    unique_id = uuid.uuid4()
    logging.info(f"Unique ID for this run: {unique_id}")

    command_parts = text.split()
    if len(command_parts) == 2 and command_parts[0].lower() == "run":
        script_name = command_parts[1]
        if script_name in ALLOWED_SCRIPTS:
            # Check for cooldown
            # if can_run_script():
            try:
                logging.info(f"Executing script: {script_name}")

                # Create a thread and start it
                # thread = Thread(target=run_program, args=(script_name,))
                # thread.start()
                thread = Thread(target=run_program, args=(script_name, unique_id))
                thread.start()

            except Exception as e:
                logging.error(f"Error while executing script {script_name}. Error: {e}")
                
                # Notify Slack that the program has failed
                client.chat_postMessage(channel= channel_id, text=f"Failed to run {script_name}. Error: {e}")

        else:
            logging.warning(f"Attempt to run unauthorized script: {script_name}")

            # Optionally, send a message to Slack indicating an unauthorized script was attempted
            client.chat_postMessage(channel= channel_id, text=f"Attempt to run unauthorized script: {script_name}")



def process_socket_mode_request(client: SocketModeClient, request: SocketModeRequest):
    
    logging.debug("Received socket mode request")
    logging.debug(f"Envelope ID: {request.envelope_id}, Payload: {request.payload}")
    
    # Log the entire payload for inspection
    logging.debug(f"Full payload: {request.payload}")
    
    if "event" in request.payload and "type" in request.payload["event"]:
        logging.debug("Event type exists in payload")

        if request.payload["event"]["type"] == "message":
            logging.debug("Event type is 'message'")
            
            if "text" in request.payload["event"]:
                text = request.payload["event"]["text"]
                logging.debug(f"Received text: {text}")
                
                if text.lower().startswith("run"):
                    logging.info(f"Handling command for: {text}")
                    handle_command(text)
            else:
                logging.warning("No 'text' in event")
        else:
            logging.warning("Event type is not 'message'")
    else:
        logging.warning("No 'event' or 'type' in payload")
    
    # Acknowledge the request.
    response = {
        "envelope_id": request.envelope_id,
        "payload": {},
    }
    client.send_socket_mode_response(response)


def main():

    sm_client = SocketModeClient(
        app_token=app_token
    )
    sm_client.socket_mode_request_listeners.append(process_socket_mode_request)
    sm_client.connect()

    # Keep the program running
    try:
        if not is_connected():
            error_message = "No internet connection detected."
            logging.error(error_message)
            send_error_to_slack(error_message)
            return
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping the program.")
    except Exception as e:
        error_message = f"Unhandled exception occurred: {e}"
        logging.error(error_message)
        send_error_to_slack(error_message)


if __name__ == "__main__":
    main()
