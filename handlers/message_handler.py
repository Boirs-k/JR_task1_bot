from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import kb_end_talk
from .command import com_start
from .handlers_state import CelebrityTalk
from classes import gpt_client

message_router = Router()


@message_router.message(CelebrityTalk.wait_for_answer, F.text == 'Попрощаться!')
async def end_talk_handler(message: Message, state: FSMContext):
    await state.clear()
    await com_start(message)


@message_router.message(CelebrityTalk.wait_for_answer)
async def talk_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    message_from_user = {
        'role': 'user',
        'content': message.text,
    }
    data['messages'].append(message_from_user)
    response = await gpt_client.talk_request(data['messages'])
    await message.answer_photo(
        photo=data['photo'],
        caption=response,
        reply_markup=kb_end_talk(),
    )
    message_from_celebrity = {
        'role': 'assistant',
        'content': response,
    }
    data['messages'].append(message_from_celebrity)
    await state.update_data(data)
