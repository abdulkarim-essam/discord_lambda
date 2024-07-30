from urllib3 import PoolManager
from .user import User
from .messages import Message
import typing
import json
from .components import ActionRow



class InteractionMetadata:
      id: str
      type: int
      user_id: str
      user: typing.Union[User, None]
      authorizing_integration_owners: dict
      interacted_message_id: str

      def __init__(self, **kwargs):
          self.id = kwargs.get('id')
          self.type = kwargs.get('type')
          self.user_id = kwargs.get('user_id')
          self.user = User(**kwargs.get('user')) if kwargs.get('user') else None
          self.authorizing_integration_owners = kwargs.get('authorizing_integration_owners')
          self.interacted_message_id = kwargs.get('interacted_message_id')

class Interaction:
    application_id: str
    token: str
    channel_id: str
    content: str
    attachments: list
    embeds: list
    timestamp: str
    id: str
    edited_timestamp: str
    author: User
    webhook_id: str
    message_reference: Message
    position: int
    interaction_metadata: InteractionMetadata



    def __init__(self, **kwargs):
        self.application_id = kwargs.get('application_id')
        self.token = kwargs.get('token')
        self.channel_id = kwargs.get('channel_id')
        self.content = kwargs.get('content')
        self.attachments = kwargs.get('attachments')
        self.embeds = kwargs.get('embeds')
        self.timestamp = kwargs.get('timestamp')
        self.id = kwargs.get('id')
        self.edited_timestamp = kwargs.get('edited_timestamp')
        self.author = User(**kwargs.get('author')) if kwargs.get('author') else None
        self.webhook_id = kwargs.get('webhook_id')
        self.message_reference = Message(**kwargs.get('message_reference')) if kwargs.get('message_reference') else None
        self.position = kwargs.get('position')
        self.interaction_metadata = InteractionMetadata(**kwargs.get('interaction_metadata')) if kwargs.get('interaction_metadata') else None


    def edit(self, pool: PoolManager, content: str = None, tts: bool = False, embeds: list[dict] = None, allowed_mentions: dict = None, components: list[ActionRow] = None):
        data = {}

        if content is not None:
            data['content'] = content

        if tts is not None:
            data['tts'] = tts

        if embeds is not None:
            data['embeds'] = embeds

        if allowed_mentions is not None:
            data['allowed_mentions'] = allowed_mentions

        if components is not None:
            data['components'] = [c.to_dict() for c in components]


        resp = pool.request('PATCH', f'https://discord.com/api/v9/webhooks/{self.application_id}/{self.token}/messages/@original', body=json.dumps(data), headers={'Content-Type': 'application/json'})
        if resp.status != 200:
            return None

        return json.loads(resp.data.decode('utf-8'))
# b'{"type":19,"channel_id":"1240035159064055959","content":"","attachments":[],"embeds":[],"timestamp":"2024-05-17T12:20:07.066000+00:00","edited_timestamp":null,"flags":192,"components":[],"id":"1241002308548956240","author":{"id":"1186659996314914928","username":"EB Vendors Assistant","avatar":"0263ec2e56235a08592c8ae14a570bd9","discriminator":"8391","public_flags":524288,"flags":524288,"bot":true,"banner":null,"accent_color":null,"global_name":null,"avatar_decoration_data":null,"banner_color":null,"clan":null},"mentions":[],"mention_roles":[],"pinned":false,"mention_everyone":false,"tts":false,"application_id":"1186659996314914928","webhook_id":"1186659996314914928","message_reference":{"type":0,"channel_id":"1240035159064055959","message_id":"1240035168144720013","guild_id":"1240035059499663553"},"position":0,"interaction_metadata":{"id":"1241002302177939558","type":3,"user_id":"1150390416529702943","user":{"id":"1150390416529702943","username":"abdulkarim_essam","avatar":"31b0408f124c62170fb8a7294ed2742e","discriminator":"0","public_flags":0,"flags":0,"banner":null,"accent_color":null,"global_name":"Abdulkarim Essam","avatar_decoration_data":null,"banner_color":null,"clan":null},"authorizing_integration_owners":{"0":"1240035059499663553"},"interacted_message_id":"1240035168144720013"}}\n'


    @staticmethod
    def get_by_token(pool: PoolManager, application_id: str, token: str):
        resp = pool.request('GET', f'https://discord.com/api/v9/webhooks/{application_id}/{token}/messages/@original')

        if resp.status != 200:
            return None

        resp = json.loads(resp.data.decode('utf-8'))
        resp['application_id'] = application_id
        resp['token'] = token

        return Interaction(**resp)
