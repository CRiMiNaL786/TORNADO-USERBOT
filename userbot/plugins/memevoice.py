# Credits to @spechide and his team for @TROLLVOICEBOT
# made by @thetornadoteam_the_badass from the snippets of waifu AKA stickerizerbot....
# kang karega kya madarchod?
# aukaat h bsdk teri...jake baap ka loda chus ke aa....


import re

from userbot import bot
from tornadobot.utils import admin_cmd, sudo_cmd, edit_or_reply
from userbot.cmdhelp import CmdHelp
from userbot.helpers.functions import deEmojify


@bot.on(admin_cmd(pattern="mev(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="mev(?: |$)(.*)", allow_sudo=True))
async def nope(thetornadoteam):
    tornado = thetornadoteam.pattern_match.group(1)
    if not tornado:
        if thetornadoteam.is_reply:
            (await thetornadoteam.get_reply_message()).message
        else:
            await edit_or_reply(thetornadoteam, "`Sir please give some query to search and download it for you..!`"
            )
            return

    troll = await bot.inline_query("TrollVoiceBot", f"{(deEmojify(tornado))}")

    await troll[0].click(
        thetornadoteam.chat_id,
        reply_to=thetornadoteam.reply_to_msg_id,
        silent=True if thetornadoteam.is_reply else False,
        hide_via=True,
    )
    await thetornadoteam.delete()
    

CmdHelp("memevoice").add_command(
  "mev", "<meme txt>", "Searches and uploads the meme in voice format (if any)."
).add()
