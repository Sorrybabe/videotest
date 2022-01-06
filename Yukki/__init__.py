import asyncio
import os
import time
import heroku3
from os import listdir, mkdir

from git import Repo
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient as Bot
from rich.console import Console
from rich.table import Table

from config import ASSISTANT_PREFIX, DURATION_LIMIT_MIN, LOG_GROUP_ID, UPSTREAM_REPO, UPSTREAM_BRANCH
from config import MONGO_DB_URI as mango
from config import MUSIC_BOT_NAME, OWNER_ID, SUDO_USERS, get_queue, HEROKU_API_KEY
from config import STRING1, STRING2, STRING3, STRING4, STRING5, LOG_SESSION
from Yukki.Core.Clients.cli import (ASS_CLI_1, ASS_CLI_2, ASS_CLI_3,
                                    ASS_CLI_4, ASS_CLI_5, LOG_CLIENT, app)
from Yukki.Utilities.changers import time_to_seconds
from Yukki.Utilities.heroku import is_heroku
from git.exc import GitCommandError, InvalidGitRepositoryError
loop = asyncio.get_event_loop()
console = Console()


### Heroku Shit
Heroku_cli = None
Heroku_app = None
UPSTREAM_BRANCH = UPSTREAM_BRANCH
UPSTREAM_REPO = UPSTREAM_REPO

### Modules
MOD_LOAD = []
MOD_NOLOAD = []

### Mongo DB
MONGODB_CLI = Bot(mango)
db = MONGODB_CLI.Yukki

### Boot Time
boottime = time.time()

### Clients
app = app
ASS_CLI_1 = ASS_CLI_1
ASS_CLI_2 = ASS_CLI_2
ASS_CLI_3 = ASS_CLI_3
ASS_CLI_4 = ASS_CLI_4
ASS_CLI_5 = ASS_CLI_5
LOG_CLIENT = LOG_CLIENT
aiohttpsession = ClientSession()

### Config
SUDOERS = SUDO_USERS
OWNER_ID = OWNER_ID
LOG_GROUP_ID = LOG_GROUP_ID
MUSIC_BOT_NAME = MUSIC_BOT_NAME
DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
ASSISTANT_PREFIX = ASSISTANT_PREFIX

### Bot Info
BOT_ID = 0
BOT_NAME = ""
BOT_USERNAME = ""

### Assistant Info
ASSIDS = []
ASSID1 = 0
ASSNAME1 = ""
ASSUSERNAME1 = ""
ASSMENTION1 = ""
ASSID2 = 0
ASSNAME2 = ""
ASSUSERNAME2 = ""
ASSMENTION2 = ""
ASSID3 = 0
ASSNAME3 = ""
ASSUSERNAME3 = ""
ASSMENTION3 = ""
ASSID4 = 0
ASSNAME4 = ""
ASSUSERNAME4 = ""
ASSMENTION4 = ""
ASSID5 = 0
ASSNAME5 = ""
ASSUSERNAME5 = ""
ASSMENTION5 = ""
random_assistant = []

async def initiate_bot():
    global SUDOERS, OWNER_ID, ASSIDS
    global BOT_ID, BOT_NAME, BOT_USERNAME
    global ASSID1, ASSNAME1, ASSMENTION1, ASSUSERNAME1
    global ASSID2, ASSNAME2, ASSMENTION2, ASSUSERNAME2
    global ASSID3, ASSNAME3, ASSMENTION3, ASSUSERNAME3
    global ASSID4, ASSNAME4, ASSMENTION4, ASSUSERNAME4
    global ASSID5, ASSNAME5, ASSMENTION5, ASSUSERNAME5
    global Heroku_cli, Heroku_app
    os.system("clear")
    header = Table(show_header=True, header_style="bold yellow")
    header.add_column(
        "\x59\x75\x6b\x6b\x69\x20\x4d\x75\x73\x69\x63\x20\x42\x6f\x74\x20\x3a\x20\x54\x68\x65\x20\x4d\x6f\x73\x74\x20\x41\x64\x76\x61\x6e\x63\x65\x64\x20\x4d\x75\x73\x69\x63\x20\x42\x6f\x74"
    )
    console.print(header)
    with console.status(
        "[magenta] Yukki Music Bot Booting...",
    ) as status:
        console.print("┌ [red]Booting Up The Clients...\n")
        await app.start()
        console.print("└ [green]Booted Bot Client")
        console.print("\n┌ [red]Booting Up The Assistant Clients...")
        if STRING1 != "None":
            await ASS_CLI_1.start()
            random_assistant.append(1)
            console.print("├ [yellow]Booted Assistant Client")
        if STRING2 != "None":
            await ASS_CLI_2.start()
            random_assistant.append(2)
            console.print("├ [yellow]Booted Assistant Client 2")
        if STRING3 != "None":
            await ASS_CLI_3.start()
            random_assistant.append(3)
            console.print("├ [yellow]Booted Assistant Client 3")
        if STRING4 != "None":
            await ASS_CLI_4.start()
            random_assistant.append(4)
            console.print("├ [yellow]Booted Assistant Client 4")
        if STRING5 != "None":
            await ASS_CLI_5.start()
            random_assistant.append(5)
            console.print("├ [yellow]Booted Assistant Client 5")
        console.print("└ [green]Assistant Clients Booted Successfully!")
        if LOG_SESSION != "None":
            console.print("\n┌ [red]Booting Logger Client")
            await LOG_CLIENT.start()
            console.print("└ [green]Logger Client Booted Successfully!")
        if "raw_files" not in listdir():
            mkdir("raw_files")
        if "downloads" not in listdir():
            mkdir("downloads")
        if "cache" not in listdir():
            mkdir("cache")
        if "search" not in listdir():
            mkdir("search")
        console.print("\n┌ [red]Loading Clients Information...")
        getme = await app.get_me()
        BOT_ID = getme.id
        if getme.last_name:
            BOT_NAME = getme.first_name + " " + getme.last_name
        else:
            BOT_NAME = getme.first_name
        BOT_USERNAME = getme.username
        if STRING1 != "None":
            getme1 = await ASS_CLI_1.get_me()
            ASSID1 = getme1.id
            ASSIDS.append(ASSID1)
            ASSNAME1 = (
                f"{getme1.first_name} {getme1.last_name}"
                if getme1.last_name
                else getme1.first_name
            )
            ASSUSERNAME1 = getme1.username
            ASSMENTION1 = getme1.mention
        if STRING2 != "None":
            getme2 = await ASS_CLI_2.get_me()
            ASSID2 = getme2.id
            ASSIDS.append(ASSID2)
            ASSNAME2 = (
                f"{getme2.first_name} {getme2.last_name}"
                if getme2.last_name
                else getme2.first_name
            )
            ASSUSERNAME2 = getme2.username
            ASSMENTION2 = getme2.mention
        if STRING3 != "None":
            getme3 = await ASS_CLI_3.get_me()
            ASSID3 = getme3.id
            ASSIDS.append(ASSID3)
            ASSNAME3 = (
                f"{getme3.first_name} {getme3.last_name}"
                if getme3.last_name
                else getme3.first_name
            )
            ASSUSERNAME3 = getme3.username
            ASSMENTION3 = getme3.mention
        if STRING4 != "None":
            getme4 = await ASS_CLI_4.get_me()
            ASSID4 = getme4.id
            ASSIDS.append(ASSID4)
            ASSNAME4 = (
                f"{getme4.first_name} {getme4.last_name}"
                if getme4.last_name
                else getme4.first_name
            )
            ASSUSERNAME4 = getme4.username
            ASSMENTION4 = getme4.mention
        if STRING5 != "None":
            getme5 = await ASS_CLI_5.get_me()
            ASSID5 = getme5.id
            ASSIDS.append(ASSID5)
            ASSNAME5 = (
                f"{getme5.first_name} {getme5.last_name}"
                if getme5.last_name
                else getme5.first_name
            )
            ASSUSERNAME5 = getme5.username
            ASSMENTION5 = getme5.mention
        console.print("└ [green]Loaded Clients Information!")
        console.print("\n┌ [red]Loading Sudo Users...")
        sudoersdb = db.sudoers
        sudoers = await sudoersdb.find_one({"sudo": "sudo"})
        sudoers = [] if not sudoers else sudoers["sudoers"]
        for user_id in SUDOERS:
            if user_id not in sudoers:
                sudoers.append(user_id)
                await sudoersdb.update_one(
                    {"sudo": "sudo"},
                    {"$set": {"sudoers": sudoers}},
                    upsert=True,
                )
        SUDOERS = (SUDOERS + sudoers + OWNER_ID) if sudoers else SUDOERS
        console.print("└ [green]Loaded Sudo Users Successfully!\n")
        if await is_heroku():
            console.print("\n┌ [red]Heroku App Detected...")
            if HEROKU_API_KEY != "" :
                Heroku_cli = heroku3.from_key(HEROKU_API_KEY)
                console.print("\n├ [green]Connected to Heroku Client...")                
            if HEROKU_APP_NAME == "":
                try:
                    Heroku_app = Heroku_cli.app(HEROKU_APP_NAME)
                    console.print("\n├ [green]Connected to Heroku App...") 
                except:
                    console.print("\n├ [red] Error! HEROKU_APP_NAME doesnt exist...") 
                    return
            console.print("\n└ [red]Heroku App Setup Completed...\n")     
        try:
            repo = Repo()
        except GitCommandError:
            console.print("┌ [red] Checking Git Client!")
            console.print("└ [red]Git Command Error\n")
            return
        except InvalidGitRepositoryError:
            console.print("┌ [red] Checking Git Client!")
            repo = Repo.init()
            if "notreallyshikhar_tmp" in repo.remotes:
                origin = repo.remote("notreallyshikhar_tmp")
            else:
                origin = repo.create_remote("notreallyshikhar_tmp", UPSTREAM_REPO)
            origin.fetch()
            repo.create_head(UPSTREAM_BRANCH, origin.refs.master)
            repo.heads.master.set_tracking_branch(origin.refs.master)
            repo.heads.master.checkout(True)
            active_branch = repo.active_branch.name
            if active_branch != UPSTREAM_BRANCH:
                console.print("└ [red] UPSTREAM_BRANCH is not defined wrong. Correct the Branch.\n")
                return
            try:
               repo.create_remote("notreallyshikhar_tmp", UPSTREAM_REPO)
            except BaseException:
               pass
            console.print("└ [red]Git Client Setup Completed\n")
            





loop.run_until_complete(initiate_bot())

def init_db():
    global db_mem
    db_mem = {}

init_db()
