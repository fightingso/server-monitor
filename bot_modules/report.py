import subprocess
import re
import os
import asyncio 
from dotenv import load_dotenv

_users = set()

async def send_report(message, client, channel_id):
    for channel in channel_id:
        channel = client.get_channel(int(channel))
        await channel.send(message)


async def login_report(client, channel_id):
    global _users

    who = subprocess.run(["who"], capture_output=True, text=True).stdout
    users = who.split("\n")[:-1]

    current_users = set()
    for user in users:
        parts = user.split()
        name = parts[0]
        ip = parts[-1].replace("(", "").replace(")", "")
        current_users.add((name, ip))

    new_logins = current_users - _users
    for name, ip in new_logins:
        await send_report(f"{name} logged in from {ip}", client, channel_id)

    logouts = _users - current_users
    for name, ip in logouts:
        await send_report(f"{name} logged out from {ip}", client, channel_id)

    _users = current_users

async def sudo_report(client, channel_id):
    with open("/var/log/auth.log", "r") as log_file:
        log_file.seek(0, os.SEEK_END)

        while True:
            line = log_file.readline()
            if not line:
                await asyncio.sleep(1) 
                continue

            if "sudo" in line and "COMMAND" in line:
                match = re.search(r'([^ ]+)\s+([^ ]+)\s+sudo:\s+([^:]+):\s+TTY=([^ ]+)\s+; PWD=([^ ]+)\s+; USER=([^ ]+)\s+; COMMAND=(.+)', line)
                if match:
                    timestamp = match.group(1)
                    hostname = match.group(2)
                    user = match.group(3)
                    tty = match.group(4)
                    pwd = match.group(5)
                    runas_user = match.group(6)
                    command = match.group(7).strip()
                    command_clean = re.sub(r'/usr/bin/', '', command)

                    try:
                        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10, cwd=pwd, encoding='utf-8', errors='ignore')
                        output = result.stdout.strip() if result.stdout else "No output"
                        error = result.stderr.strip() if result.stderr else "No errors"
                    except subprocess.TimeoutExpired:
                        output = "Command timed out"
                        error = "Command timed out"

                    report_message = (
                        f"```zsh\n"
                        f"{user}:: {pwd} >> {command_clean}\n\n"
                        f"**Output:**\n{output}\n\n"
                        f"**Errors:**\n{error}\n"
                        f"```"
                    )
                    await send_report(report_message, client, channel_id)
