from telegram import Update
from telegram import Chat
from telegram import Message
from telegram import User
from telegram import Chat
from telegram import MessageEntity
from telegram import PhotoSize

'''
{
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
'''

class Dispatcher:

  def __init__(self, update: Update):
    self.update = update
    self.dispatch()


  def dispatch(self):
    message = Message(self.update.message)
    if message.entities:
      pass