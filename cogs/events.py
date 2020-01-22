import discord
from discord.ext import commands, tasks
from logger import log
import asyncio

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready')
        await self.client.change_presence(status = discord.Status.online)
        await log('Hayasaka is online')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await log(f'Hayasaka joined {guild.name} (ID: {guild.id})')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await log(f'Hayasaka left {guild} (ID: {guild.id})')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await log(f'{member} (ID: {member.id}) has joined a server')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await log(f'{member} (ID: {member.id}) has left a server')

    @commands.Cog.listener()
    async def on_message(self, msg):
        await log(f'({msg.guild} #{msg.channel}) {msg.author}: {msg.content}', 'm')
        if msg.author == self.client.user or msg.author.bot:
            return

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        await log(f'({channel.guild} #{channel.name}) {user} is typing...', 'm')

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        await log(f'({msg.guild} #{msg.channel}) {msg.author}: {msg.content}', 'd')

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, msgs):
        for msg in msgs:
            await log(f'({msg.guild} #{msg.channel}) {msg.author}: {msg.content}', 'd')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = await ctx.channel.send(f'Command on cooldown. Please try again after {error.retry_after:.2f}s.')
        elif isinstance(error, commands.BadArgument):
            msg = await ctx.channel.send('Invalid command argument. Please try again.')
        elif isinstance(error, commands.MissingPermissions):
            msg = await ctx.channel.send('Missing permissions for command.')
        else:
            msg = await ctx.channel.send(error)
        await asyncio.sleep(3)
        await msg.delete()

def setup(client):
    client.add_cog(Events(client))