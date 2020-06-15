import requests
import json
import time
from bot import Bot

# bot_details = dict()
# with open('./bot.json', 'r') as f:
#   bot_details = json.load(f)
#   print(json.dumps(bot_details, indent=2))

# API_URL = f'{bot_details["url"]}{bot_details["token"]}'
# print(API_URL)

# def startBot():
#   updates = requests.get(f'{API_URL}/getUpdates');
#   setOffset = list(json.loads(updates.text)['result'])
#   print(json.dumps(setOffset, indent=2))
#   try:
#     newUpdateId = int(setOffset[-1]['update_id']) + 1
#     # print(setOffset[-1], newUpdateId)
#     runBot(newUpdateId)
#   except (err) as err:
#     print(f'Exeption getting last update ID\n{err}')


# def runBot(newOffsetId):
  
#   while True:
#     updates = requests.get()

#     time.sleep(2.5)

# startBot()

bot = Bot('./bot.json')
bot.run()


