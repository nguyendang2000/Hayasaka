import discord
from discord.ext import commands
from embed import get_anime_embed, get_manga_embed

class MAL(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def anime(self, ctx, *, name = None):
        await ctx.channel.send(embed = await get_anime_embed(name))

    @commands.command()
    async def manga(self, ctx, *, name = None):
        await ctx.channel.send(embed = await get_manga_embed(name))

def setup(client):
    client.add_cog(MAL(client))