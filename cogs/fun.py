import discord
from discord.ext import commands
import random
import asyncio

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.',
                     'It is decidedly so.',
                     'Without a doubt.',
                     'Yes - definitely.',
                     'You may rely on it.',
                     'As I see it, yes.',
                     'Most likely.',
                     'Outlook good.',
                     'Yes.',
                     'Signs point to yes.',
                     'Reply hazy, try again.',
                     'Ask again later.',
                     'Better not tell you now.',
                     'Cannot predict now.',
                     'Concentrate and ask again.',
                     'Don\'t count on it.',
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Very doubtful.']
        await ctx.channel.send(f'The Magic 8-Ball replies: **{random.choice(responses)}**')

    @commands.command(aliases = ['flip'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coinflip(self, ctx, amount: int = 1):
        if amount == 1:
            rng = random.randrange(0, 101)
            if rng < 100:
                await ctx.channel.send(f'{ctx.message.author.mention} flips a coin.')
                await asyncio.sleep(1)
                await ctx.channel.send(f'It lands on **{random.choice(["heads", "tails"])}**!')
            else:
                embed = discord.Embed(colour = discord.Colour.from_rgb(171, 220, 237))
                embed.set_image(url = 'https://i.imgur.com/Lx6NMOO.gif')
                await ctx.channel.send(embed = embed)
        elif 1 < amount <= 100000:
            results = [random.randrange(0, 2) for i in range(0, amount)]
            await ctx.channel.send(f'{ctx.message.author.mention} flips a coin {amount} times.')
            await asyncio.sleep(1)
            await ctx.channel.send(f'It lands on heads {results.count(0)} times and on tails {results.count(1)} times!')
        else:
            await ctx.channel.send('The technology is not there yet!')

    @commands.command(aliases = ['rss', 'horriblesubs'])
    async def seasonal(self, ctx, *, anime):
        rss_feed = f'https://nyaa.si/?page=rss&q={"+".join(anime.split())}+HorribleSubs+1080p'
        await ctx.channel.send(f'Here is your RSS feed: {rss_feed}')

def setup(client):
    client.add_cog(Fun(client))