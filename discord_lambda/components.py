from typing import TypedDict
class Component:
      type: int
      custom_id: str

      def __init__(self, type: int, **kwargs):
          self.type = type
          self.kwargs = kwargs

      def to_dict(self):
          if 'emoji' in self.kwargs:
              if isinstance(self.kwargs['emoji'], str):
                  self.kwargs['emoji'] = {
                      "name": self.kwargs['emoji']
                  }

          return {
              "type": self.type,
              **self.kwargs
          }

      def __repr__(self):
          return f"<Component type={self.type} kwargs={self.kwargs}>"
class SelectMenuOption:
    label: str
    value: str
    description: str
    emoji: dict
    default: bool

    def __init__(self, label: str, value: str, description: str = None, emoji: dict = None, default: bool = False):
        self.label = label
        self.value = value
        self.description = description
        self.emoji = emoji if not emoji or isinstance(emoji, dict) else {
            "name": emoji
        }
        self.default = default

    def to_dict(self):
        return {
            "label": self.label,
            "value": self.value,
            "description": self.description,
            "emoji": self.emoji,
            "default": self.default
        }

    def __repr__(self):
        return f"<SelectMenuOption label={self.label} value={self.value} description={self.description} emoji={self.emoji} default={self.default}>"


    @staticmethod
    def create(label: str, value: str, description: str = None, emoji: dict = None, default: bool = False):
        return SelectMenuOption(label, value, description, emoji, default)

class SelectMenu(Component):
    options: list[SelectMenuOption]

    def __init__(self, options: list[SelectMenuOption], **kwargs):
        super().__init__(3, **kwargs)
        self.options = options


    @staticmethod
    def create(options: list[SelectMenuOption], **kwargs):
        return SelectMenu(options, **kwargs)

    def to_dict(self):
        return {
            **super().to_dict(),
            "options": [o.to_dict() for o in self.options]
        }

class ButtonStyle:
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5

class Button(Component):
    style: int
    label: str
    emoji: dict
    url: str
    disabled: bool

    def __init__(self, style: int, label: str, **kwargs):
        super().__init__(2, **kwargs)
        self.style = style
        self.label = label

    @staticmethod
    def create(style: int, label: str, **kwargs):
        return Button(style, label, **kwargs)

    def to_dict(self):
        return {
            **super().to_dict(),
            "style": self.style,
            "label": self.label
        }

    def __repr__(self):
        return f"<Button style={self.style} label={self.label}>"

class ActionRow:
    components: list[Component]
    def __init__(self, components: list):
        self.components = components

    def to_dict(self):

        return {
            "type": 1,
            "components": [c.to_dict() for c in self.components]
        }

    def __repr__(self):
        return f"<ActionRow components={self.components}>"


class ModalTextFieldStyle:
    SHORT = 1
    PARAGRAPH = 2

class ModalTextField(Component):

    style: ModalTextFieldStyle
    label: str
    placeholder: str
    required: bool
    min_length: int
    max_length: int
    value: str

    def __init__(self, style: ModalTextFieldStyle, label: str, custom_id: str, **kwargs):
        super().__init__(4, custom_id=custom_id, **kwargs)
        self.style = style
        self.label = label
        self.placeholder = kwargs.get('placeholder', None)
        self.required = kwargs.get('required', False)
        self.min_length = kwargs.get('min_length', None)
        self.max_length = kwargs.get('max_length', None)
        self.value = kwargs.get('value', None)

    @staticmethod
    def create(style: ModalTextFieldStyle, label: str, custom_id: str, **kwargs):
      """
      Creates a new ModalTextField component.

      Parameters:
      - style `ModalTextFieldStyle`: The style of the text field. Use `ModalTextFieldStyle.SHORT` for a short text field or `ModalTextFieldStyle.PARAGRAPH` for a paragraph text field.

      - label `str`: The label of the text field. It's a brief description shown above the text field.

      - custom_id `str`: The custom id of the text field.

      Optional Keyword Arguments:
      - required `bool`: Specifies whether the text field is required for form submission. Defaults to `False`.
      - min_length `int`: The minimum length (in characters) required for the text field content. Defaults to `None`, indicating no minimum.
      - max_length `int`: The maximum length (in characters) allowed for the text field content. Defaults to `None`, indicating no maximum.
      - placeholder `str`: Placeholder text displayed inside the text field before the user enters a value.
      - value `str`: The initial value of the text field.

      Returns:
      - ModalTextField: An instance of the ModalTextField component configured with the specified options.

      Example:
      >>> ModalTextField.create(ModalTextFieldStyle.SHORT, 'Name', "name", placeholder='Enter your name here')
      """

      return ModalTextField(style, label, custom_id, **kwargs)


    def to_dict(self):
        data = {
            "style": self.style,
            "label": self.label
        }

        if self.placeholder:
            data['placeholder'] = self.placeholder

        if self.required:
            data['required'] = self.required

        if self.min_length:
            data['min_length'] = self.min_length

        if self.max_length:
            data['max_length'] = self.max_length

        if self.value:
            data['value'] = str(self.value)

        return {
            **super().to_dict(),
            **data
        }


