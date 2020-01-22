from datetime import datetime

async def log(content, type = None):
    name = 'general'
    if(type == 'm'):
        name = 'messages'
    elif(type == 'd'):
        name = 'deletions'
    log_file = open(f'logs/{name}.txt', 'a')
    log_file.write(f'[{get_log_time()} UTC] {content}\n')

def get_log_time():
    return datetime.utcnow().strftime("%d/%m/%Y | %H:%M:%S")