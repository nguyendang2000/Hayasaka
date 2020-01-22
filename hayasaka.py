import discord
from discord.ext import commands
from config import token
import os
import asyncio

client = commands.Bot(command_prefix = 'h.')

client.remove_command('help')

@client.command(hidden = True)
@commands.is_owner()
async def load(ctx, extension):
    try:
        client.load_extension(f'cogs.{extension}')
        msg = await ctx.send(f'SUCCESS: Extension **{extension}** loaded.')
    except commands.ExtensionAlreadyLoaded:
        msg = await ctx.send(f'ERROR: Extension **{extension}** is already loaded.')
    except commands.ExtensionNotFound:
        msg = await ctx.send(f'ERROR: Extension **{extension}** not found.')
    finally:
        await asyncio.sleep(5)
        await ctx.message.delete()
        await msg.delete()

@client.command(hidden = True)
@commands.is_owner()
async def unload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        msg = await ctx.send(f'SUCCESS: Extension **{extension}** unloaded.')
    except commands.ExtensionNotLoaded:
        msg = await ctx.send(f'ERROR: Extension **{extension}** is not loaded.')
    except commands.ExtensionNotFound:
        msg = await ctx.send(f'ERROR: Extension **{extension}** not found.')
    finally:
        await asyncio.sleep(5)
        await ctx.message.delete()
        await msg.delete()

@client.command(hidden = True)
@commands.is_owner()
async def reload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        msg = await ctx.send(f'SUCCESS: Extension **{extension}** reloaded.')
    except commands.ExtensionNotLoaded:
        try:
            client.load_extension(f'cogs.{extension}')
            msg = await ctx.send(f'SUCCESS: Extension **{extension}** loaded.')
        except commands.ExtensionNotFound:
            msg = await ctx.send(f'ERROR: Extension **{extension}** not found.')
    finally:
        await asyncio.sleep(5)
        await ctx.message.delete()
        await msg.delete()

for extension in os.listdir('./cogs'):
    if extension.endswith('.py'):
        client.load_extension(f'cogs.{extension[:-3]}')

client.run(token)