#!/usr/bin/env python
# This file is part of https://github.com/jainamoswal/BotStatus.
# Usage covered in < GPL-3.0 License >
# Jainam Oswal. <jainam.me> 

# import modules
import os
import re
import json
import github
import logging
import telethon
import requests
import platform
from pytz import timezone 
from datetime import datetime
from telethon.errors import MessageIdInvalidError, MessageAuthorRequiredError

print(':::::::::::::::::::::: ⏲️ Action started successfully ⏲️ ::::::::::::::::::::::')
print()
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.CRITICAL)

# define configs & default configs and blabla...
# Required :- 
bots = requests.get(os.getenv('BOTS', 'https://bit.ly/3zzCVJE')).json() # the raw link of the gist file having config data in JSON format. Use mine incase of None provided. 😂 
api_id = os.getenv('APP_ID', None) # API ID from my.telegram.org
api_hash = os.getenv('API_HASH', None) # APP hash from my.telegram.org
session = os.getenv('SESSION', None) # session string via telethon.
client = telethon.TelegramClient(telethon.sessions.StringSession(session), api_id, api_hash) # none of your business.
all_mixed_ids = os.getenv('IDS', None) # All Chat IDs along with message IDs (Telegram) to edit in format chat_id:message_id. In case of many, separate them with spaces. Eg, -100123456xxx:8x 123456xx:2xx

# Optional :-
file_name = os.getenv('FILE_NAME', 'README.md') # filename is case sensitive.
edit_in_repo = os.getenv('EDIT_IN_REPO', 'true')  # If you want to edit status in GitHub Repo, set it to True else False.
edit_in_telegram = os.getenv('EDIT_IN_TELEGRAM', 'true') # If you want to edit status in Telegram, set it to True else False
start_text = "Live status of my bots goes following ~" # default for start_message.
start_message = os.getenv('START_MESSAGE', start_text) # text before the status to show.
end_text = "**Bots status are auto-updated every 3 hours at random frequency.**" # default for end_message.
end_message = os.getenv('END_MESSAGE', end_text) # text after the status to show.
commit_message = os.getenv('COMMIT_MESSAGE', '✨ auto-updated bot status. ✨') # commit message at status update. Btw, stars looks cool.
bullet = os.getenv('BULLET', '◪') # if you want to get custom bullets in Telegram.
time_zone = os.getenv('TIME_ZONE', 'Asia/Kolkata') # ISD. You can choose different as per your location.
time_format = os.getenv('TIME_FORMAT', '%H:%M %d/%m') # Time format, defaults to Hrs:minutes Day/Month. Eg, 9:41 12/9
current_time = datetime.now(timezone(time_zone)).strftime(time_format) # Time when the script runs.
up_github = os.getenv('UP_GITHUB', '✔️') # Custom Icon when Bot is up to show in GitHub MarkDown file.
down_github = os.getenv('DOWN_GITHUB', '❌') # Custom Icon when Bot is down to show in GitHub MarkDown file.
up_telegram = os.getenv('UP_TELEGRAM', '🚀') # Custom Icon when Bot is up to show in Telegram.
down_telegram = os.getenv('DOWN_TELEGRAM', '❌') # Custom Icon when Bot is down to show in Telegram.

# print some information
def display():
    print()
    print(f"◻️ Telethon version : {telethon.__version__}") # telethon version
    print(f"◻️ Platform : {platform.system()}") # system
    print(f"◻️ Platform release : {platform.release()}") # system version
    print(f"◻️ OS version : {platform.version().split()[0]}") # OS version
    print()

# returns a list of proper formatted ids to edit in a looooooop.
def get_ids(all_mixed_ids):
    all_chats_with_ids_mix = all_mixed_ids.split(' ')
    all_chats = []
    for each in all_chats_with_ids_mix:
        all_chats.append(each.split(':'))
    return all_chats

# updates in ReadMe file at GitHub
def updateme(old, json_data, first_match, second_match):
    new = '''\n| 🤖 Bot 🤖 | ⭐️ Status ⭐️ |\n| :-: | :-: |\n'''
    for i in json_data:
        new += f"| [{json_data[i]['name']}](https://t.me/{i}) | {up_github if json_data[i]['status'] else down_github} |\n"
    new_string = f"\n{first_match}\n{new}\n`Updated last at ~ {current_time}`\n\n"
    new_string += f"**Made with ❤️ via [BotStatus](https://github.com/jainamoswal/botstatus)**. \n{second_match}" # self promotion is must ¯\_(ツ)_/¯
    return re.sub(f'\n{first_match}.*?{second_match}', new_string, old, flags=re.DOTALL)

# fetch status of all bots listed in the raw gist file
async def main():
    bot_status = {}
    async with client:
        for each_bot in bots:
            async with client.conversation(each_bot, exclusive=False) as conv:
                name = await client.get_entity(each_bot)
                try:
                    sent = await conv.send_message('/' + bots[each_bot]['start'])
                    received = await conv.get_response(timeout=bots[each_bot]['sleep'])
                    await received.delete()
                    bot_status.update({each_bot:{'name':name.first_name, 'status':True}})
                    await sent.delete()
                except Exception as e:
                    if type(e).__name__ == "YouBlockedUserError":
                        print(f'🚧 You\'ve blocked @{each_bot}. Please unblock it, until next run, I\'ll mark it as down. 🚧') # you blocked the bot :(
                    bot_status.update({each_bot:{'name':name.first_name, 'status':False}}) # bot didn't replied back :(      
        return bot_status

# edit the message with status at telegram
async def edit_message(data):
    async with client:
        text = f'{start_message}\n' # I love f-strings and to comment every line :)
        for i in data:
            text += f"{bullet} [{data[i]['name']}](https://t.me/{i}) ~ {up_telegram if data[i]['status'] else down_telegram}\n"
        text += f"\n**Last Checked:** \n__{current_time}__\n"
        text += end_message
        chats_to_edit = get_ids(all_mixed_ids)
        for chat_id, message_id in chats_to_edit:
            try:
                await client.edit_message(int(chat_id), int(message_id), text, link_preview=False)
            except MessageIdInvalidError:
                print(f'Provided message ID ({message_id}) is invalid of chat ({chat_id}), Maybe message Id representing the Message is Deleted or was not sent before.')
            except MessageAuthorRequiredError:
                print(f'You don\'t have enough rights to edit this message.\n Chat : {chat_id} with Message {message_id}')

# pastes the JSON output to spaceb.in/ and returns the raw link
def PasteMe(json=None):
    url="https://spaceb.in/api/v1/documents/"
    json={"content": str(json), "extension": "txt"}
    req = requests.post(url, json=json, verify=False) 
    returnMe =  url + req.json()['payload']['id'] + "/raw"
    return returnMe

# run the script via __main__ style
if __name__ == '__main__':
    json_data = client.loop.run_until_complete(main())
    os.system(f'echo \"output={PasteMe(json=json_data)}\" >> $GITHUB_ENV') # sets JSON data as output, so that you can use the json data for other use also.
    display()
    for each in json_data:
        print(f"🔸 {json_data[each]['name']} [@{each}] is {'🟢' if json_data[each]['status'] else '🔴'}")
    if edit_in_telegram.lower() == "true":
        client.loop.run_until_complete(edit_message(json_data))
    if edit_in_repo.lower() == "true":
        repo = github.Github(os.getenv('GITHUB_TOKEN')).get_repo(os.getenv('GITHUB_REPOSITORY'))
        contents = repo.get_contents(file_name) 
        repo.update_file(file_name, commit_message, updateme(contents.decoded_content.decode(), json_data, '<start>', '<end>'), contents.sha)

print()
print('::::::::::::::::::::: 🎉 Action completed successfully 🎉 :::::::::::::::::::::')
print('Mind joining @j_projects at Telegram and do follow me on github.com <jainamoswal>')
