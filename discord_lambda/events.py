from typing import Union
from discord_lambda.channels import TextChannel
import json
from discord_lambda.responses import Response
from discord_lambda.options import Option, StringOption, MemberOption, EmptyOption
from discord_lambda.components import ActionRow, ModalTextField
from .user import Member
from .messages import Message
class EventType(str):
    pass

class AWSEvent:
    body: str
    headers: dict


    def __init__(self, event: dict):
        self.__body = event.get('body')
        self.headers = event.get('headers', {})

    @property
    def body(self):
        return json.loads(self.__body or '{}') or {}


class DiscordEvent:
    app_permissions: str
    application_id: str
    channel: TextChannel
    channel_id: str
    data: dict
    entitlement_sku_ids: list
    entitlements: list
    guild: dict
    guild_id: str
    guild_locale: str
    id: str
    locale: str
    member: Member
    type: EventType
    version: int
    message: Message
    token: str


    def __init__(self, body: dict):
        self.app_permissions = body.get('app_permissions')
        self.application_id = body.get('application_id')
        self.channel = body.get('channel')
        self.channel_id = body.get('channel_id')
        self.data = body.get('data')
        self.entitlement_sku_ids = body.get('entitlement_sku_ids')
        self.entitlements = body.get('entitlements')
        self.guild = body.get('guild')
        self.guild_id = body.get('guild_id')
        self.guild_locale = body.get('guild_locale')
        self.id = body.get('id')
        self.locale = body.get('locale')
        self.member = Member(**body.get('member')) if body.get('member') else None
        self.__type = body.get('type')
        self.version = body.get('version')
        self.message = Message(**body.get('message')) if body.get('message') is not None else None
        self.token = body.get('token')



    def respond(self, data:dict ) -> Response:
        print({
          'statusCode': 200,
          'body': json.dumps(data),
          'headers': {
              'Content-Type': 'application/json',
          }})

        return {
          'statusCode': 200,
          'body': json.dumps(data),
          'headers': {
              'Content-Type': 'application/json',
          }
      }


    def reply(self, content: str = None, tts: bool = False, embeds: list[dict] = None, allowed_mentions: dict = None, ephemeral: bool = True, components: list[ActionRow] = []) -> Response:
        data = {}

        if content is not None:
            data['content'] = content

        if tts is not None:
            data['tts'] = tts

        if embeds is not None:
            data['embeds'] = embeds

        if allowed_mentions is not None:
            data['allowed_mentions'] = allowed_mentions

        if ephemeral:
            data['flags'] = 64

        if components is not None:
            data['components'] = [c.to_dict() for c in components]

        return self.respond({"type": 4, "data": data})



    def edit_original_response(self, content: str = None, tts: bool = False, embeds: list[dict] = None, allowed_mentions: dict = None, components: list[ActionRow] = None) -> Response:
        data = {}

        if content is not None:
            data['content'] = content if content else ''

        if tts is not None:
            data['tts'] = tts

        if embeds is not None:
            data['embeds'] = embeds if embeds else []

        if allowed_mentions is not None:
            data['allowed_mentions'] = allowed_mentions

        if components is not None:
            data['components'] = [c.to_dict() for c in components] if components else []

        return self.respond({"type": 7, "data": data})

    def show_modal(self, title: str, custom_id: str, fields: list[ModalTextField]) -> Response:
        """
        Show a modal to the user

        Parameters:
        - title _str_: The title of the modal
        - custom_id _str_: The custom id of the modal
        - fields _list[ModalTextField]_: The fields of the modal

        Returns:
        - Response: The response from the API

        Example:
        ```python
        fields = [
            ModalTextField.create(ModalTextFieldStyle.SHORT, "Name", "name", required=True),
            ModalTextField.create(ModalTextFieldStyle.PARAGRAPH, "description", "Description")
        ]
        event.show_modal("Create a new project", "create_project", fields)
        ```
        """

        # create an action row for each field
        components = [ActionRow([field]) for field in fields]

        # create the modal
        return self.respond({
            "type": 9,
            "data":
            {
                "title": title,
                "custom_id": custom_id,
                "components": [c.to_dict() for c in components]
            }})

    def defer_response(self, ephemeral: bool = False) -> Response:

        data = {
            "flags": 64 if ephemeral else 0
        }

        return self.respond({"type": 5, "data": data})

    def defer_update(self) -> Response:
        return self.respond({"type": 6})

    @staticmethod
    def create(body: dict):
        event = DiscordEvent(body)

        if event.__type == 1:
            return PingEvent(body)
        if event.__type == 2:
            return SlashCommandEvent(body)
        # select menu
        if event.__type == 3:
            event = ComponentEvent(body)
            if event.is_select_menu: return SelectMenuEvent(body)
            if event.is_button: return ButtonEvent(body)
        if event.__type == 4:
            return AutoCompleteEvent(body)
        if event.__type == 5:
            return ModalEvent(body)

    @property
    def type(self):
        if self.__type == 1:
            return PingEvent
        if self.__type == 2:
            return SlashCommandEvent


class PingEvent(DiscordEvent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def respond(self):
        return super().respond({'type': 1})



class SlashCommandEvent(DiscordEvent):
    name: str
    options: list[Option]
    message: Message

    def __init__(self, body: dict):
        super().__init__(body)
        self.name = body.get('data', {}).get('name')
        self.__options = body.get('data', {}).get('options')
        self.__parsed_options = None
        self.__data = body.get('data')


    def get_option(self, name: str) -> Union[str, Member, None]:
        for option in self.options:
            if option.name == name:
                return option.value

        return None



    @property
    def options(self) -> list[Option]:
        if self.__parsed_options is not None:
            return self.__parsed_options

        options = self.__options
        self.__parsed_options = [Option.create(option, self.__data) for option in options]

        return self.__parsed_options

    @property
    def message(self) -> Message:
        if not self.__data.get('target_id'): return None

        messages = self.__data.get('resolved', {}).get('messages', {})

        message = messages.get(self.__data.get('target_id'))

        return Message(**message) if message else None

    @message.setter
    def message(self, message: Message):
        if not message: return

class AutocompleteChoice:

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value
        }

    @staticmethod
    def create(name: str, value: str):
        return AutocompleteChoice(name, value)



class AutoCompleteEvent(DiscordEvent):
    name: str
    options: list[Option]


    def __init__(self, body: dict):
        super().__init__(body)
        self.name = body.get('data', {}).get('name')
        self.__options = body.get('data', {}).get('options')
        self.__parsed_options = None
        self.__data = body.get('data')


    def get_option(self, name: str) -> Union[str, Member, None]:
        for option in self.options:
            if option.name == name:
                return option.value

        return None


    def get_focused_option(self):
        for option in self.options:
            if option.focused:
                return option

        return None


    def return_choices(self, choices: list[AutocompleteChoice]):
        if not choices:
            raise ValueError("Choices must be a non-empty list of AutocompleteChoice objects.")

        return self.respond({
            "type": 8,
            "data": {
                "choices": [choice.to_dict() for choice in choices]
            }
        })







    @property
    def options(self) -> list[Option]:
        if self.__parsed_options is not None:
            return self.__options

        options = self.__options
        print(self.__data)
        self.__parsed_options = [Option.create(option, self.__data) for option in options]

        return self.__parsed_options


class ComponentEvent(DiscordEvent):
    custom_id: str
    component_type: int
    is_button: bool
    is_select_menu: bool

    def __init__(self, body: dict):
        super().__init__(body)
        self.custom_id = body.get('data', {}).get('custom_id')
        self.component_type = body.get('data', {}).get('component_type')


    @property
    def is_select_menu(self):
      return self.component_type == 3


    @property
    def is_button(self):
        return self.component_type == 2


class SelectMenuEvent(ComponentEvent):
    values: list[str]
    selected_value: str

    def __init__(self, body: dict):
        super().__init__(body)
        self.values = body.get('data', {}).get('values')


    @property
    def selected_value(self):
        return self.values[0]


class ButtonEvent(ComponentEvent):
    def __init__(self, body: dict):
        super().__init__(body)




class ModalEvent(ComponentEvent):
    values: dict

    def __init__(self, body: dict):
        super().__init__(body)
        self.values = self._extract_values(body)

    def _extract_values(self, body: dict):
        """
        Extracts a dictionary of custom_id: value from the modal data components.
        """
        values = {}
        components = body.get("data", {}).get("components", [])

        for row in components:
            for component in row.get("components", []):
                custom_id = component.get("custom_id")
                value = component.get("value", None)  # Get value, or None if missing
                if custom_id:
                    values[custom_id] = value

        return values

    def get_value(self, field_name: str):
        """
        Returns the value for a given custom_id or None if not found.
        """
        return self.values.get(field_name)

    def get_values(self):
        """
        Returns all the values extracted from the modal.
        """
        return self.values
