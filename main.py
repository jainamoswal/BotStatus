# This file is part of https://github.com/jainamoswal/BotStatus.
# Usage covered in < GPL-3.0 License >
# Jainam Oswal. <jainam.me> 

# import modules
import os, logging, asyncio, re, github, requests, platform
from pytz import timezone 
from datetime import datetime
import telethon

print(':::::::::::::::::::::: ⏲️ Action started successfully ⏲️ ::::::::::::::::::::::')
print()
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.CRITICAL)

# define configs
bots = requests.get(os.getenv('BOTS')).json() # the raw link of the gist file having config data in JSON format
api_id = os.getenv('APP_ID') # API ID from my.telegram.org
api_hash = os.getenv('API_HASH') # APP hash from my.telegram.org
session = os.getenv('SESSION') # session string via telethon
client = telethon.TelegramClient(telethon.sessions.StringSession(session), api_id, api_hash) # none of your bussiness 
file_name = 'README.md' if os.getenv('FILE_NAME') is None else os.getenv('FILE_NAME')  # filename is case sensitive

# print some information
def display():
  print()
  print(f"◻️ Telethon version : {telethon.__version__}") # telethon version
  print(f"◻️ Platform : {platform.system()}") # system
  print(f"◻️ Platform release : {platform.release()}") # system version
  print(f"◻️ OS version : {platform.version().split()[0]}") # OS version
  print()

# updates in ReadMe file at github
def updateme(old, json_data, first_match, second_match):
    new = '''\n| 🤖 Bot 🤖 | ⭐️ Status ⭐️ |\n| :-: | :-: |\n'''
    for i in json_data:
        new += f"| [{json_data[i]['name']}](https://t.me/{i}) | {'✔️' if json_data[i]['status'] else '❌'} |\n"
    new_string = f"\n{first_match}\n{new}\n`Updated last at ~ {datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M:%S on %Y-%m-%d ')} INR` 🏳️‍🌈\n\n"
    new_string += f"**Made with ❤️ via [BotStatus](https://github.com/jainamoswal/botstatus)**. \n{second_match}"
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
        text = 'Live status of my bots goes following ~\n'
        for i in data:
            text += f"🔅 [{data[i]['name']}](https://t.me/{i}) ~ {'🚀' if data[i]['status'] else '❌'}\n"
        text += f"\n**Last Checked:** \n__{datetime.now(timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')} IST__\n\n**Bots status are auto-updated every 3 hours at random frequency.**\n\n[J Projects](https://t.me/J_Projects)"
        await client.edit_message(int(os.getenv('CHANNEL_ID')), int(os.getenv('MESSAGE_ID')), text, link_preview=False)

# run the script via __main__ style
if __name__ == '__main__':
    json_data = client.loop.run_until_complete(main())
    display()
    for each in json_data:
        print(f"🔸 {json_data[each]['name']} [@{each}] is {'🟢' if json_data[each]['status'] else '🔴'}")
    client.loop.run_until_complete(edit_message(json_data))
    repo = github.Github(os.getenv('GITHUB_TOKEN')).get_repo(os.getenv('GITHUB_REPOSITORY'))
    contents = repo.get_contents(file_name) 
    repo.update_file(file_name, "✨ auto-updated bot status. ✨", updateme(contents.decoded_content.decode(), json_data, '<start>', '<end>'), contents.sha)

print()
print('::::::::::::::::::::: 🎉 Action completed successfully 🎉 :::::::::::::::::::::')
print('Mind joining @j_projects at Telegram and do follow me on github.com <jainamoswal>')