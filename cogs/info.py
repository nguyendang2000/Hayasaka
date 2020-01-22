import discord
from discord.ext import commands
from embed import get_server_embed, get_user_embed, get_avatar_embed

class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send(f'My ping is {round(self.client.latency * 1000)}ms.')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def server(self, ctx):
        await ctx.channel.send(embed = get_server_embed(ctx.guild))

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def user(self, ctx, *, member: discord.Member = None):
        if member is None: member = ctx.message.author
        await ctx.channel.send(embed = get_user_embed(member))

    @commands.command(aliases = ['pfp', 'picture'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None: member = ctx.message.author
        await ctx.channel.send(embed = get_avatar_embed(member))

def setup(client):
    client.add_cog(Info(client))