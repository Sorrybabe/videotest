import os

import random
import asyncio
import urllib3
import heroku3
import math
import requests


from git import Repo
from datetime import datetime
from time import time, strftime

from pyrogram import Client, filters

from config import HEROKU_API_KEY, HEROKU_APP_NAME
from Yukki import app, SUDOERS, LOG_GROUP_ID
from Yukki.Utilities.heroku import is_heroku, user_input
from Yukki.Utilities.paste import isPreviewUp, paste_queue

from pyrogram.types import Message

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(
        HEROKU_API_KEY
    ),
    "https",
    str(
        HEROKU_APP_NAME
    ),
    "HEAD",
    "main"
]

@app.on_message(filters.command("get_log") & filters.user(SUDOERS))
async def log_(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\nIn order to update your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!</code>")
            return
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>")
            return
    else:
        await message.reply_text("Only for Heroku Apps")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(" Please make sure your Heroku API Key, Your App name are configured correctly in the heroku")
    data = happ.get_log()
    if len(data) > 1024:
        link = await paste_queue(data)
        url = link + "/index.txt"
        return await message.reply_text(f"Here is the Log of Your App[{HEROKU_APP_NAME}]\n\n[Click Here to checkout Logs]({url})")
    else:
        await message.reply_text(data)
        
        
@app.on_message(filters.command("get_var") & filters.user(SUDOERS))
async def varget_(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\nIn order to update your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!</code>")
            return
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>")
            return
    else:
        await message.reply_text("Only for Heroku Apps")
    usage = "**Usage:**\n/get_var [Var Name]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(" Please make sure your Heroku API Key, Your App name are configured correctly in the heroku")  
    heroku_config = happ.config()
    if check_var in heroku_config:
        return await message.reply_text(f"**Heroku Config:**\n\n**{check_var}:** <code>{heroku_config[check_var]}</code>")
    else:
        return await message.reply_text(f"No such Var")                                
                                        
    
@app.on_message(filters.command("del_var") & filters.user(SUDOERS))
async def vardel_(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\nIn order to update your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!</code>")
            return
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>")
            return
    else:
        await message.reply_text("Only for Heroku Apps")
    usage = "**Usage:**\n/del_var [Var Name]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(" Please make sure your Heroku API Key, Your App name are configured correctly in the heroku")  
    heroku_config = happ.config()
    if check_var in heroku_config:
        await message.reply_text(f"**Heroku Var Deletion:**\n\n{check_var} has been deleted successfully.")
        del heroku_config[check_var]
    else:
        return await message.reply_text(f"No such Var")    
    
@app.on_message(filters.command("set_var") & filters.user(SUDOERS))
async def set_var(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\nIn order to update your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!</code>")
            return
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>")
            return
    else:
        await message.reply_text("Only for Heroku Apps")
    usage = "**Usage:**\n/set_var [Var Name] [Var Value]"
    if len(message.command) < 3:
        return await message.reply_text(usage)
    to_set = message.text.split(None, 2)[1].strip()
    value = message.text.split(None, 2)[2].strip()
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(" Please make sure your Heroku API Key, Your App name are configured correctly in the heroku")  
    heroku_config = happ.config()
    if to_set in heroku_config:
        await message.reply_text(f"**Heroku Var Updation:**\n\n{check_var} has been updated successfully. Bot will Restart Now.")
    else:
        await message.reply_text(f"Added New Var with name {to_set}. Bot will Restart Now.")   
    heroku_config[to_set] = value

    
@app.on_message(filters.command("usage") & filters.user(SUDOERS))
async def usage_dynos(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\nIn order to update your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!</code>")
            return
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>")
            return
    else:
        await message.reply_text("Only for Heroku Apps")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(" Please make sure your Heroku API Key, Your App name are configured correctly in the heroku")
    dyno = await message.reply_text("Checking Heroku Usage. Please Wait")
    account_id = Heroku.account().id
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
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("Unable to fetch.")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    return await dyno.edit(
        "**Dyno Usage**:\n\n"
        f" -> `Dyno usage for`  **{HEROKU_APP_NAME}**:\n"
        f"     •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
        f"**|**  [`{AppPercentage}`**%**]"
        "\n\n"
        " -> `Dyno hours quota remaining this month`:\n"
        f"     •  `{hours}`**h**  `{minutes}`**m**  "
        f"**|**  [`{percentage}`**%**]"
    )


@app.on_message(filters.command("update") & filters.user(SUDOERS))
async def update_(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\nIn order to update your app, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!</code>")
            return
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            await message.reply_text("<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>")
            return
    response = await message.reply_text("<code>Checking for available updates...</code>")
    os.system(
        'git fetch origin master &> /dev/null'
    ) ;
    await asyncio.sleep(7)
    verification = ""
    repo = Repo()
    REPO_ = repo.remotes.origin.url.split('.git')[0] # main git repository
    for checks in repo.iter_commits("HEAD..origin/master"):
        verification = str(checks.count())
    if verification == "":
        await response.edit("<code>Bot is up-to-date! 1</code>")
        return
    if "-push" in await user_input(message.text):
        if verification == "":
            await response.edit("<code>Bot is up-to-date! 2</code>")
            return
        await response.edit("<b>Found a new update!</b>")
        await asyncio.sleep(1)
        await response.edit("<code>Trying to update, please be patient!</code>")
        os.system(
            'git stash &> /dev/null && git pull'
        ) ;
        if await is_heroku():
            try:
                await response.edit("<code> 3 Bot was updated successfully! Now, wait for 1 - 2 mins until the bot restarts!</code>")
                os.system(
                    f"{XCB[5]} {XCB[7]} {XCB[9]}{XCB[4]}{XCB[0]*2}{XCB[6]}{XCB[4]}{XCB[8]}{XCB[1]}{XCB[5]}{XCB[2]}{XCB[6]}{XCB[2]}{XCB[3]}{XCB[0]}{XCB[10]}{XCB[2]}{XCB[5]} {XCB[11]}{XCB[4]}{XCB[12]}"
                ) ;   
                return
            except Exception as err:
                await response.edit("<code>Something went wrong while initiating reboot! Please try again later or check logs for more info.</code>")
                await app.send_message(LOG_GROUP_ID, f"AN EXCEPTION OCCURRED AT #UPDATER DUE TO: <code>{err}</code>")
                return
        else:
            await response.edit("<code>Bot was updated successfully! Now, wait for 1 - 2 mins until the bot reboots!</code>")
            os.system(
                'pip3 install -r requirements.txt'
            ) ;
            os.system(
                f"kill -9 {os.getpid()} && bash start"
            ) ;
            exit()
        return        
    updates = ""
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"
        [
            (
                format // 10 % 10 != 1
            ) * 
            (
                format % 10 < 4
            ) * format % 10 :: 4
        ]
    )
    for info in repo.iter_commits("HEAD..origin/master"):
        updates += f"<b>➣ #{info.count()}: [{info.summary}]({REPO_}/commit/{info}) by -> {info.author}</b>\n\t\t\t\t<b>➥ Commited on:</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
    _update_response_ = "<b>A new update is available for the Bot!</b>\n\n➣ Push Updates by\n\t\t\t\t\t\t➥ <code>/update -push</code>\n\n**<u>Updates:</u>**\n\n"
    _final_updates_ = _update_response_ + updates
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    _rand_ = f"changelog_{''.join((random.choice('0123456789abcdef') for i in range(4)))}.txt"
    _rand_x_ = os.path.join("tmp", _rand_)
    if len(_final_updates_) > 4096:
        await response.delete()
        open(_rand_x_, "w").write(_final_updates_)
        try:
            await app.send_document(
                message.chat.id,
                _rand_x_,
                caption = f"<b>#CHANGELOG</b>\n\n➣ Push Updates by\n\t\t\t\t\t\t➥ <code>/update -push</code>"
            )
            os.remove(_rand_x_)
            return
        except Exception as err:
            await app.send_message(LOG_GROUP_ID, f"<b>ISSUE RAISED AT #UPDATER</b>\n\n<b>>></b> `{err}`")
            os.remove(_rand_x_)
            return
    await response.edit(
        _final_updates_,
        disable_web_page_preview = True
    )
