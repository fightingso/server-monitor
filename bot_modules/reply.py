import subprocess

async def reply(message):
    if message.content == "/who":
        result = subprocess.run(["who"], capture_output=True, text=True)
        await message.channel.send(result.stdout)

    elif message.content == "/smi":
        result = subprocess.run(["nvidia-smi", "--query-gpu=timestamp,name,utilization.gpu,memory.used", "--format=csv"], capture_output=True, text=True)
        for gpu in result.stdout.split("\n")[1:-1]:
            await message.channel.send(gpu)

    elif message.content == "/free":
        result = subprocess.run(["free", "-h"], capture_output=True, text=True)
        info = result.stdout.split("\n")[1].split(" ")
        info = [element for element in info if element]
        await message.channel.send(f"Used / Total : {info[2]} / {info[1]}")

    elif message.content == "/help":
        help_message = (
            "**Available Commands:**\n"
            "`/who` - Show who is logged in.\n"
            "`/smi` - Show GPU information.\n"
            "`/free` - Show memory usage information.\n"
            "`/help` - Show this help message.\n\n"
            "Interested in contributing to the development of this bot? Visit our GitHub repository at https://github.com/fightingso/server-monitor and see how you can help!"
        )
        await message.channel.send(help_message)

