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
from bot import Bot

'''
{
  'update_id': 515620855, 
  'message' OR 'edited_message': {
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

class UserRequests:
  def __init__(self, user: User, chat: Chat, cmd: str, title_selected: int = -1, episode_selected: int = -1):
    self.user_id: str = user.id
    self.chat_id: str = chat.id
    self.first_name: str = user.first_name
    self.username: str = user.username
    self.cmd: str = cmd
    self.mes: MoviesAndSeries = MoviesAndSeries()
    self.title_selected_index: int = title_selected
    self.title_selected: str = ''
    self.episode_selected: str = ''
    self.episode_list: list() = list()
    self.episode_selected_index: int = episode_selected
    self.url_show: str = ''
  def __str__(self):
    return f'''
user_id: {self.user_id}
chat_id: {self.chat_id}
first_name: {self.first_name}
username: {self.username}
cmd: {self.cmd}
title_selected_index: {self.title_selected_index}
episode_selected_index: {self.episode_selected_index}
title_selected: {self.title_selected}
episode_selected: {self.episode_selected}
url_show: {self.url_show}
'''


class BotVallottaCinema(Bot):

  def __init__(self, pathConfig):
    super().__init__(pathConfig)
    self.curr_next = 0
    self.user_requests: Dict(UserRequests) = dict()


  def _loopUpdates(self, updates: List[Update]):
    for update in updates:
      self.dispatchAction(Update(update))


  def dispatchAction(self, update: Update):
    message = Message(update.message if update.message else update.edited_message)
    user = User(message.fromUser)
    if message.entities:
      for entity in message.entities:
        entity = MessageEntity(entity)
        print('chat id ', Chat(message.chat).id, User(message.fromUser).id)
        if entity.isCommand:
          self.sendAction(Chat(message.chat).id)
          if any(command for command in ['/find', '/cerca'] if command in message.text):
            self.find(message)
          elif user.id in self.user_requests:
            try:
              if '/movie' in message.text:
                self.showMovieUrl(message)
              elif '/series' in message.text:
                index = int(message.text.replace('/series', '')) - 1
                self.user_requests[user.id].title_selected = self.user_requests[user.id].mes.list_title[index][0]
                self.showSeriesEpisodes(message, index)
              elif '/ep' in message.text:
                self.showEpisodeUrl(message)
              elif '/next' in message.text:
                self.curr_next += 1
                self.showSeriesEpisodes(message, -1, True)
            except:
              self.sendMessage(Chat(message.chat).id, 'Run a search first')
          else:
            self.sendMessage(Chat(message.chat).id, 'Run a search first')
          

  def find(self, msg: Message):
    query = re.sub(r"^/\w+ (.+)", r'\g<1>', msg.text)
    chat = Chat(msg.chat)
    user = User(msg.fromUser)
    username = f' as [{chat.username}]' if chat.username else ''
    self.user_requests[user.id] = UserRequests(user, chat, msg.text)
    self.appendToSearchesFile(f'{chat.first_name}{username} is looking for: "{query}"\n', True)
    if len(query) > 1:
      self.user_requests[user.id].mes = MoviesAndSeries()
      founds = self.user_requests[user.id].mes.getTitleList(query)
      if len(founds):
        if hasattr(msg, 'chat'):
          pass
          results = ''
          for i, title in enumerate(founds[:10]):
            results += f'/{"series" if self.user_requests[user.id].mes.isSeries(i) else "movie"}<b>{i+1}</b> {title[0]}\n\n'
          self.sendMessage(chat.id, results, 'HTML')
      else:
        self.sendMessage(chat.id, 'No results were found')


  def showMovieUrl(self, msg: Message):
    index = int(msg.text.replace('/movie', '')) - 1
    chat = Chat(msg.chat)
    user = User(msg.fromUser)
    try:
      txt = f'<a href="{self.user_requests[user.id].mes.list_title[index][1]}">{self.user_requests[user.id].mes.list_title[index][0]}</a>'
      self.user_requests[user.id].title_selected_index = index
      self.user_requests[user.id].title_selected = self.user_requests[user.id].mes.list_title[index][0]
      self.user_requests[user.id].url_show = self.user_requests[user.id].mes.list_title[index][1]
      self.sendMessage(chat.id, txt, 'HTML')
      self.appendToSearchesFile(f'{self.user_requests[user.id]}', True, startWith='\n\n')
    except IndexError:
      print(f'ERROR "IndexError" in showMovieUrl for index[{index}]\n{self.user_requests[user.id].mes}')
      self.sendMessage(chat.id, f'Error occurred, you\'re selecting a wrong movie number, not belonged to your last search.')
      

  def showSeriesEpisodes(self, msg, index: int, isNext = False):
    results = ''
    user = User(msg.fromUser)
    chat = Chat(msg.chat)
    username = f' as [{self.user_requests[user.id].username}]' if self.user_requests[user.id].username else ''
    episode_list = list()
    if isNext:
      start = self.curr_next * 24
      episode_list = self.user_requests[user.id].episode_list
      self.appendToSearchesFile(f'{self.user_requests[user.id].first_name}{username} - page {self.curr_next}\n', True)
    else:
      episode_list = self.user_requests[user.id].mes.getEpisodeList(index)
      self.user_requests[user.id].episode_list = episode_list
      self.user_requests[user.id].title_selected_index = index
      start = 0
      self.appendToSearchesFile(f'{self.user_requests[user.id].first_name}{username} - series {index}\n', True)
    
    for i, ep in enumerate(episode_list[start : start+24]):
      results += f'/ep<b>{i+start+1}</b> {ep[0]}\n\n'
    if len(episode_list[start : start+24]) == 24:
      results += '/next episodes'
    self.sendMessage(chat.id, results, 'HTML')


  def showEpisodeUrl(self, msg: Message, isNext = False):
    index = int(msg.text.replace('/ep', '')) - 1
    chat = Chat(msg.chat)
    user = User(msg.fromUser)
    try:
      ep = self.user_requests[user.id].mes.list_episodes[index]
      self.user_requests[user.id].episode_selected_index = index
      self.user_requests[user.id].episode_selected = ep[0]
      url_show = self.user_requests[user.id].mes.getShowUrl(index)
      self.user_requests[user.id].url_show = url_show
      self.appendToSearchesFile(f'{self.user_requests[user.id]}', True, startWith='\n\n')
      msg = f'<a href="{url_show}">{ep[0]}</a>',
      self.sendMessage(chat.id, msg, 'HTML')
    except IndexError:
      print(f'ERROR "IndexError" in showEpisodeUrl for index[{index}]\n{self.user_requests[user.id].mes}')
      self.sendMessage(chat.id, f'Error occurred, you\'re selecting a wrong episode number, not belonged to your last search.')


  def appendToSearchesFile(self, content, atBeginning = False, startWith = ''):
    if not atBeginning:
      with open('searches.txt', 'a') as f:
        f.write(f'[{time.ctime()}] :: {content}')
    else:
      with open('searches.txt', 'r+') as f:
        file_content = f.read()
        f.seek(0, 0)
        f.write(f'{startWith}[{time.ctime()}] :: {content}{file_content}')
      
  
