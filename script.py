class Txt(object):

    PRIVATE_START_MSG = """
Hi {},

I'm Video Encoder Bot Can Can Compress Your Video To Negligible Size Without Loosing The Qualities Just Send Me Video
"""
    GROUP_START_MSG = """
Hi {},

I'm Video Encoder Bot Can Can Compress Your Video To Negligible Size Without Loosing The Qualities Just Send Me Video

❗**You Hasn't Started Me Yet To Use Me First Start Me So I Can Work Flawlessly**
"""
    PROGRESS_BAR = """<b>
╭━━━━❰Progress Bar❱━➣
┣⪼ 🗃️ Size: {1} | {2}
┣⪼ ⏳️ Done: {0}%
┣⪼ 🚀 Speed: {3}/s
┣⪼ ⏰️ Eta: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""

    SEND_FFMPEG_CODE = """
❪ Set Custom Ffmpeg Code ❫

Send me the correct ffmpeg code for more info.


☛ <a href=https://unix.stackexchange.com/questions/28803/how-can-i-reduce-a-videos-size-with-ffmpeg#:~:text=ffmpeg%20%2Di%20input.mp4%20%2Dvcodec%20libx265%20%2Dcrf%2028%20output.mp4> For Help </a>

⦿ Fᴏʀᴍᴀᴛ Oɴ Hᴏᴡ Tᴏ Sᴇᴛ

☞ ffmpeg -i input.mp4 <code> -c:v libx264 -crf 23 </code> output.mp4

<code> -c:v libx264 -crf 23 </code> This Is Your Ffmpeg Code ✅

📥 For Help Join. @KingBjssChat
"""

    SEND_METADATA ="""
❪ SET CUSTOM METADATA ❫

☞ For Example:-

◦ <code> -map 0 -c:s copy -c:a copy -c:v copy -metadata title="My Video" -metadata author="John Doe" -metadata:s:s title="Subtitle Title" -metadata:s:a title="Audio Title" -metadata:s:v title="Video Title" </code>

📥 For Help Join. @KingBjssChat
"""

    
    HELP_MSG = """
Available Commands:-

➜ /set_ffmpeg - To set custom ffmpeg code
➜ /set_metadata - To set custom metadata code
➜ /set_caption - To set custom caption
➜ /del_ffmpeg - Delete the custom ffmpeg code
➜ /del_caption - Delete caption
➜ /see_ffmpeg - View custom ffmpeg code
➜ /see_metadata - View custom metadata code
➜ /see_caption - View caption 
➜ To Set Thumbnail just send photo

<b>⦿ Developer:</b> <a href=https://t.me/KingBjss>King Bjss ❄️</a>
"""

    ABOUT_TXT = """<b>╭───────────⍟
├🤖 My Name: @{}
├👨‍💻 Programmer: <a href=https://t.me/KingBjss>King Bjss</a>
├📕 Library: <a href=https://github.com/pyrogram>Pyrogram</a>
├✏️ Language: <a href=https://www.python.org>Python3</a>
├💾 Database: <a href=https://cloud.mongodb.com>Mongo DB</a>
├🌀 My Server: <a href=https://dashboard.heroku.com>Heroku</a>
╰───────────────⍟ """
    
