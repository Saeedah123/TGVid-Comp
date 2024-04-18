from config import Config
import traceback
from helper.database import db
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os
import sys
import time
import asyncio
import logging
import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(
        time.time() - Config.BOT_UPTIME))
    start_t = time.time()
    st = await message.reply('**Accessing The Details.....**')
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Bot Status--** \n\n**⌚️ Bot Uptime:** {uptime} \n**🐌 Current Ping:** `{time_taken_s:.3f} ms` \n**👭 Total Users:** `{total_users}`")


# Restart to cancell all process
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    await m.reply_text("🔄__Restarting.....__")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} Is Started The Broadcast......")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Broadcast Started..!")
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['id'], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            await db.delete_user(user['id'])
        done += 1
        if not done % 20:
            await sts_msg.edit(f"Broadcast In Progress: \nTotal Users {total_users} \nCompleted: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFailed: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Broadcast Completed: \nCompleted In `{completed_in}`.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFailed: {failed}")


async def send_msg(user_id, message):
    try:
        await message.forward(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Deactivated")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Blocked The Bot")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : User Id Invalid")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500


@Client.on_message(filters.private & filters.command("ban_user") & filters.user(Config.ADMIN))
async def ban(c: Client, m: Message):

    if len(m.command) == 1:
        await m.reply_text(
            f"Use This Command To Ban Any User From The Bot.\n\n"
            f"Usage:\n\n"
            f"`/ban_user user_id ban_duration ban_reason`\n\n"
            f"Eg: `/ban_user 1234567 28 You misused me.`\n"
            f"This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"Banning User {user_id} For {ban_duration} Days For The Reason {ban_reason}."
        try:
            await c.send_message(
                user_id,
                f"You Are Banned To Use This Bot For **{ban_duration}** day(s) For The Reason __{ban_reason}__ \n\n"
                f"**Message From The Admin**"
            )
            ban_log_text += '\n\nUser Notified Successfully!'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nUser Notification Failed! \n\n`{traceback.format_exc()}`"

        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error Occoured! Traceback Given Below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("unban_user") & filters.user(Config.ADMIN))
async def unban(c: Client, m: Message):

    if len(m.command) == 1:
        await m.reply_text(
            f"Use This Command To Unban Any User.\n\n"
            f"Usage:\n\n`/unban_user user_id`\n\n"
            f"Eg: `/unban_user 1234567`\n"
            f"This Will Unban User With Id `1234567`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning User {user_id}"
        try:
            await c.send_message(
                user_id,
                f"Your Ban Was Lifted!"
            )
            unban_log_text += '\n\nUser Notified Successfully!'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error Occurred! Traceback Given Below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("banned_users") & filters.user(Config.ADMIN))
async def _banned_users(_, m: Message):

    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''

    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"> **user_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, " \
                f"**Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total Banned User(s): `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)
    
