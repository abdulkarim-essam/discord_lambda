from .user import User


class Message:
    id: str
    author: User
    channel_id: str
    content: str


    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.author = User(**kwargs.get('author')) if kwargs.get('author') else None
        self.guild_id = kwargs.get('guild_id')
        self.channel_id = kwargs.get('channel_id')
        self.content = kwargs.get('content')
        self.embeds = kwargs.get('embeds')
