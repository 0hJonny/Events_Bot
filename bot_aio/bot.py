import asyncio
import logging
import sys
import os
from typing import List

# ----

from urllib.parse import quote
import requests

# ----
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dataclasses import dataclass
from aiogram import F


IP_FLASK= os.getenv("FLASK_IP_ADDRESS")
PORT = os.getenv("FLASK_PORT")
API_FILTERED = f"http://{IP_FLASK}:{PORT}/api_v1_0/bot_api_filter"
API_LATESTS = f"http://{IP_FLASK}:{PORT}/api_v1_0/bot_api"
LIMIT = 5

# Bot token can be obtained via https://t.me/BotFather

TOKEN= os.getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


def RequesterFiltered(key: str, value: str) -> List[str]:
    answers: List[str] = []
    request: requests = requests.get(API_FILTERED, params={key: value})
    events_data = request.json()
    for event in events_data:
        event_object = event['object']
        event_municipality = event['municipality']
        event_name = event['event_name']
        event_date = event['event_date']
        event_address = event['event_address']
        link = f"https://2gis.ru/surgut/search/{quote(event_address)}"
        answers.append(f"{event_name}\nДата: {event_date}\n{event_object}.\n{event_municipality}\nМесто проведения: {event_address}\n{link}\n")
        if len(answers) == LIMIT:
            break
    if not answers:
        answers.append("Ooops! Здесь пока ничего нет!")
    return answers


@dataclass
class Event:
    object: str
    municipality: str
    event_name: str
    event_date: str
    event_address: str


request = requests.get(url = API_LATESTS)
data = request.json()

main_kb = InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text = "📝Официальный сайт", url='https://data.admhmao.ru/datasets/', callback_data="faq"),
InlineKeyboardButton(text = "📝Сургут", url='https://afisha.yandex.ru/surgut', callback_data="event"),
InlineKeyboardButton(text = "📝Когалым", url='https://afisha.yandex.ru/kogalym', callback_data="prof")
]
],row_width = 1)


events_data = request.json()


@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    kb = [
       [
           types.KeyboardButton(text="/start"),
           types.KeyboardButton(text="/ивенты"),
           types.KeyboardButton(text="/ссылки")
       ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!")
    await message.reply(f"Я бот, который расскажет тебе информацию о культурных мероприятиях и событиях в твоем городе!", reply_markup=keyboard)



@dp.message(Command('ивенты'))
async def send_events(message:types.Message):
    kb = [
        [
           types.KeyboardButton(text="Показать ивенты"),
           types.KeyboardButton(text="Отфильтровать")
       ],
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    await message.reply(f"Выбери что хочешь сделать?", reply_markup=markup)

@dp.message(F.text == "Показать ивенты")
async def show_events(message: types.Message):
    for event in events_data:
        event_object = event['object']
        event_municipality = event['municipality']
        event_name = event['event_name']
        event_date = event['event_date']
        event_address = event['event_address']
        link = f"https://2gis.ru/surgut/search/{quote(event_address)}"
        response = f"{event_name}\nДата: {event_date}\n{event_object}.\n{event_municipality}\nМесто проведения: {event_address}\n{link}\n"
        await message.answer(response, disable_web_page_preview=False)

@dp.message(F.text == "Отфильтровать")
async def filter(message: types.Message):
    kb = [
        [
           types.KeyboardButton(text="Город"),
           types.KeyboardButton(text="Месяц")
       ],
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    await message.reply(f"Выбери параметр для фильтрации", reply_markup=markup)

@dp.message(F.text == "Город")
async def city(message: types.Message):
    kb = [
        [
           types.KeyboardButton(text="Ханты-Мансийск"),
           types.KeyboardButton(text="Сургут"),
           types.KeyboardButton(text="Когалым")
       ],
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    await message.reply(f"Выбери город", reply_markup=markup)

@dp.message(F.text == "Ханты-Мансийск")
async def hmao(message: types.Message):
    answers = RequesterFiltered('city', 'Ханты-Мансийск')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)


@dp.message(F.text == "Сургут")
async def srg(message: types.Message):
    answers = RequesterFiltered('city', 'Сургут')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)
        await message.answer(answer, disable_web_page_preview=False)


@dp.message(F.text == "Когалым")
async def kogal(message: types.Message):
    answers = RequesterFiltered('city', 'Когалым')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Месяц")
async def month(message: types.Message):
    kb = [
        [
           types.KeyboardButton(text="Январь"),
           types.KeyboardButton(text="Февраль"),
           types.KeyboardButton(text="Март"),
           types.KeyboardButton(text="Апрель"),
           types.KeyboardButton(text="Май"),
           types.KeyboardButton(text="Июнь"),
           types.KeyboardButton(text="Июль"),
           types.KeyboardButton(text="Август"),
           types.KeyboardButton(text="Сентябрь"),
           types.KeyboardButton(text="Октябрь"),
           types.KeyboardButton(text="Ноябрь"),
           types.KeyboardButton(text="Декабрь")
       ],
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    await message.reply(f"Выбери месяц", reply_markup=markup)

@dp.message(F.text == "Январь")
async def yanuary(message: types.Message):
    answers = RequesterFiltered('date', 'Январь')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Февраль")
async def february(message: types.Message):
    answers = RequesterFiltered('date', 'Февраль')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Март")
async def mart(message: types.Message):
    answers = RequesterFiltered('date', 'Март')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Апрель")
async def april(message: types.Message):
    answers = RequesterFiltered('date', 'Апрель')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Май")
async def may(message: types.Message):
    answers = RequesterFiltered('date', 'Майнь')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Июнь")
async def june(message: types.Message):
    answers = RequesterFiltered('date', 'Июнь')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Июль")
async def jule(message: types.Message):
    answers = RequesterFiltered('date', 'Июль')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Август")
async def august(message: types.Message):
    answers = RequesterFiltered('date', 'Август')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Сентябрь")
async def september(message: types.Message):
    answers = RequesterFiltered('date', 'Сентябрь')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Октябрь")
async def october(message: types.Message):
    answers = RequesterFiltered('date', 'Октябрь')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Ноябрь")
async def november(message: types.Message):
    answers = RequesterFiltered('date', 'Ноябрь')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)

@dp.message(F.text == "Декабрь")
async def december(message: types.Message):
    answers = RequesterFiltered('date', 'Декабрь')
    for answer in answers:
        await message.answer(answer, disable_web_page_preview=False)


@dp.message(Command('ссылки'))
async def url_command(message:types.Message):
    await message.answer('Полезные ссылки на мероприятия в городах ХМАО:', reply_markup=main_kb)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
