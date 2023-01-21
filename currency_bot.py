import requests
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from bs4 import BeautifulSoup
from config import LoginData
from keyboard import Currency

bot = Bot(token=LoginData.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}


class Form(StatesGroup):
    currency = State()


@dp.message_handler(commands='check_currency')
async def check_currency(message: types.Message):
    await Form.currency.set()
    await message.reply('Напиши буквенное обозначение валюты. Например: \n'
                        'GBP - Английский фунт, SEK - Шведская крона, TRY - Турецкая лира. \n'
                        'Или выбери одну из популярных кнопкой внизу', reply_markup=Currency.currency_kb)


@dp.message_handler(state=Form.currency)
async def process_currency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['currency'] = message.text
        request = requests.get(f'https://ligovka.ru/detailed/{message.text}')
        if request.status_code == 404:
            await message.reply('Напиши буквенное обозначение валюты корректно. Например: GBP, SEK, TRY\n'
                                'Или выбери одну из популярных кнопкой внизу', reply_markup=Currency.currency_kb)
        else:
            soup = BeautifulSoup(request.text, 'html.parser')
            currency = soup.find_all('td', class_='price2')
            currency_name = soup.find_all('h1')
            cur_cost = BeautifulSoup(str(currency[0]), 'html.parser').text
            cur_name = BeautifulSoup(str(currency_name[0]), 'html.parser').text
            await bot.send_message(message.chat.id, text=f'{cur_name}, на ligovka.ru стоит, {cur_cost}')


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nБот поможет тебе получить немного полезной информации")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('Тут будет помощь')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
