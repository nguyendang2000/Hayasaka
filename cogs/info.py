import discord
from discord.ext import commands
import asyncio
from random import sample
from config import elapsed, embed_date, embed_format

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
        server = ctx.guild
        owner = server.owner.display_name
        member_count = str(len(server.members))
        online_count = 0
        for member in server.members:
            if(str(member.status) == "online"):
                online_count += 1
        online = f' ({online_count} Online)'
        text_count = len(server.text_channels)
        voice_count = len(server.voice_channels)
        afk_channel = server.afk_channel
        region = str(server.region).capitalize()
        notifications = f'**Notifications**: {embed_format(server.default_notifications)}'
        filter = f'**NSFW Filter**: {embed_format(server.explicit_content_filter)}'
        verification = f'**Verification**: {embed_format(server.verification_level)}'
        mfa = f'**MFA**: {embed_format(server.mfa_level)}'
        roles = ', '.join([role.name for role in server.roles[::-1][:10]])
        role_count = len(server.roles)
        if role_count - 10 > 0:
            roles = f'{roles}, and {role_count - 10} other(s).'
        emotes_list = [str(emote) for emote in server.emojis]
        emotes_count = len(emotes_list)
        emotes_cap = 28
        if(len(emotes_list) < emotes_cap):
            emotes_cap = len(emotes_list)
        emotes = ' '.join(sample(emotes_list, emotes_cap))
        created_at = embed_date(server.created_at)
        embed = discord.Embed(colour = discord.Colour.from_rgb(171, 220, 237))
        embed.set_author(name = f'{server.name}\'s Server Info (ID: {server.id})')
        if server.icon_url:
            embed.set_thumbnail(url = server.icon_url)
        field_names = ['Owner', 'Members', 'Text Channels', 'Voice Channels', 'AFK Channel', 'Voice Region', 'Defaults',
                  'Security', f'Roles ({role_count})', f'Custom Emotes ({emotes_count})', 'Server Created']
        field_values = [owner, member_count + online, text_count, voice_count, afk_channel, region,
                  f'{notifications}\n{filter}', f'{verification}\n{mfa}', roles, emotes, created_at]
        field_inline = [True, True, True, True, True, True, True, True, False, False, False]
        for i in range(0, len(field_names)):
            embed.add_field(name = field_names[i], value = field_values[i], inline = field_inline[i])
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
                              colour = discord.Colour.from_rgb(171, 220, 237))
        embed.set_author(name = f'{member.display_name}\'s User Info',
                         icon_url = member.avatar_url)
        embed.set_thumbnail(url = member.avatar_url)
        field_names = ['Status', 'ID', 'Roles', 'Account Created', f'Joined {ctx.guild.name}']
        field_values = [status, id, roles, created_at, joined_at]
        field_inline = [True, True, False, False, False]
        for i in range(0, len(field_names)):
            embed.add_field(name = field_names[i], value = field_values[i], inline = field_inline[i])
        await ctx.channel.send(embed = embed)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        pfp = discord.Embed(colour = discord.Colour.from_rgb(171, 220, 237))
        pfp.set_image(url = member.avatar_url_as(static_format = 'png', size = 256))
        pfp.set_footer(text = f'{member.display_name}\'s avatar')
        await ctx.channel.send(embed = pfp)

def setup(client):
    client.add_cog(Info(client))