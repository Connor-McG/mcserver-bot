import os
from mcstatus import MinecraftServer
import discord
import json
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
hostnames = json.loads(os.environ['MC_HOSTNAMES'])

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!mcserver':
        for hostname in hostnames:
            server = MinecraftServer.lookup(hostname)
            data = {'online': 'offline'}
            try:
                ping_response = server.ping()
                data['online'] = 'online'
                data['ping'] = ping_response

                status_response = server.status(retries=1)
                data['version'] = status_response.version.name
                data['protocol'] = status_response.version.protocol
                data['motd'] = status_response.description
                data['player_count'] = status_response.players.online
                data['player_max'] = status_response.players.max
                data['players'] = []
                if status_response.players.sample is not None:
                    data['players'] = [{'name': player.name, 'id': player.id} for player in status_response.players.sample]

                query_response = server.query(retries=1)
                data['host_ip'] = query_response.raw['hostip']
                data['host_port'] = query_response.raw['hostport']
                data['map'] = query_response.map
                data['plugins'] = query_response.software.plugins
            except:
                pass
            if data['online'] == 'offline':
                response = f"{hostname}: \U0000274C"
            else:
                if data['players']:
                    response = f"{hostname}: \U00002705 - version: {data['version']} players: {data['player_count']}/{data['player_max']} {data['players']} ping: {data['ping']}ms motd: {data['motd']['text']}"
                else: 
                    response = f"{hostname}: \U00002705 - version: {data['version']} players: {data['player_count']}/{data['player_max']} ping: {data['ping']}ms motd: {data['motd']['text']}"
            await message.channel.send(response)
        
        

client.run(token)