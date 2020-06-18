import requests
import json
import time
from typing import List, Dict, Tuple
from telegram import Config
from telegram import Update
from telegram import Message
from botvallottacinema import BotVallottaCinema

class Bot:

  def __init__(self, pathConfig):
    with open(pathConfig, 'r') as f:
      self.config = Config(json.load(f))
      self._apiUrl = f'{self.config.url}{self.config.token}'
      self._updates: List[Update]
  

  def run(self):
    lastUpdateId = self._getUpdate()[-1]['update_id']
    print('first', lastUpdateId)
    lastUpdateId = lastUpdateId + 1 if lastUpdateId > 0 else 0
    updateId = lastUpdateId
    print('init', lastUpdateId)
    self.cinema = BotVallottaCinema(self._apiUrl, self.config.idBot, self.config.commanads, self)
    time.sleep(2.5)
    
    while True:
      update = self._getUpdate(updateId)
      lastUpdateId = update[-1]['update_id']
      
      if lastUpdateId == 0:
        updateId = 0
      elif updateId == lastUpdateId:
        updateId += 1
        self._dispatchAction(update)
      else:
        self._dispatchAction(update)
        lastUpdateId += 1
        updateId = lastUpdateId
      
      time.sleep(2)


  def sendMessage(self, msg: Dict):
    req = requests.get(f'{self._apiUrl}/sendMessage', params=msg)

  def _dispatchAction(self, updates: List[Update]):
    for update in updates:
      self.cinema.dispatchAction(Update(update))


  def _getUpdate(self, offset='') -> List[Update]:
    self._updates = list(json.loads(requests.get(f'{self._apiUrl}/getUpdates?offset={offset}').text)['result'])
    if len(self._updates):
      return self._updates

    self._updates = [{'update_id':0}]
    return self._updates


  def _printUpdate(self):
    print(json.dumps(self._updates, indent=2))