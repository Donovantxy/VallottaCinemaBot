import re
import json

from typing import List, Dict, Tuple
from telegram import Config
from telegram import Update
from telegram import Chat
from telegram import Message
from telegram import User
from telegram import Chat
from telegram import MessageEntity
from telegram import PhotoSize
from moviesandseries import MoviesAndSeries

'''
{
  'update_id': 515620412,
  'message': {
    'message_id': 311,
    'from': {
      'id': 51914389,
      'is_bot': False,
      'first_name': 'Fulvio',
      'username': 'FullView',
      'language_code': 'en'
    },
    'chat': {
      'id': 51914389,
      'first_name': 'Fulvio',
      'username': 'FullView',
      'type': 'private'
    }, 
    'date': 1592303433,
    'text': '/find Batman',
    'entities': [
      {
        'offset': 0, 'length': 5, 'type': 'bot_command'
      }
    ]
  }
}
'''

class BotVallottaCinema:

  def __init__(self, baseApiUrl: str, idBot: str, commands: List[str], bot):
    # print(update)
    self.baseApiUrl = baseApiUrl
    self.idBot = idBot
    self.commands = commands
    self.bot = bot
    self.mes = MoviesAndSeries()


  def dispatchAction(self, update: Update):
    # print(22, self.update)
    message = Message(update.message)
    # print(message)#, message.message_id, message.chat)
    if message.entities:
      for entity in message.entities:
        entity = MessageEntity(entity)
        if entity.isCommand:
          if any(command for command in ['/find', '/cerca'] if command in message.text):
            self.find(message)
          

  def find(self, msg: Message):
    query = re.sub(r"^/\w+ (.+)", r'\g<1>', msg.text)
    print(f'FIND: "{query}"')
    if len(query) > 1:
      founds = self.mes.getTitleList(query)
      if len(founds):
        print(json.dumps(founds[:10], indent=2))
        if hasattr(msg, 'chat'):
          self.bot.sendMessage('test message', Chat(msg.chat).id)
        # return self.mes.list_title[:10]
      else:
        print('No results were found')
        # result = self.notFoundMsg


  
