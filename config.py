import discord
from discord.ext import commands
from datetime import datetime
from dateutil.relativedelta import  relativedelta
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