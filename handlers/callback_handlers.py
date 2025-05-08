import os

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from keyboards.callback_data import CelebrityData, QuizData
from .handlers_state import CelebrityTalk
from classes import gpt_client

callback_router = Router()


@callback_router.callback_query(CelebrityData.filter(F.button == 'select_celebrity'))
async def celebrity_callbaks(callback: CallbackQuery, callback_data: CelebrityData, bot: Bot, state: FSMContext):
    photo_path = os.path.join('resources', 'images', callback_data.file_name + '.jpg')
    file_name = callback_data.file_name
    with open(os.path.join('resources', 'prompts', file_name + '.txt'), 'r', encoding='UTF-8') as file:
        celebrity_name = file.readline().split(', ')[0][5:]
    photo = FSInputFile(photo_path)
    await callback.answer(text=f'С тобой говорит {celebrity_name}')
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption='Задайте свой вопроc:',
    )

    init_message = gpt_client.init_message(file_name)['messages']
    await state.set_state(CelebrityTalk.wait_for_answer)
    await state.set_data({'messages': [init_message[0]], 'photo': photo})


@callback_router.callback_query(QuizData.filter(F.button == 'select_topic'))
async def quiz_callbaks(callback: CallbackQuery, callback_data: QuizData, bot: Bot, state: FSMContext):
    photo_path = os.path.join('resources', 'images', 'quiz.jpg')
    photo = FSInputFile(photo_path)
    topic = callback_data.topic
    await callback.answer(text=f'Вы выбрали тему {callback_data.topic_name}!')
    init_message = gpt_client.init_message('quiz')['messages']
    user_topic = {
        'role': 'user',
        'content': callback_data.topic,
    }
    data = {
        'messages': [
            init_message,
            user_topic,
        ],
    }

    response = await gpt_client.talk_request(data['messages'])
    await gpt_client.talk_request()
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption=response,
    )

    # await state.set_state(CelebrityTalk.wait_for_answer)
    # await state.set_data({'messages': [init_message[0]], 'photo': photo})
