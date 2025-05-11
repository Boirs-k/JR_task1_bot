import os
from enum import Enum


class BotPath(Enum):
    RESOURCES = 'resources'
    IMAGES = os.path.join(RESOURCES, 'images')
    MESSAGES = os.path.join(RESOURCES, 'messages')
    PROMPTS = os.path.join(RESOURCES, 'prompts')


class GPTRole(Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'
