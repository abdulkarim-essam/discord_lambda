from .user import Member
from typing import Union
class Option:


    def __init__(self, body: dict):
        print(body)
        self.name = body.get('name')
        self.value = body.get('value')
        self.type = str
        self.focused = body.get('focused') or False

    @staticmethod
    def create(body: dict, data: dict = None) -> Union['StringOption', 'MemberOption', 'IntegerOption']:
        if body.get('type') == 3:
            return StringOption(body)
        elif body.get('type') == 4:
            return IntegerOption(body)
        if body.get('type') == 6:
            return MemberOption(body, data)





class StringOption(Option):
    value: str

    def __init__(self, body: dict):
        super().__init__(body)
        self.value = body.get('value')

    def __str__(self):
        return self.value

class IntegerOption(Option):
    value: int

    def __init__(self, body: dict):
        super().__init__(body)
        self.value = int(body.get('value'))

    def __str__(self):
        return self.value


class MemberOption(Option):
    value: Member
    member: Member

    def __init__(self, body: dict, data: dict):
        super().__init__(body)
        self.__member_data = data.get('resolved', {}).get('members', {}).get(self.value)
        self.__member_data['user'] = data.get('resolved', {}).get('users', {}).get(self.value)
        self.value = Member(**self.__member_data)
        self.member = self.value

    def __str__(self):
        return self.value


class EmptyOption:
    value: None

    def __init__(self, body: dict):
        self.value = None

    def __str__(self):
        return ''
