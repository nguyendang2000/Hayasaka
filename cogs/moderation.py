import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['delete', 'del'])
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.has_permissions(manage_messages = True)
    async def prune(self, ctx, amount: int = 1):
        await ctx.message.delete()
        await ctx.channel.purge(limit = amount)
        msg = await ctx.channel.send(f'{amount} message(s) deleted by {ctx.author.mention}.')
        await asyncio.sleep(5)
        await msg.delete()

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await member.kick(reason = reason)
        await ctx.channel.send(f'Kicked {member}.')

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        await member.ban(reason = reason)
        await ctx.channel.send(f'Banned {member}.')

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f'Unbanned {user}.')

def setup(client):
    client.add_cog(Moderation(client))