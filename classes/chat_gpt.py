import os

import openai


class ChatGPT:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.gpt_token = os.getenv('AI_TOKEN')
        self._client = self.create_client()

    def create_client(self):
        gpt_client = openai.AsyncOpenAI(api_key=self.gpt_token)
        return gpt_client

    @staticmethod
    def _load_prompt(prompt_name: str) -> str:
        prompt_path = os.path.join('resources', 'prompts', f'{prompt_name}.txt')
        with open(prompt_path, 'r', encoding='UTF-8') as file:
            prompt = file.read()
        return prompt

    def init_message(self, prompt_name: str) -> dict[str, str | list[dict[str, str]]]:
        return {
            'messages': [
                {
                    'role': 'system',
                    'content': self._load_prompt('random'),
                },
            ],
            'model': 'gpt-3.5-turbo'
        }

    async def random_request(self) -> str:
        response = await self._client.chat.completions.create(**self.init_message('random'))

        return response.choices[0].message.content

    async def gpt_request(self, request_text: str) -> str:
        key_args = self.init_message('gpt')
        key_args['messages'].append(
            {
                'role': 'user',
                'content': request_text,
            }
        )
        response = await self._client.chat.completions.create(**key_args)

        return response.choices[0].message.content

    async def talk_request(self, messages: list[dict[str, str]]) -> str:
        response = await self._client.chat.completions.create(
            messages=messages,
            model='gpt-3.5-turbo',
        )
        return response.choices[0].message.content