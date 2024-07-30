import discord_lambda.embed_cfg as cfg
# embed builder for discord


def field(name: str, value: str, inline: bool = True) -> dict:
    return {
        'name': name or '\u200b',
        'value': value or '\u200b',
        'inline': inline
     }
def embed(title: str = None, description: str = None, url: str = None, color: int = None, fields: list[dict] = None, author: dict = None, thumbnail: dict = None, image: str = None, footer: dict = None, timestamp: str = None) -> dict:
    data = {}

    if title or cfg.default_embed_title:
        if title is not False: data['title'] = title or cfg.default_embed_title

    if description or cfg.default_embed_description:
        if description is not False: data['description'] = description or cfg.default_embed_description
    if url or cfg.default_embed_url:
        if url is not False: data['url'] = url or cfg.default_embed_url

    if color or cfg.default_embed_color:
        data['color'] = color or cfg.default_embed_color

    if fields is not None:
        if fields is not False: data['fields'] = fields

    if author or cfg.default_embed_author:
        if author is not False: data['author'] = author or cfg.default_embed_author

    if thumbnail or cfg.default_embed_thumbnail:
        if thumbnail is not False: data['thumbnail'] = {
            'url': thumbnail or cfg.default_embed_thumbnail
        }

    if image or cfg.default_embed_image:
        if image is not False: data['image'] = {
            'url': image or cfg.default_embed_image
        }

    if footer or cfg.default_embed_footer:
        if footer is not False: data['footer'] = footer or cfg.default_embed_footer

    if timestamp is not None:
        if timestamp is not False: data['timestamp'] = timestamp

    data['type'] = 'rich'

    return data



def error_embed(description: str) -> dict:
    return embed(
        title='Failed',
        description=description
    )



