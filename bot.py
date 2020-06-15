import requests
import json
import time
from typing import List, Dict, Tuple
from telegram import Update
from telegram import Message

class Bot:

  def __init__(self, pathConfig):
    with open(pathConfig, 'r') as f:
      config = json.load(f)
      self._apiUrl = f'{config["url"]}{config["token"]}'
      self._updates: List[Update]
      print(json.dumps(config, indent=2))
  
  def run(self):
    lastUpdateId = self._getUpdate()[-1]['update_id']
    print('first', lastUpdateId)
    lastUpdateId = lastUpdateId + 1 if lastUpdateId > 0 else 0
    updateId = lastUpdateId
    print('init', lastUpdateId)
    time.sleep(2.5)
    
    while True:
      update = self._getUpdate(updateId)
      lastUpdateId = update[-1]['update_id']
      
      if lastUpdateId == 0:
        updateId = 0
      elif updateId == lastUpdateId:
        updateId += 1
        self._dispatchEvent(update)
      else:
        self._dispatchEvent(update)
        lastUpdateId += 1
        updateId = lastUpdateId
        # print(3, updateId, update)
      
      time.sleep(2)

  def _dispatchEvent(self, updates: List[Update]):
    # print(updates)
    for update in updates:
      update = Update(update)
      print(update)
  
  def _getUpdate(self, offset='') -> List[Update]:
    self._updates = list(json.loads(requests.get(f'{self._apiUrl}/getUpdates?offset={offset}').text)['result'])
    if len(self._updates):
      return self._updates

    self._updates = [{'update_id':0}]
    return self._updates

  def _printUpdate(self):
    print(json.dumps(self._updates, indent=2))