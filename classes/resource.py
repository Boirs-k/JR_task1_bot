import os

from aiogram.types import FSInputFile

from .enums import BotPath


class Button:
    def __init__(self, path: str):
        self._path = os.path.join(BotPath.PROMPTS.value, path + '.txt')
        with open(self._path, 'r', encoding='UTF-8') as txt_file:
            self.name = txt_file.readline().split(', ')[0][5:]
        self.callback = path


class Buttons:
    def __init__(self):
        self.buttons = self._read_buttons()

    def _read_buttons(self) -> list[Button]:
        buttons_list = [file for file in os.listdir(BotPath.PROMPTS.value) if file.startswith('talk_')]
        buttons = [Button(file.split('.')[0]) for file in buttons_list]
        return buttons

    def __iter__(self):
        return self

    def __next__(self):
        while self.buttons:
            return self.buttons.pop(0)
        raise StopIteration


class BotPhoto:
    def __init__(self, file_name: str):
        self._file_name = file_name + '.jpg'

    @property
    def photo(self) -> FSInputFile:
        photo_path = os.path.join(BotPath.IMAGES.value, self._file_name)
        return FSInputFile(photo_path)


class BotText:
    def __init__(self, file_name: str):
        self._file_name = file_name + '.txt'

    @property
    def text(self) -> str:
        text_path = os.path.join(BotPath.MESSAGES.value, self._file_name)
        with open(text_path, 'r', encoding='UTF-8') as file:
            data = file.read()
        return data
