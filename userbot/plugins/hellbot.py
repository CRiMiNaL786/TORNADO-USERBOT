# this plugin made by Tornado Userbot

"""Plugin for HellBot Repo

\nCode by @THETORNADOTEAM

type '.destroyx' to get DESTROYX repo
"""

import random, re
from tornadobot.utils import admin_cmd
import asyncio
from telethon import events

@borg.on(admin_cmd(pattern="destroyx ?(.*)"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("Click [here](https://github.com/CRiMiNAL786/DESTROYX) to open this 🔥**Lit AF!!**🔥 **DESTROY X** Repo.. Join Group :- @DESTROYXSUPPORT Repo Uploaded By @TornadoBot_Support")
    
  
