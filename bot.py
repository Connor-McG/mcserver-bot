import os
from mcstatus import MinecraftServer
import discord
import json
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
            response = f"{hostname} is offline"
            try:
                server = MinecraftServer.lookup(hostname)
                query = server.query()
                status = server.status()
                if query.players.names == []:
                    response = f"{hostname} is online with {query.players.online} players and a latency of {status.latency}ms"
                else:
                    response = f"{hostname} is online with {query.players.online}: {query.players.names} and a latency: {status.latency}ms"
            except:
                pass
            await message.channel.send(response)

client.run(token)
