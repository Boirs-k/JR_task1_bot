from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types.message import Message
from classes import gpt_client
from classes.chat_gpt import GPTMessage
from classes.enums import GPTRole
from classes.resource import BotPhoto, Button, BotText
from keyboards import ikb_select_topic
from keyboards.callback_data import CelebrityData, QuizData
from .command import com_start
from .handlers_state import CelebrityTalk, Quiz

callback_router = Router()


@callback_router.callback_query(CelebrityData.filter(F.button == 'select_celebrity'))
async def celebrity_callbacks(callback: CallbackQuery, callback_data: CelebrityData, bot: Bot, state: FSMContext):
    photo = BotPhoto(callback_data.file_name).photo
    file_name = callback_data.file_name
    button_name = Button(file_name).name
    await callback.answer(text=f'С тобой говорит {button_name}')
    await bot.send_photo(chat_id=callback.from_user.id, photo=photo, caption='Задайте свой вопроc:')

    request_message = GPTMessage(file_name)
    await state.set_state(CelebrityTalk.wait_for_answer)
    await state.set_data({'messages': request_message, 'photo': photo})


@callback_router.callback_query(QuizData.filter(F.button == 'select_topic'))
async def quiz_callbacks(callback: CallbackQuery, callback_data: QuizData, bot: Bot, state: FSMContext):
    await state.clear()
    photo = BotPhoto('quiz').photo
    await callback.answer(text=f'Вы выбрали тему {callback_data.topic_name}!')
    request_message = GPTMessage('quiz')
    request_message.update(GPTRole.USER, callback_data.topic)
    response = await gpt_client.request(request_message)
    await bot.send_photo(chat_id=callback.from_user.id, photo=photo, caption=response)
    request_message.update(GPTRole.ASSISTANT, response)
    await state.set_data({'messages': request_message, 'photo': photo, 'score': 0, 'callback': callback_data})
    await state.set_state(Quiz.wait_for_answer)


@callback_router.callback_query(QuizData.filter(F.button == 'next_question'))
async def quiz_next_question(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data['messages'].update(GPTRole.USER, 'quiz_more')
    response = await gpt_client.request(data['messages'])
    await callback.bot.send_photo(chat_id=callback.from_user.id, photo=data['photo'], caption=response)
    data['messages'].update(GPTRole.ASSISTANT, response)
    await state.set_state(Quiz.wait_for_answer)
    await state.update_data(data)


@callback_router.callback_query(QuizData.filter(F.button == 'change_topic'))
async def quiz_next_question(callback: CallbackQuery):
    photo = BotPhoto('quiz').photo
    message_text = BotText('quiz').text
    await callback.bot.send_photo(chat_id=callback.from_user.id, photo=photo, caption=message_text,
                                  reply_markup=ikb_select_topic())


@callback_router.callback_query(QuizData.filter(F.button == 'finish_quiz'))
async def quiz_next_question(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = f'Квиз окончен, итоговый счёт {data['score']}!'
    await callback.bot.send_photo(chat_id=callback.from_user.id, photo=data['photo'], caption=message)
    await state.clear()
