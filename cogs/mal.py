import discord
from discord.ext import commands
from jikanpy import AioJikan
import asyncio
from config import hayasaka_blue, anime_data

class MAL(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def anime(self, ctx, *, name = None):
        aio_jikan = AioJikan(loop = asyncio.get_event_loop())
        if(name is None):
            search_term = 'Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen'
        else:
            search_term = name
        search_results = (await aio_jikan.search('anime', search_term)).get('results')
        top_result = await aio_jikan.anime(search_results[0].get('mal_id'))
        for result in search_results[:10]:
            if result.get('title').lower() == search_term.lower():
                top_result = await aio_jikan.anime(result.get('mal_id'))
                break;

        field_names = ['Genres', 'Status', 'Type', 'Score', 'Episodes', 'Start Date', 'End Date', 'Studios']
        field_values = anime_data(top_result)
        field_inline = [False, True, True, True, True, True, True, True]
        await aio_jikan.close()

        embed = discord.Embed(title = field_values[0], url = field_values[1], colour = hayasaka_blue)
        embed.set_author(name = field_values[2])
        embed.set_thumbnail(url = field_values[3])
        for i in range(0, len(field_names)):
            embed.add_field(name = field_names[i], value = field_values[i + 4], inline = field_inline[i])
        await ctx.channel.send(embed = embed)

def setup(client):
    client.add_cog(MAL(client))