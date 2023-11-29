import schedule
import time
import subprocess
import os
import sys

def run_program(program):
    subprocess.call(["python3", program])

def pre_check_file(program):
    if os.path.isfile(program):
        return True
    else:
        return False

def get_valid_program():
    while True:
        program = input("Enter the name or path of the program to run: ")
        if pre_check_file(program):
            return program
        else:
            print("Invalid program. Please enter a valid file name or path.")

def schedule_program():
    program = get_valid_program()

    unit = ""
    while True:
        unit = input("Enter the unit (hour/day): ")
        if unit not in ['hour', 'day']:
            print("Invalid unit. Please enter 'hour' or 'day'.")
        else:
            break

    while True:
        if unit == "hour":
            interval = input("Enter the interval in hours, decimal is allowed(e.g. 1 = one hour, 0.1 = 6 mins): ")
            try:
                interval = float(interval)
                if interval <= 0:
                    print("Interval must be a positive value.")
                else:
                    break
            except ValueError:
                print("Invalid interval. Please enter a numeric value.")
        else:
            interval = input("Enter the interval in days, must be an integer: ")
            try:
                interval = int(interval)
                if interval <= 0:
                    print("Interval must be a positive value.")
                else:
                    break
            except ValueError:
                print("Invalid interval. Please enter a numeric value.")

    # Run the program immediately
    run_program(program)

    if unit == 'hour':
        schedule.every(interval).hours.do(run_program, program)
    else:
        schedule.every(interval).days.do(run_program, program)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Restarting the program...")
            time.sleep(300)  # Wait for 300 seconds before restarting
            python = sys.executable
            os.execl(python, "python3", *sys.argv)   #*sys.argv is used to pass the command-line arguments of the current script to the restarted process.

def main():
    schedule_program()

if __name__ == "__main__":
    main()
