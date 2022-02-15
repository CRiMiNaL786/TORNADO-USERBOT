import re

from tornadobot import bot
from tornadobot.utils import admin_cmd, sudo_cmd, edit_or_reply
from tornadobot.cmdhelp import CmdHelp
from tornadobot.helpers.functions import deEmojify
from userbot.Config import Config
from . import *

@bot.on(admin_cmd(pattern="anime(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="anime(?: |$)(.*)", allow_sudo=True))
async def nope(thetornadoteam):
    tornado = thetornadoteam.pattern_match.group(1)
    if not tornado:
        if thetornadoteam.is_reply:
            (await thetornadoteam.get_reply_message()).message
        else:
            await edit_or_reply(thetornadoteam, "`Sir please give some query to search and download it for you..!`"
            )
            return

    troll = await bot.inline_query("animedb_bot", f"{(deEmojify(tornado))}")

    await troll[0].click(
        thetornadoteam.chat_id,
        reply_to=thetornadoteam.reply_to_msg_id,
        silent=True if thetornadoteam.is_reply else False,
        hide_via=True,
    )
    await thetornadoteam.delete()
    

CmdHelp("anime").add_command(
  "anime", "<anime name>", "Searches for the given anime and sends the details."
).add()
