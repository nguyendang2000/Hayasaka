import discord
from discord.ext import commands, tasks
from itertools import cycle

status = cycle([discord.Activity(name = 'over Kaguya-sama', type = discord.ActivityType.watching),
                discord.Activity(name = 'Kaguya-sama', type = discord.ActivityType.listening),
                discord.Activity(name = 'a video of rampaging elephants', type = discord.ActivityType.watching),
                discord.Game('with Kaguya-sama')])

class Tasks(commands.Cog):

    def __init__(self, client):
        self.change_status.start()
        self.client = client

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop(seconds = 60)
    async def change_status(self):
        await self.client.change_presence(activity = next(status))

    @change_status.before_loop
    async def before_change_status(self):
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Tasks(client))