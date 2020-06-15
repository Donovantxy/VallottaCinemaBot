from typing import List, Dict, Tuple

class Update(object):
  def __init__(self, update = None, update_id=0):
    self.update_id: int = update['update_id']
    self.message: Message = update['message'] if 'message' in update else None
    self.edited_message: Message = update['edited_message'] if 'edited_message' in update else None
    self.channel_post: Message = update['channel_post'] if 'channel_post' in update else None
    self.edited_channel_post: Message = update['edited_channel_post'] if 'edited_channel_post' in update else None
  
  def __str__(self):
    try:
      return f'Update: {self.update_id} - {Message(self.message).text} by {self.message["from"]["id"]}'
    except:
      return f'ERROR -> Update: {self.update_id}'
  

class Message(object):
  def __init__(self, message = None):
    self.message_id: int = message['message_id'] if 'message_id' in message else None
    self.fromUser: User  = message['from'] if 'from' in message else None
    self.date: int = message['date'] if 'date' in message else None
    self.chat: Chat = message['chat'] if 'chat' in message else None
    self.forward_from: User = message['forward_from'] if 'forward_from' in message else None
    self.forward_from_chat: Chat = message['forward_from_chat'] if 'forward_from_chat' in message else None
    self.forward_from_message_id: int = message['forward_from_message_id'] if 'forward_from_message_id' in message else None
    self.forward_signature: str = message['forward_signature'] if 'forward_signature' in message else None
    self.forward_sender_name: str = message['forward_sender_name'] if 'forward_sender_name' in message else None
    self.forward_date: int = message['forward_date'] if 'forward_date' in message else None
    self.reply_to_message: Message = message['reply_to_message'] if 'reply_to_message' in message else None
    self.via_bot: User = message['via_bot'] if 'via_bot' in message else None
    self.edit_date: int = message['edit_date'] if 'edit_date' in message else None
    self.media_group_id: str = message['media_group_id'] if 'media_group_id' in message else None
    self.author_signature: str = message['author_signature'] if 'author_signature' in message else None
    self.text: str = message['text'] if 'text' in message else None
    self.entities: List[MessageEntity] = message['entities'] if 'entities' in message else None
    self.animation: Animation = message['animation'] if 'animation' in message else None
    self.audio: Audio = message['audio'] if 'audio' in message else None
    self.document: Document = message['document'] if 'document' in message else None
    self.photo: List[PhotoSize] = message['photo'] if 'photo' in message else None
    self.sticker: Sticker = message['sticker'] if 'sticker' in message else None
    self.video: Video = message['video'] if 'video' in message else None
    self.video_note: VideoNote = message['video_note'] if 'video_note' in message else None
    self.voice: Voice = message['voice'] if 'voice' in message else None
    self.caption: str = message['caption'] if 'caption' in message else None
    self.caption_entities: List[MessageEntity] = message['caption_entities'] if 'caption_entities' in message else None
    self.contact: Contact = message['contact'] if 'contact' in message else None
    self.dice: Dice = message['dice'] if 'dice' in message else None
    self.game: Game = message['game'] if 'game' in message else None
    self.poll: Poll = message['poll'] if 'poll' in message else None
    self.venue: Venue = message['venue'] if 'venue' in message else None
    self.location: Location = message['location'] if 'location' in message else None
    self.new_chat_members: List[User] = message['new_chat_members'] if 'new_chat_members' in message else None
    self.left_chat_member: User = message['left_chat_member'] if 'left_chat_member' in message else None
    self.new_chat_title: str = message['new_chat_title'] if 'new_chat_title' in message else None
    self.new_chat_photo: List[PhotoSize] = message['new_chat_photo'] if 'new_chat_photo' in message else None
    self.delete_chat_photo: True = message['delete_chat_photo'] if 'delete_chat_photo' in message else None
    self.group_chat_created: True = message['group_chat_created'] if 'group_chat_created' in message else None
    self.supergroup_chat_created: True = message['supergroup_chat_created'] if 'supergroup_chat_created' in message else None
    self.channel_chat_created: True = message['channel_chat_created'] if 'channel_chat_created' in message else None
    self.migrate_to_chat_id: int = message['migrate_to_chat_id'] if 'migrate_to_chat_id' in message else None
    self.migrate_from_chat_id: int = message['migrate_from_chat_id'] if 'migrate_from_chat_id' in message else None
    self.pinned_message: Message = message['pinned_message'] if 'pinned_message' in message else None
    self.invoice: Invoice = message['invoice'] if 'invoice' in message else None
    self.successful_payment: SuccessfulPayment = message['successful_payment'] if 'successful_payment' in message else None
    self.connected_website: str = message['connected_website'] if 'connected_website' in message else None
    self.passport_data: PassportData = message['passport_data'] if 'passport_data' in message else None
    self.reply_markup: InlineKeyboardMarku = message['reply_markup'] if 'reply_markup' in message else None
  
class User:
  def __init__(self, user = None):
    self.id: int = user['id'] if 'id' in user else None
    self.is_bot: bool = user['is_bot'] if 'is_bot' in user else None
    self.first_name: str = user['first_name'] if 'first_name' in user else None
    self.last_name: str = user['last_name'] if 'last_name' in user else None
    self.username: str = user['username'] if 'username' in user else None
    self.language_code: str = user['language_code'] if 'language_code' in user else None
    self.can_join_groups: bool = user['can_join_groups'] if 'can_join_groups' in user else None
    self.can_read_all_group_messages: bool = user['can_read_all_group_messages'] if 'can_read_all_group_messages' in user else None
    self.supports_inline_queries: bool = user['supports_inline_queries'] if 'supports_inline_queries' in user else None

class Chat:
  def __int__(self, chat = None):
    self.id: int = chat['id'] if 'id' in chat else None
    self.type: str = chat['type'] if 'type' in chat else None
    self.title: str = chat['title'] if 'title' in chat else None
    self.username: str = chat['username'] if 'username' in chat else None
    self.first_name: str = chat['first_name'] if 'first_name' in chat else None
    self.last_name: str = chat['last_name'] if 'last_name' in chat else None
    self.photo: ChatPhoto = chat['photo'] if 'photo' in chat else None
    self.description: str = chat['description'] if 'description' in chat else None
    self.invite_link: str = chat['invite_link'] if 'invite_link' in chat else None
    self.pinned_message: Message = Message(chat['pinned_message']) if 'pinned_message' in chat else None
    self.permissions: ChatPermissions = chat['permissions'] if 'permissions' in chat else None
    self.slow_mode_delay: int = chat['slow_mode_delay'] if 'slow_mode_delay' in chat else None
    self.sticker_set_name: str = chat['sticker_set_name'] if 'sticker_set_name' in chat else None
    self.can_set_sticker_set: bool = chat['can_set_sticker_set'] if 'can_set_sticker_set' in chat else None

class MessageEntity:
  def __init__(self, messageentity = None):
    self.type: str = messageentity['type'] if 'type' in messageentity else None
    self.offset: int = messageentity['offset'] if 'offset' in messageentity else None
    self.length: int = messageentity['length'] if 'length' in messageentity else None
    self.url: str = messageentity['url'] if 'url' in messageentity else None
    self.user: User = User(messageentity['user']) if 'user' in messageentity else None
    self.language: str = messageentity['language'] if 'language' in messageentity else None

class PhotoSize:
  def __init__(self):
    self.file_id: str
    self.file_unique_id: str
    self.width: int
    self.height: int
    self.file_size: int

class Animation:
  pass

class Audio:
  pass

class Document:
  pass

class Sticker:
  pass

class Video:
  pass

class VideoNote:
  pass

class Voice:
  pass

class Contact:
  pass

class Dice:
  pass

class Game:
  pass

class Poll:
  pass

class Venue:
  pass

class Location:
  pass

class Invoice:
  pass

class SuccessfulPayment:
  pass

class PassportData:
  pass

class InlineKeyboardMarku:
  pass

class ChatPhoto:
  pass

class ChatPermissions:
  pass