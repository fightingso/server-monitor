import subprocess

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

