import re
import json
import time

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
  'update_id': 515620854
  'message': {
    'message_id': 1022
    'from': {
      'id': 51914389
      'is_bot': False
      'first_name': 'Fulvio'
      'username': 'FullView'
      'language_code': 'en'
      },
      'chat': {
        'id': 51914389,
        'first_name': 'Fulvio',
        'username': 'FullView',
        'type': 'private'},
        'date': 1592471797,
        'text': '/find maxi eroe',
        'entities': [
          {
            'offset': 0,
            'length': 5,
            'type': 'bot_command'
          }
        ]
      }
    }
  }
},
{
  'update_id': 515620855, 
  'edited_message': {
    'message_id': 1022,
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
    'date': 1592471797,
    'edit_date': 1592471806,
    'text': '/find eroe',
    'entities': [
      {
        'offset': 0,
        'length': 5,
        'type': 'bot_command'
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
    self.num_next = 0
    self.title_index = 0


  def dispatchAction(self, update: Update):
    message = Message(update.message if update.message else update.edited_message)
    if message.entities:
      for entity in message.entities:
        entity = MessageEntity(entity)
        if entity.isCommand:
          if any(command for command in ['/find', '/cerca'] if command in message.text):
            self.find(message)
          elif '/movie' in message.text:
            self.showMovieUrl(message)
          elif '/series' in message.text:
            self.index = message.text.replace('/series', '')
            self.showSeriesEpisodes(message, self.index)
          elif '/ep' in message.text:
            self.showEpisodeUrl(message)
          elif '/next' in message.text:
            self.num_next += 1
            self.showSeriesEpisodes(message, self.index, True)
          

  def find(self, msg: Message):
    query = re.sub(r"^/\w+ (.+)", r'\g<1>', msg.text)
    chat = Chat(msg.chat)
    username = f' as [{chat.username}]' if chat.username else ''
    self.appendToSearchesFile(f'{chat.first_name}{username} is looking for: "{query}"\n')
    if len(query) > 1:
      founds = self.mes.getTitleList(query)
      if len(founds):
        # print(json.dumps(founds[:5], indent=2))
        if hasattr(msg, 'chat'):
          pass
          results = ''
          for i, title in enumerate(founds[:8]):
            results += f'/{"series" if self.mes.isSeries(i) else "movie"}<b>{i+1}</b> {title[0]}\n\n'
          
          msg = {
            'chat_id': Chat(msg.chat).id,
            'text': results,
            'parse_mode': 'HTML',
          }
          self.bot.sendMessage(msg)
      else:
        self.bot.sendMessage({
          'chat_id': Chat(msg.chat).id,
          'text': 'No results were found',
        })


  def showSeriesEpisodes(self, msg, index, isNext = False):
    list_episode = self.mes.getEpisodeList(int(index))
    results = ''
    chat = Chat(msg.chat)
    username = f' as [{chat.username}]' if chat.username else ''
    self.appendToSearchesFile(f'{chat.first_name}{username} - series {index}\n')

    start = 0 if not isNext else self.num_next * 24
    for i, ep in enumerate(list_episode[start : start+24]):
      results += f'/ep<b>{i+start+1}</b> {ep[0]}\n\n'
    if len(list_episode[start : start+24]) == 24:
      results += '/next episodes'
    self.bot.sendMessage({
      'chat_id': chat.id,
      'text': results,
      'parse_mode': 'HTML'
    })


  def showMovieUrl(self, msg: Message):
    index = int(msg.text.replace('/movie', '')) - 1
    chat = Chat(msg.chat)
    try:
      self.bot.sendMessage({
        'chat_id': chat.id,
        'text': f'<a href="{self.mes.list_title[int(index)][1]}">{self.mes.list_title[int(index)][0]}</a>',
        'parse_mode': 'HTML'
      })
    except IndexError:
      print(f'ERROR "IndexError" in showMovieUrl for index[{index}]\n{self.mes}')
      self.bot.sendMessage({
        'chat_id': chat.id,
        'text': f'Error occurred, you\'re selecting a wrong movie number, not belonged to your last search.'
      })
  
  
  def showEpisodeUrl(self, msg: Message, isNext = False):
    index = int(msg.text.replace('/ep', '')) - 1
    chat = Chat(msg.chat)
    try:
      ep = self.mes.list_episodes[index]
      username = f' as [{chat.username}]' if chat.username else ''
      self.appendToSearchesFile(f'{chat.first_name}{username} - episode: {ep[0]}\n\n')

      self.bot.sendMessage({
        'chat_id': chat.id,
        'text': f'<a href="{self.mes.getShowUrl(index)}">{ep[0]}</a>',
        'parse_mode': 'HTML'
      })
    except IndexError:
      print(f'ERROR "IndexError" in showEpisodeUrl for index[{index}]\n{self.mes}')
      self.bot.sendMessage({
        'chat_id': chat.id,
        'text': f'Error occurred, you\'re selecting a wrong episode number, not belonged to your last search.'
      })

  def appendToSearchesFile(self, content):
    with open('searches.txt', 'a') as f:
      f.write(f'[{time.ctime()}] :: {content}')
      
  
