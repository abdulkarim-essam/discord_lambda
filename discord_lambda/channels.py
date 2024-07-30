from typing import TypedDict
class TextChannel(TypedDict):
    flags: int
    guild_id: str
    id: str
    last_message_id: str
    name: str
    nsfw: bool
    parent_id: str
    permissions: str
    position: int
    rate_limit_per_user: int


