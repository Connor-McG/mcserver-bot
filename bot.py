import os
from mcstatus import MinecraftServer
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
hostname = os.getenv('MC_HOSTNAME')

def is_online(server):
    try:
        ping_response = server.ping()
        return ping_response
    except:
        return False

def server_info(server):
    data = {}
    status_response = server.status(retries=1)

    data['version'] = status_response.version.name
    data['protocol'] = status_response.version.protocol
    data['motd'] = status_response.description['text']
    data['player_count'] = status_response.players.online
    data['player_max'] = status_response.players.max
    data['players'] = []

    if status_response.players.sample is not None:
        data['players'] = [{'name': player.name, 'id': player.id} for player in
                           status_response.players.sample]

    return data

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
        server = MinecraftServer.lookup(hostname)

        if is_online(server):
            data = server_info(server)

            response = f"```{hostname} \U00002705 --- ver {data['version']} \n" \
                        f"   {data['motd']} \n " \
                        f"   Players ({data['player_count']}/{data['player_max']}) \n" \

            for player in data['players']:
                response += f'      - {player["name"]}'

            response += ' ```'

        else:
            response = f"``` **{hostname}**  \U0000274C ``` "

        await message.channel.send(response)

client.run(token)
