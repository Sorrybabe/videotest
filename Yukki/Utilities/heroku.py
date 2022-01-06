import socket
from config import HEROKU_API_KEY


async def is_heroku():
    return 'heroku' in socket.getfqdn()

async def user_input(input):
    if ' ' in input or '\n' in input:
       return str(input.split(maxsplit=1)[1].strip())
    return ''

useragent = (
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/80.0.3987.149 Mobile Safari/537.36"
)

headers = {
    "User-Agent": useragent,
    "Authorization": f"Bearer {HEROKU_API_KEY}",
    "Accept": "application/vnd.heroku+json; version=3.account-quotas",
}
    
