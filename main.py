# MC Server Query Bot for Discord by NKSCPreditive

import discord
import asyncio
from mcipc.query import Client
from datetime import datetime

bot = discord.Client()

# SETUP
token = open(r'token.txt', 'r').read() or "" # Your Discord bot's token (Don't share this token with anyone)
server_ip = '127.0.0.1' # Set to the minecraft server's ip address
ports = [25565] # If you have mutiple servers running off the same IP you can add the ports for each server here
message_channel = 0 # Set to the ID of the discord text channel you want to use
# Make sure the channel you are using is an empty channel
update_rate = 30.0 # Time in seconds that the server information is refreshed
bot_timezone = "UTC+0" # The UTC timezone the bot is running in
# END OF SETUP

async def queryMinecraftServer(port, ip=server_ip):
    channel = bot.get_channel(message_channel)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S {}".format(bot_timezone))

    try:
        # Attempts a query connection to the minecraft server
        with Client(ip, port, timeout=5.0) as client:
            stats = client.full_stats
            await channel.send('**Server**: {} **MC Version**: {} **IP**: {}:{} **Player Count**: {}/{}'.format(stats.host_name, stats.version,
                                                                                                                server_ip, stats.host_port, stats.num_players,
                                                                                                                stats.max_players), delete_after=update_rate)
            await channel.send('**Connected Players**: {}'.format(', '.join(stats.players)), delete_after=update_rate)
            await channel.send('*Last Updated: {}*'.format(current_time), delete_after=update_rate)
    except:
        await channel.send('**ERROR**: *Timed out trying to connect to server* __{}:{}__'.format(ip, port), delete_after=update_rate)


@bot.event
async def on_ready():
    channel = bot.get_channel(message_channel)
    print('Logged onto Discord as {0.user}'.format(bot))
    doing = discord.CustomActivity(name="Checking Server Infomation")
    await bot.change_presence(status=discord.Status.online, activity=doing)
    bot.loop.create_task(autoRun())
    msgs = await channel.history().flatten()
    await channel.delete_messages(msgs)
    

async def autoRun():
    while True:
        for port in ports:
            await queryMinecraftServer(port)
        await asyncio.sleep(update_rate)


bot.run(token)