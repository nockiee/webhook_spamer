import json
import requests
import time
import sys
import random
from datetime import datetime, timedelta


def send_message(webhook_url, message, max_retries=3, delay=3):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    for attempt in range(max_retries):
        try:
            response = requests.post(webhook_url, json=message, headers=headers)
            if response.status_code == 204: 
                return True
            else:
                time.sleep(delay)
        except Exception:
            time.sleep(delay)
    return False

def colored_text(text, color):
    colors = {
        "gray": "\033[90m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "reset": "\033[0m",
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"


def update_progress_bar(current, total, start_time, bar_length=120):
    progress = current / total
    filled_length = int(bar_length * progress)

    bar = [colored_text("=", "green") if i < filled_length else colored_text("-", "red") for i in range(bar_length)]

    percentage = int(progress * 100)
    eta = calculate_eta(start_time, current, total)

    progress_line = f"\r{''.join(bar)} {percentage}%"
    info_line = (
        f"ETA: {eta} | Sent: {current} | Start: {start_time.strftime('%H:%M:%S')} | "
        f"End: {eta_end_time(start_time, eta)}"
    )

    sys.stdout.write(progress_line)
    sys.stdout.write(f"\n{info_line}")
    sys.stdout.flush()


def calculate_eta(start_time, current, total):
    elapsed_time = datetime.now() - start_time
    if current == 0:
        return "..."
    average_time_per_task = elapsed_time / current
    remaining_tasks = total - current
    remaining_time = average_time_per_task * remaining_tasks
    return str(remaining_time).split(".")[0]


def eta_end_time(start_time, eta):
    try:
        h, m, s = map(int, eta.split(":"))
        return (datetime.now() + timedelta(hours=h, minutes=m, seconds=s)).strftime("%H:%M:%S")
    except ValueError:
        return "..."


def main():
    try:
        with open("hook.txt", "r") as hook_file:
            webhooks = [line.strip() for line in hook_file.readlines() if line.strip()]
    except FileNotFoundError:
        print("[ERROR] | hook.txt not found!")
        return

    try:
        with open("message.json", "r") as message_file:
            message = json.load(message_file)
    except FileNotFoundError:
        print("[ERROR] | message.json not found!")
        return
    except json.JSONDecodeError:
        print("[ERROR] | Invalid message.json format!")
        return

    num_webhooks = int(input(f"How many webhooks to use? (available: {len(webhooks)}): "))
    num_messages = int(input("How many messages to send?: "))

    if num_webhooks > len(webhooks):
        print(f"[ERROR] | Only {len(webhooks)} webhooks available. Aborting.")
        return

    active_webhooks = webhooks[:num_webhooks]
    total_tasks = num_messages
    completed_tasks = 0
    start_time = datetime.now()

    for _ in range(num_messages):
        webhook = random.choice(active_webhooks)
        success = send_message(webhook, message)
        if not success:
            print(f"\n[ERROR] Failed to send message via {webhook}")
            continue

        completed_tasks += 1
        update_progress_bar(
            current=completed_tasks,
            total=total_tasks,
            start_time=start_time
        )

    print("\nDone!")


if __name__ == "__main__":
    main()
