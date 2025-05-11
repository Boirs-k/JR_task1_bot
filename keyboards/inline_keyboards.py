from collections import namedtuple

from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes.resource import Button, Buttons
from keyboards.callback_data import CelebrityData, QuizData

QuizButton = namedtuple('Button', ['button_text', 'button_callback'])

def ikb_celebrity():
    keyboard = InlineKeyboardBuilder()
    buttons = Buttons()
    for b in buttons:
        keyboard.button(
            text=b.name,
            callback_data=CelebrityData(
                button='select_celebrity',
                file_name=b.callback,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_select_topic():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        QuizButton('Язык Python', 'quiz_prog'),
        QuizButton('Математика', 'quiz_math'),
        QuizButton('Биология', 'quiz_biology'),
    ]
    for b in buttons:
        keyboard.button(
            text=b.button_text,
            callback_data=QuizData(
                button='select_topic',
                topic=b.button_callback,
                topic_name=b.button_text,
            )
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_quiz_next(current_topic: QuizData):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        QuizButton('Дальше', 'next_question'),
        QuizButton('Сменить тему', 'change_topic'),
        QuizButton('Закончить', 'finish_quiz'),
    ]

    for b in buttons:
        keyboard.button(
            text=b.button_text,
            callback_data=QuizData(
                button=b.button_callback,
                topic=current_topic.topic,
                topic_name=current_topic.topic_name,
            ),
        )
    keyboard.adjust(2, 1)
    return keyboard.as_markup()
