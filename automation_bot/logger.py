import datetime
import os

# Get the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, "activity_log.txt")

# Get current time
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Append to the log file
with open(log_file, "a") as f:
    f.write(f"🤖 Bot ran successfully at: {now}\n")

print("Log updated.")