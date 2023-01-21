import requests
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from config import LoginData
from keyboard import Weather

bot = Bot(token=LoginData.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}


class Form(StatesGroup):
    weather = State()


# Check_weather
@dp.message_handler(commands='check_weather')
async def check_weather(message: types.Message):
    await Form.weather.set()
    await message.reply('Напишите в каком городе интересна погода? Например: '
                        'Тула, Самара, Уфа. \n'
                        'Или выбери один из популярных кнопкой внизу', reply_markup=Weather.weather_kb)


@dp.message_handler(state=Form.weather)
async def process_weather(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weather'] = message.text
        request = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&APPID={LoginData.WEATHER_TOKEN}&units=metric&lang=ru')
        if request.status_code == 404:
            await message.reply('Напиши название города корректно. Например: '
                                'Тула, Самара, Moscow, Lisboa. \n'
                                'Или выбери один из популярных кнопкой внизу', reply_markup=Weather.weather_kb)
        else:
            weather = request.json()['weather'][0]['description']
            temp = int(request.json()['main']['temp'])
            feels_like = int(request.json()['main']['feels_like'])
            wind = request.json()['wind']['speed']
            await bot.send_message(message.chat.id, text=(f'Сейчас в г.{message.text} - {weather}: \n'
                                                          f'Температура: {temp}°C\n'
                                                          f'Ощущается как: {feels_like}°C\n'
                                                          f'Скорость ветра: {wind} м/с\n'))


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nБот поможет тебе получить немного полезной информации")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('Тут будет помощь')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
