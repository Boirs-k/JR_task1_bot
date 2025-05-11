from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message

from classes import gpt_client
from classes.chat_gpt import GPTMessage
from classes.resource import BotPhoto, BotText
from keyboards import kb_reply, ikb_celebrity, ikb_select_topic
from misc import bot_thinking
from .handlers_state import ChatGPTRequests

command_router = Router()


@command_router.message(F.text == 'Закончить')
@command_router.message(Command('start'))
async def com_start(message: Message):
    photo = BotPhoto('main').photo
    buttons = [
        '/random',
        '/gpt',
        '/talk',
        '/quiz',
    ]
    message_text = BotText('main').text
    await message.answer_photo(photo=photo, caption=message_text, reply_markup=kb_reply(buttons))


@command_router.message(F.text == 'Хочу ещё факт')
@command_router.message(Command('random'))
async def com_random(message: Message):
    await bot_thinking(message)
    photo = BotPhoto('random').photo
    request_message = GPTMessage('random')
    buttons = [
        'Хочу ещё факт',
        'Закончить',
    ]
    message_text = await gpt_client.request(request_message)
    await message.answer_photo(photo=photo, caption=message_text, reply_markup=kb_reply(buttons))


@command_router.message(Command('gpt'))
async def com_gpt(message: Message, state: FSMContext):
    await state.set_state(ChatGPTRequests.wait_for_request)
    await bot_thinking(message)
    photo = BotPhoto('gpt').photo
    message_text = BotText('gpt').text
    await message.answer_photo(photo=photo, caption=message_text)


@command_router.message(Command('talk'))
async def com_talk(message: Message):
    await bot_thinking(message)
    photo = BotPhoto('talk').photo
    message_text = BotText('talk').text
    await message.answer_photo(photo=photo, caption=message_text, reply_markup=ikb_celebrity())


@command_router.message(Command('quiz'))
async def com_quiz(message: Message):
    await bot_thinking(message)
    photo = BotPhoto('quiz').photo
    message_text = BotText('quiz').text
    await message.answer_photo(photo=photo, caption=message_text, reply_markup=ikb_select_topic())
