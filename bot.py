import os
from mcstatus import MinecraftServer
import discord
import json
from socket import timeout
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
hostnames = json.loads(os.environ['MC_HOSTNAMES'])
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!mcserver': 
        for hostname in hostnames:

            try:
                server = MinecraftServer.lookup(hostname)
                query = server.query()
                status = server.status()
                if query.players.names == []:
                    response = (f"{hostname} is online with {query.players.online}"
                    f" players and a latency of {status.latency}ms")
                else:
                    response = (f"{hostname} is online with {query.players.online}: "
                    f"{query.players.names} and a latency: {status.latency}ms")
            except timeout:
                response = f"{hostname} is offline"

            except Exception as e:
                response = f"bot encountered exception {e}"

            await message.channel.send(response)

client.run(token)
