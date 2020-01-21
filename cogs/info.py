import discord
from discord.ext import commands
import asyncio
from config import elapsed, embed_date, embed_format, hayasaka_blue, server_data

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
        embed = discord.Embed(colour = hayasaka_blue)
        embed.set_author(name = f'{server.name}\'s Server Info (ID: {ctx.guild.id})')
        if ctx.guild.icon_url:
            embed.set_thumbnail(url = ctx.guild.icon_url)
        fields = ['Owner', 'Members', 'Text Channels', 'Voice Channels', 'AFK Channel', 'Voice Region', 'Defaults',
                  'Security', 'Roles', 'Custom Emotes', 'Server Created']
        values = server_data(ctx.guild)
        inline = [True, True, True, True, True, True, True, True, False, False, False]
        for i in range(0, len(fields)):
            embed.add_field(name = fields[i], value = values[i], inline = inline[i])
        await ctx.channel.send(embed = embed)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def user(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        status = str(member.status).capitalize()
        id = member.id
        roles = ', '.join([role.name for role in member.roles])
        created_at = embed_date(member.created_at)
        joined_at = embed_date(member.joined_at)
        embed = discord.Embed(title = 'Discord Tag',
                              description = f'{member} ({member.mention})',
                              colour = hayasaka_blue)
        embed.set_author(name = f'{member.display_name}\'s User Info (ID: {id})')
        embed.set_thumbnail(url = member.avatar_url)
        field_names = ['Status', 'Roles', 'Account Created', f'Joined {ctx.guild.name}']
        field_values = [status, roles, created_at, joined_at]
        for i in range(0, len(field_names)):
            embed.add_field(name = field_names[i], value = field_values[i], inline = False)
        await ctx.channel.send(embed = embed)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        embed = discord.Embed(colour = hayasaka_blue)
        embed.set_image(url = member.avatar_url_as(static_format = 'png', size = 256))
        embed.set_footer(text = f'{member.display_name}\'s avatar')
        await ctx.channel.send(embed = embed)

def setup(client):
    client.add_cog(Info(client))