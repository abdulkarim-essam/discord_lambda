from typing import Union

class User :

    avatar_url: str
    discriminator: str
    id: str
    username: str

    def __init__(self, **kwargs):
        self.__avatar = kwargs.get('avatar')
        self.discriminator = kwargs.get('discriminator')
        self.id = kwargs.get('id')
        self.username = kwargs.get('username')
        self.name = kwargs.get('global_name') if kwargs.get('global_name') else kwargs.get('username')
        self.global_name = kwargs.get('global_name')
        self.bot = kwargs.get('bot', False)

    @property
    def avatar_url(self):
        # return avatar or default avatar if no avatar
        return f'https://cdn.discordapp.com/avatars/{self.id}/{self.__avatar}.png' if self.__avatar else 'https://cdn.discordapp.com/embed/avatars/0.png'



class Member:
    avatar_url: str
    timeout_expiry: str
    joined_at: str
    mute: bool
    nick: str
    nickname: str
    pending: bool
    username: str
    user: Union[User, None]
    id: str



    def __init__(self, **kwargs):
        self.__id = kwargs.get('id')
        self.__avatar= kwargs.get('avatar')
        self.timeout_expiry = kwargs.get('communication_disabled_until')
        self.deaf = kwargs.get('deaf')
        self.joined_at = kwargs.get('joined_at')
        self.mute = kwargs.get('mute')
        self.nick = kwargs.get('nick')
        self.nickname = kwargs.get('nick')
        self.pending = kwargs.get('pending')

        self.user = User(**kwargs.get('user')) if kwargs.get('user') else None

    @property
    def avatar_url(self):
        # return avatar or default avatar if no avatar
        return f'https://cdn.discordapp.com/avatars/{self.user.id}/{self.__avatar}.png' if self.__avatar else self.user.avatar_url

    @property
    def username(self):
        return self.user.username if self.user else self.__id

    @property
    def id(self):
        return self.user.id if self.user else self.__id


