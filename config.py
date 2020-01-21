import discord
from datetime import datetime
from dateutil.relativedelta import  relativedelta
from random import sample
import inflect

e = inflect.engine()
hayasaka_blue = discord.Colour.from_rgb(171, 220, 237)

async def log(content, type = None):
    log_name = 'general'
    if(type == 's'):
        log_name = 'server'
    elif(type == 'm'):
        log_name = 'messages'
    elif(type == 'd'):
        log_name = 'deletions'
    log_file = open(f'logs/{log_name}.txt', 'a')
    log_file.write(f'[{log_time()} UTC] {content}\n')

def log_time():
    return datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")

def elapsed(start, end):
    difference = relativedelta(start, end)
    divisions = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
    return ['%d %s' % (getattr(difference, division), getattr(difference, division) > 1
                       and division or division[:-1]) for division in divisions if getattr(difference, division)]

def embed_date(date):
    weekday_month = date.strftime('%A, %B')
    day = e.ordinal(date.strftime(' %d'))
    year_time = date.strftime(' %Y at %I:%M %p UTC')
    time_since = f'\n({e.join((elapsed(datetime.utcnow(), date))[0:3])} ago)'
    return weekday_month + day + year_time + time_since

embed_dictionary = {'0': 'No', '1': 'Yes', 'disabled': 'Disabled', 'no_role': 'No Role', 'all_members': 'Everyone',
                  'NotificationLevel.all_messages': 'All', 'NotificationLevel.only_mentions': 'Mentions',
                  'none': 'None', 'low': 'Low', 'medium': 'Medium', 'high': 'High', 'extreme': 'Extreme'}

def embed_format(term):
    return embed_dictionary[str(term)]

def server_data(server):
    owner = server.owner.display_name
    member_count = str(len(server.members))
    online_count = 0
    for member in server.members:
        if (str(member.status) == "online"):
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
    if (len(emotes_list) < emotes_cap):
        emotes_cap = len(emotes_list)
    emotes = ' '.join(sample(emotes_list, emotes_cap))
    created_at = embed_date(server.created_at)
    return [owner, member_count + online, text_count, voice_count, afk_channel, region, f'{notifications}\n{filter}',
            f'{verification}\n{mfa}', roles, emotes, created_at]

def mal_date(date):
    if date is not None:
        return datetime.strftime(datetime.strptime(date[:10], '%Y-%m-%d'), '%B %d, %Y')
    else:
        return "None"

def mal_format(term):
    if term is None:
        return "None"
    if isinstance(term, list):
        if len(term) == 0:
            return 'None'
        else:
            return ', '.join(term)
    return term

def anime_data(anime):
    title = anime.get('title')
    url = anime.get('url')
    title_jp = anime.get('title_japanese')
    image_url = anime.get('image_url')
    genres = mal_format(', '.join([f'[{genre.get("name")}]({genre.get("url")})' for genre in anime.get('genres')]))
    status = anime.get('status')
    type = anime.get('type')
    score = mal_format(anime.get('score'))
    episodes = anime.get('episodes')
    duration = anime.get('duration')
    start_date = mal_date((anime.get('aired')).get('from'))
    end_date = mal_date((anime.get('aired')).get('to'))
    studios = mal_format([f'[{studio.get("name")}]({studio.get("url")})' for studio in anime.get('studios')])
    return [title, url, title_jp, image_url, genres, status, type, score, f'{episodes} ({duration})',
            start_date, end_date, studios]