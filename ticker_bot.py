import requests
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from config import LoginData
from keyboard import Ticker

bot = Bot(token=LoginData.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}


class Form(StatesGroup):
    ticker = State()


@dp.message_handler(commands='check_ticker')
async def check_ticker(message: types.Message):
    await Form.ticker.set()
    await message.reply('Напиши название тикера. Например: \n'
                        'AMZN - Amazon, NVDA - NVIDIA, ARVL - Arrival. \n'
                        'Или выбери одну из популярных кнопкой внизу', reply_markup=Ticker.ticker_kb)


@dp.message_handler(state=Form.ticker)
async def process_ticker(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ticker'] = message.text
        request = requests.get(f'https://api.nasdaq.com/api/quote/{message.text}/info?assetclass=stocks',
                               headers=headers)
        if request.json()['status']['rCode'] == 400:
            await message.reply('Напиши название тикера корректно.\nНапример: AMZN, NVDA, ARVL\n'
                                'Или выбери один из популярных кнопкой внизу', reply_markup=Ticker.ticker_kb)
        else:
            price = request.json()['data']['primaryData']['lastSalePrice']
            company_name = request.json()['data']['companyName']
            await bot.send_message(message.chat.id, text=f'Одна акция, {company_name}, стоит, {price}')


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nБот поможет тебе получить немного полезной информации")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('Тут будет помощь')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
