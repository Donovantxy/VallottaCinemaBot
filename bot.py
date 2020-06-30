import requests
import json
import time
import datetime
from typing import List, Dict, Tuple
from telegram import Config
from telegram import Update
from telegram import Message
from telegram import User



class Bot:

  def __init__(self, pathConfig, timingForChekingUpdates: int = 2):
    with open(pathConfig, 'r') as f:
      self._config = Config(json.load(f))
      self._apiUrl = f'{self._config.url}{self._config.token}'
      self._commands = self._config.commands
      self._updates: List[Update]
      self._timingForChekingUpdates = timingForChekingUpdates
  

  def run(self):
    lastUpdateId = self._getUpdate()[-1]['update_id']
    print('first', lastUpdateId)
    lastUpdateId = lastUpdateId + 1 if lastUpdateId > 0 else 0
    updateId = lastUpdateId
    print('init', lastUpdateId)
    time.sleep(self._timingForChekingUpdates)
    
    while True:
      update = self._getUpdate(updateId)
      lastUpdateId = update[-1]['update_id']
      
      if lastUpdateId == 0:
        updateId = 0
      elif updateId == lastUpdateId:
        updateId += 1
        self._loopUpdates(update)
      else:
        self._loopUpdates(update)
        lastUpdateId += 1
        updateId = lastUpdateId
      
      time.sleep(self._timingForChekingUpdates)


  def sendAction(self, chat_id: str, action: str = 'typing'):
    requests.get(f'{self._apiUrl}/sendChatAction', params={
      'chat_id': chat_id,
      'action': action
    })
    

  def sendMessage(self, chat_id: str, msg: str, parse_mode: str = ''):
    requests.get(f'{self._apiUrl}/sendMessage', params={
      'chat_id': chat_id,
      'text': msg,
      'parse_mode': parse_mode
    })

  

  def _getUpdate(self, offset='') -> List[Update]:
    self._updates = list(json.loads(requests.get(f'{self._apiUrl}/getUpdates?offset={offset}').text)['result'])
    if len(self._updates):
      return self._updates

    self._updates = [{'update_id':0}]
    return self._updates


  def _printUpdate(self):
    print(json.dumps(self._updates, indent=2))
 
  def _sendAnalytics(self, category: str, action: str, label: str, user: User):
    name = user.first_name
    now = datetime.datetime.now()
    now = f'[{now.day}/{now.month}/{str(now.year)[2:]} {now.hour}:{now.minute}:{now.second}]'
    # now = ''
    if user.username:
      name += f'[{user.username}]'
    # payload = f'ec={category}&ea={action}&el={name}: {label}'
    query_params = {
      'v': '1',
      't': 'event',
      'tid': self._config.ga_tracking_id,
      'cid': '555',
      'ec': category,
      'ea': action,
      'el': f'{now}{name}: {label}',
      'dp': '/'
    }
    r = requests.post('https://www.google-analytics.com/collect', params=query_params)
    print(r.text)
    print(f'[{now}]{name}: {label}')


  # _loopUpdates must be implemented in subclasses
  def _loopUpdates(self, updates: List[Update]):
    pass
  