import datetime
import logging
import time
from threading import Thread

import schedule
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "MS Rewards Bot is running! Last check: " + datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def run():
    app.run(host="0.0.0.0", port=8080)


def start_server():
    server_thread = Thread(target=run)
    server_thread.daemon = True
    server_thread.start()


def schedule_job():
    from main import main

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] Running scheduled MS Rewards task")
    try:
        main()
        print(
            f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Task completed successfully"
        )
    except Exception as e:
        print(
            f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error during task execution: {str(e)}"
        )


if __name__ == "__main__":
    start_server()

    # Schedule the job to run every day at 8:00 AM
    schedule.every().day.at("08:00").do(schedule_job)

    print("Server started. Scheduled to run daily at 08:00 AM")

    # Run the scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(
            60
        )  # Check every minute instead of every second to reduce resource usage
