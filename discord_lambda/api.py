from urllib3 import PoolManager
import json

class PERMISSIONS:
    VIEW_CHANNEL = 0x400
    SEND_MESSAGES = 0x800
    SEND_TTS_MESSAGES = 0x1000
    MENTION_EVERYONE = 0x2000

class Role:
    id: str
    name: str
    description: str
    permissions: str
    position: int
    color: int
    hoist: bool
    managed: bool
    mentionable: bool
    icon: str
    unicode_emoji: str
    flags: int
    tags: dict


    def __init__(self, id: str, name: str, description: str, permissions: str, position: int, color: int, hoist: bool, managed: bool, mentionable: bool, icon: str, unicode_emoji: str, flags: int, tags: dict):
        self.id = id
        self.name = name
        self.description = description
        self.permissions = permissions
        self.position = position
        self.color = color
        self.hoist = hoist
        self.managed = managed
        self.mentionable = mentionable
        self.icon = icon
        self.unicode_emoji = unicode_emoji
        self.flags = flags
        self.tags = tags


class Guild:
    id: str
    name: str
    icon: str
    description: str
    home_header: str
    splash: str
    discovery_splash: str
    features: list
    banner: str
    owner_id: str
    application_id: str
    region: str
    afk_channel_id: str
    afk_timeout: int
    system_channel_id: str
    system_channel_flags: int
    widget_enabled: bool
    widget_channel_id: str
    verification_level: int
    roles: list[Role]
    default_message_notifications: int
    mfa_level: int
    explicit_content_filter: int
    max_presences: int
    max_members: int
    max_stage_video_channel_users: int
    max_video_channel_users: int
    vanity_url_code: str
    premium_tier: int
    premium_subscription_count: int
    preferred_locale: str
    rules_channel_id: str
    safety_alerts_channel_id: str
    public_updates_channel_id: str
    hub_type: str
    premium_progress_bar_enabled: bool
    latest_onboarding_question_id: str
    nsfw: bool
    nsfw_level: int
    emojis: list
    stickers: list
    incidents_data: dict
    inventory_settings: dict
    embed_enabled: bool
    embed_channel_id: str



    def __init__(self, id: str, name: str, icon: str, description: str, home_header: str, splash: str, discovery_splash: str, features: list, banner: str, owner_id: str, application_id: str, region: str, afk_channel_id: str, afk_timeout: int, system_channel_id: str, system_channel_flags: int, widget_enabled: bool, widget_channel_id: str, verification_level: int, roles: list[Role], default_message_notifications: int, mfa_level: int, explicit_content_filter: int, max_presences: int, max_members: int, max_stage_video_channel_users: int, max_video_channel_users: int, vanity_url_code: str, premium_tier: int, premium_subscription_count: int, preferred_locale: str, rules_channel_id: str, safety_alerts_channel_id: str, public_updates_channel_id: str, hub_type: str, premium_progress_bar_enabled: bool, latest_onboarding_question_id: str, nsfw: bool, nsfw_level: int, emojis: list, stickers: list, incidents_data: dict, inventory_settings: dict, embed_enabled: bool, embed_channel_id: str, token: str = ''):
        self.id = id
        self.name = name
        self.icon = icon
        self.description = description
        self.home_header = home_header
        self.splash = splash
        self.discovery_splash = discovery_splash
        self.features = features
        self.banner = banner
        self.owner_id = owner_id
        self.application_id = application_id
        self.region = region
        self.afk_channel_id = afk_channel_id
        self.afk_timeout = afk_timeout
        self.system_channel_id = system_channel_id
        self.system_channel_flags = system_channel_flags
        self.widget_enabled = widget_enabled
        self.widget_channel_id = widget_channel_id
        self.verification_level = verification_level
        self.roles = roles
        self.default_message_notifications = default_message_notifications
        self.mfa_level = mfa_level
        self.explicit_content_filter = explicit_content_filter
        self.max_presences = max_presences
        self.max_members = max_members
        self.max_stage_video_channel_users = max_stage_video_channel_users
        self.max_video_channel_users = max_video_channel_users
        self.vanity_url_code = vanity_url_code
        self.premium_tier = premium_tier
        self.premium_subscription_count = premium_subscription_count
        self.preferred_locale = preferred_locale
        self.rules_channel_id = rules_channel_id
        self.safety_alerts_channel_id = safety_alerts_channel_id
        self.public_updates_channel_id = public_updates_channel_id
        self.hub_type = hub_type
        self.premium_progress_bar_enabled = premium_progress_bar_enabled
        self.latest_onboarding_question_id = latest_onboarding_question_id
        self.nsfw = nsfw
        self.nsfw_level = nsfw_level
        self.emojis = emojis
        self.stickers = stickers
        self.incidents_data = incidents_data
        self.inventory_settings = inventory_settings
        self.embed_enabled = embed_enabled
        self.embed_channel_id = embed_channel_id
        self.__token = token




    def create_category(self, pool: PoolManager, name: str, position: int = 0, permission_overwrites: list = []) -> 'CategoryChannel':
        data = {
            'name': name,
            'type': 4,
            'position': position,
            'permission_overwrites': permission_overwrites
        }

        response = pool.request('POST', f'https://discord.com/api/v9/guilds/{self.id}/channels', headers={
            'Authorization': f'Bot {self.__token}',
            'Content-Type': 'application/json'
        }, body=json.dumps(data))

        if response.status > 299:
            return None

        data = json.loads(response.data.decode('utf-8'))


        return CategoryChannel(id=data['id'], name=data['name'], guild_id=data['guild_id'], position=data['position'], permission_overwrites=data['permission_overwrites'], nsfw=data.get('nsfw', False), token=self.__token)



    @staticmethod
    def get(pool: PoolManager, guild_id: str, token: str) -> 'Guild':
        response = pool.request('GET', f'https://discord.com/api/v9/guilds/{guild_id}', headers={
            'Authorization': f'Bot {token}'
        })

        if response.status != 200:
            return None


        data = json.loads(response.data.decode('utf-8'))

        if 'id' not in data:
            return None

        roles = [Role(id=r['id'], name=r['name'], description=r['description'], permissions=r['permissions'], position=r['position'], color=r['color'], hoist=r['hoist'], managed=r['managed'], mentionable=r['mentionable'], icon=r['icon'], unicode_emoji=r['unicode_emoji'], flags=r['flags'], tags=r.get('tags', [])) for r in data['roles']]

        return Guild(id=data['id'], name=data['name'], icon=data['icon'], description=data['description'], home_header=data['home_header'], splash=data['splash'], discovery_splash=data['discovery_splash'], features=data['features'], banner=data['banner'], owner_id=data['owner_id'], application_id=data['application_id'], region=data['region'], afk_channel_id=data['afk_channel_id'], afk_timeout=data['afk_timeout'], system_channel_id=data['system_channel_id'], system_channel_flags=data['system_channel_flags'], widget_enabled=data['widget_enabled'], widget_channel_id=data['widget_channel_id'], verification_level=data['verification_level'], roles=roles, default_message_notifications=data['default_message_notifications'], mfa_level=data['mfa_level'], explicit_content_filter=data['explicit_content_filter'], max_presences=data['max_presences'], max_members=data['max_members'], max_stage_video_channel_users=data['max_stage_video_channel_users'], max_video_channel_users=data['max_video_channel_users'], vanity_url_code=data['vanity_url_code'], premium_tier=data['premium_tier'], premium_subscription_count=data['premium_subscription_count'], preferred_locale=data['preferred_locale'], rules_channel_id=data['rules_channel_id'], safety_alerts_channel_id=data['safety_alerts_channel_id'], public_updates_channel_id=data['public_updates_channel_id'], hub_type=data['hub_type'], premium_progress_bar_enabled=data['premium_progress_bar_enabled'], latest_onboarding_question_id=data['latest_onboarding_question_id'], nsfw=data.get('nsfw', False), nsfw_level=data['nsfw_level'], emojis=data['emojis'], stickers=data['stickers'], incidents_data=data['incidents_data'], inventory_settings=data['inventory_settings'], embed_enabled=data['embed_enabled'], embed_channel_id=data['embed_channel_id'], token=token)


class CategoryChannel:
    id: str
    name: str
    guild_id: str
    position: int
    permission_overwrites: list
    nsfw: bool


    def __init__(self, id: str, name: str, guild_id: str, position: int, permission_overwrites: list, nsfw: bool, token: str = ''):
        self.id = id
        self.name = name
        self.guild_id = guild_id
        self.position = position
        self.permission_overwrites = permission_overwrites
        self.nsfw = nsfw
        self.__token = token


    def update_user_permissions(self, pool: PoolManager, overwrite_id: str, allot: int, deny: int):
        data = {
            'allow': allot,
            'deny': deny,
            'type': 1
        }

        response = pool.request('PUT', f'https://discord.com/api/v9/channels/{self.id}/permissions/{overwrite_id}', headers={
            'Authorization': f'Bot {self.__token}',
            'Content-Type': 'application/json'
        }, body=json.dumps(data))

        return response.status == 204



    def delete(self, pool: PoolManager) -> bool:
        response = pool.request('DELETE', f'https://discord.com/api/v9/channels/{self.id}', headers={
            'Authorization': f'Bot {self.__token}'
        })

        return response.status == 204


    def get_children(self, pool: PoolManager) -> list['TextChannel']:
        response = pool.request('GET', f'https://discord.com/api/v9/guilds/{self.guild_id}/channels', headers={
            'Authorization': f'Bot {self.__token}'
        })

        if response.status > 299:
            return []

        data = json.loads(response.data.decode('utf-8'))

        channels = []

        for d in data:
            if d['parent_id'] == self.id:
                channels.append(TextChannel(id=d['id'], last_message_id=d['last_message_id'], flags=d['flags'], guild_id=d['guild_id'], name=d['name'], parent_id=d['parent_id'], rate_limit_per_user=d['rate_limit_per_user'], topic=d['topic'], position=d['position'], permission_overwrites=d['permission_overwrites'], nsfw=d['nsfw'], token=self.__token))

        return channels

    def create_text_channel(self, pool: PoolManager, name: str, type: int = 0, topic: str = '', position: int = 0, permission_overwrites: list = [], nsfw: bool = False, rate_limit_per_user: int = 0) -> 'TextChannel':
        return TextChannel.create(pool, self.guild_id, name, type, topic, position, permission_overwrites, nsfw, rate_limit_per_user, self.id, self.__token)

    @staticmethod
    def get(pool: PoolManager, channel_id: str, token: str) -> 'CategoryChannel':
        response = pool.request('GET', f'https://discord.com/api/v9/channels/{channel_id}', headers={
            'Authorization': f'Bot {token}'
        })

        if response.status != 200:
            return None

        data = json.loads(response.data.decode('utf-8'))

        if data['type'] != 4:
            return None

        return CategoryChannel(id=data['id'], name=data['name'], guild_id=data['guild_id'], position=data['position'], permission_overwrites=data['permission_overwrites'], nsfw=data.get('nsfw', False), token=token)







class Message:
    id: str
    channel_id: str
    channel: 'TextChannel'
    content: str
    attachments: list
    embeds: list[dict]
    timestamp: str
    edited_timestamp: str
    flags: int
    components: list
    author_id: str
    mentions: list
    mention_roles: list
    pinned: bool
    mention_everyone: bool
    tts: bool


    def __init__(self, id: str, channel_id: str, channel: 'TextChannel', content: str, attachments: list, embeds: list[dict], timestamp: str, edited_timestamp: str, flags: int, components: list, author_id: str, mentions: list, mention_roles: list, pinned: bool, mention_everyone: bool, tts: bool, token: str = ''):
        self.id = id
        self.channel_id = channel_id
        self.channel = channel
        self.content = content
        self.attachments = attachments
        self.embeds = embeds
        self.timestamp = timestamp
        self.edited_timestamp = edited_timestamp
        self.flags = flags
        self.components = components
        self.author_id = author_id
        self.mentions = mentions
        self.mention_roles = mention_roles
        self.pinned = pinned
        self.mention_everyone = mention_everyone
        self.tts = tts
        self.__token = token


    def pin(self, pool: PoolManager) -> bool:
        response = pool.request('PUT', f'https://discord.com/api/v9/channels/{self.channel_id}/pins/{self.id}', headers={
            'Authorization': f'Bot {self.__token}'
        })

        return response.status == 204

    def unpin(self, pool: PoolManager) -> bool:
        response = pool.request('DELETE', f'https://discord.com/api/v9/channels/{self.channel_id}/pins/{self.id}', headers={
            'Authorization': f'Bot {self.__token}'
        })


        return response.status == 204

    def edit(self, pool: PoolManager, content: str = None, embeds: list = None, components: list = None, attachments: list = None) -> 'Message':

        data = {}

        if content is not None:
            data['content'] = content

        if embeds is not None:
            data['embeds'] = embeds

        if components is not None:
            data['components'] = [c.to_dict() for c in components]

        if attachments is not None:
            data['attachments'] = attachments

        response = pool.request('PATCH', f'https://discord.com/api/v9/channels/{self.channel_id}/messages/{self.id}', headers={
            'Authorization': f'Bot {self.__token}',
            'Content-Type': 'application/json'
        }, body=json.dumps(data))

        if response.status > 299:
            return None

        self.content = content if content is not None else self.content
        self.embeds = embeds if embeds is not None else self.embeds
        self.components = components if components is not None else self.components
        self.attachments = attachments if attachments is not None else self.attachments

        return self

    def delete(self, pool: PoolManager) -> bool:
        response = pool.request('DELETE', f'https://discord.com/api/v9/channels/{self.channel_id}/messages/{self.id}', headers={
            'Authorization': f'Bot {self.__token}'
        })

        return response.status == 204



class TextChannel:
    id: str
    last_message_id: str
    flags: int
    guild_id: str
    name: str
    parent_id: str
    rate_limit_per_user: int
    topic: str
    position: int
    permission_overwrites: list
    nsfw: bool

    def __init__(self, id: str, last_message_id: str = None, flags: int = 0, guild_id: str = '', name: str = '', parent_id: str = '', rate_limit_per_user: int = 0, topic: str = '', position: int = 0, permission_overwrites: list = [], nsfw: bool = False, token: str = ''):
          self.id = id
          self.last_message_id = last_message_id
          self.flags = flags
          self.guild_id = guild_id
          self.name = name
          self.parent_id = parent_id
          self.rate_limit_per_user = rate_limit_per_user
          self.topic = topic
          self.position = position
          self.permission_overwrites = permission_overwrites
          self.__token = token


    def delete(self, pool: PoolManager) -> bool:
        response = pool.request('DELETE', f'https://discord.com/api/v9/channels/{self.id}', headers={
            'Authorization': f'Bot {self.__token}'
        })

        return response.status == 204


    def delete_message(self, pool: PoolManager, message_id: str) -> bool:
        response = pool.request('DELETE', f'https://discord.com/api/v9/channels/{self.id}/messages/{message_id}', headers={
            'Authorization': f'Bot {self.__token}'
        })


        return response.status == 204

    def send(self, pool: PoolManager, embeds: list = [], content: str = '', tts: bool = False, allowed_mentions: dict = {}, message_reference: dict = {}, components: list = [], sticker_ids: list = [], files: list = []) -> 'Message':
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

        if sticker_ids is not None:
            data['sticker_ids'] = sticker_ids

        if files is not None:
            data['files'] = files

        response = pool.request('POST', f'https://discord.com/api/v9/channels/{self.id}/messages', headers={
            'Authorization': f'Bot {self.__token}',
            'Content-Type': 'application/json'
        }, body=json.dumps(data))

        if response.status != 200:
            return None

        data = json.loads(response.data.decode('utf-8'))
        m = Message(id=data['id'], channel_id=data['channel_id'], channel=self, content=data['content'], attachments=data['attachments'], embeds=data['embeds'], timestamp=data['timestamp'], edited_timestamp=data['edited_timestamp'], flags=data['flags'], components=data['components'], author_id=data['author']['id'], mentions=data['mentions'], mention_roles=data['mention_roles'], pinned=data['pinned'], mention_everyone=data['mention_everyone'], tts=data['tts'], token=self.__token)

        return m


    def get_message(self, pool: PoolManager, message_id: str) -> 'Message':
        response = pool.request('GET', f'https://discord.com/api/v9/channels/{self.id}/messages/{message_id}', headers={
            'Authorization': f'Bot {self.__token}'
        })



        if response.status > 299:
            return None

        data = json.loads(response.data.decode('utf-8'))
        return Message(id=data['id'], channel_id=data['channel_id'], channel=self, content=data['content'], attachments=data['attachments'], embeds=data['embeds'], timestamp=data['timestamp'], edited_timestamp=data['edited_timestamp'], flags=data['flags'], components=data['components'], author_id=data['author']['id'], mentions=data['mentions'], mention_roles=data['mention_roles'], pinned=data['pinned'], mention_everyone=data['mention_everyone'], tts=data['tts'], token=self.__token)


    def delete_messages(self, pool: PoolManager, message_ids: list) -> bool:
        data = {
            'messages': message_ids
        }

        response = pool.request('POST', f'https://discord.com/api/v9/channels/{self.id}/messages/bulk-delete', headers={
            'Authorization': f'Bot {self.__token}',
            'Content-Type': 'application/json'
        }, body=json.dumps(data))

        return response.status == 204




    def update_user_permissions(self, pool: PoolManager, overwrite_id: str, allot: int, deny: int):
        data = {
            'allow': allot,
            'deny': deny,
            'type': 1
        }

        response = pool.request('PUT', f'https://discord.com/api/v9/channels/{self.id}/permissions/{overwrite_id}', headers={
            'Authorization': f'Bot {self.__token}',
            'Content-Type': 'application/json'
        }, body=json.dumps(data))


        return response.status == 204

    @staticmethod
    def create(pool: PoolManager, guild_id: str, name: str, type: int = 0, topic: str = '', position: int = 0, permission_overwrites: list = [], nsfw: bool = False, rate_limit_per_user: int = 0, parent_id: str = '', token: str = '') -> 'TextChannel':
        data = {
            'name': name,
            'type': type,
            'topic': topic,
            'position': position,
            'permission_overwrites': permission_overwrites,
            'nsfw': nsfw,
            'rate_limit_per_user': rate_limit_per_user,
            'parent_id': parent_id
        }

        response = pool.request('POST', f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers={
            'Authorization': f'Bot {token}',
            'Content-Type': 'application/json'
        }, body=json.dumps(data))

        if response.status > 299:
            return None

        data = json.loads(response.data.decode('utf-8'))

        return TextChannel(id=data['id'], last_message_id=data['last_message_id'], flags=data['flags'], guild_id=data['guild_id'], name=data['name'], parent_id=data['parent_id'], rate_limit_per_user=data['rate_limit_per_user'], topic=data['topic'], position=data['position'], permission_overwrites=data['permission_overwrites'], nsfw=data['nsfw'], token=token)




    @staticmethod
    def get(pool: PoolManager, channel_id: str, token: str) -> 'TextChannel':
        response = pool.request('GET', f'https://discord.com/api/v9/channels/{channel_id}', headers={
            'Authorization': f'Bot {token}'
        })

        if response.status != 200:
            return None

        data = json.loads(response.data.decode('utf-8'))

        if data['type'] != 0:
            return None

        return TextChannel(id=data['id'], last_message_id=data['last_message_id'], flags=data['flags'], guild_id=data['guild_id'], name=data['name'], parent_id=data['parent_id'], rate_limit_per_user=data['rate_limit_per_user'], topic=data['topic'], position=data['position'], permission_overwrites=data['permission_overwrites'], nsfw=data['nsfw'], token=token)
