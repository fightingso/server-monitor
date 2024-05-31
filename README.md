# Server Monitor

This Discord bot provides server monitoring capabilities by responding to specific commands to display server status information and by notifying in real-time when a login is detected on the server. 

The bot can show who is logged in, GPU information, memory usage, and includes a help command to list available commands.


## Installation

Clone the repository by running the following command.

```bash
git clone https://github.com/fightingso/server-monitor.git
cd server-monitor
```

To run this project, you will need to add the following environment variables to your .env file.

`DISCORD_BOT_TOKEN` : Your Discord bot token. You can get this token from the [Discord Developer Portal](https://discord.com/developers/applications).

`CHANNEL_ID` : ID of the channel using the bot. Multiple channels can be used by separating them with a comma.

Additionally, this project has a feature that outputs command information to a Discord chat only when sudo is executed. To enable this feature, you need to either change the permissions of '/var/log/auth.log' (which can be done using 'sudo setfacl -m u:$(whoami):r /var/log/auth.log') or run the project with sudo.

Finally, install the necessary libraries and run monitor.py.

```
pip install -r requirements.txt
python monitor.py
```
## Examples

<img width="541" alt="image" src="https://github.com/fightingso/server-monitor/assets/104222305/38386d2e-4466-4bc6-9b01-fcb5647ebd32">

Here's how you might use the bot in a Discord server:

- Type `/who` to see the list of logged-in users.
- Type `/smi` to check the GPU status and usage.
- Type `/free` to view the current memory usage.
- Type `/help` to get a list of all commands and what they do.

## Contributing

Contributions are always welcome!
Please feel free to submit a Pull Request.
