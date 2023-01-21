import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from config import LoginData
from keyboard import Clinic

bot = Bot(token=LoginData.TOKEN)
dp = Dispatcher(bot)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('button'))
async def process_callback_clinic(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 1:
        adult_polik = requests.get('https://gorzdrav.spb.ru/_api/api/v2/schedule/lpu/136/specialties', headers=headers)
        result = adult_polik.json()['result']
        adult_parse_result = {element['name']: element['countFreeTicket'] for element in result}
        adult_keyboard = InlineKeyboardMarkup()
        for key, value in adult_parse_result.items():
            if 'Вакцинация' not in key and value:
                adult_keyboard.add(InlineKeyboardButton(key + ': ' + str(value), callback_data="address_"))
        await bot.send_message(callback_query.from_user.id, 'Номерки есть у следующих специалистов',
                               reply_markup=adult_keyboard)
        await callback_query.answer(text="Спасибо, что воспользовались ботом!")
    elif code == 2:
        child_polik = requests.get('https://gorzdrav.spb.ru/_api/api/v2/schedule/lpu/143/specialties', headers=headers)
        result = child_polik.json()['result']
        child_parse_result = {element['name']: element['countFreeTicket'] for element in result}
        child_keyboard = InlineKeyboardMarkup()
        for key, value in child_parse_result.items():
            if 'Вакцинация' not in key and value:
                child_keyboard.add(InlineKeyboardButton(key + ': ' + str(value), callback_data="address_"))
        await bot.send_message(callback_query.from_user.id, 'Номерки есть у следующих специалистов',
                               reply_markup=child_keyboard)
        await callback_query.answer(text="Спасибо, что воспользовались ботом!")
    elif code == 3:
        child_polik = requests.get('https://gorzdrav.spb.ru/_api/api/v2/schedule/lpu/144/specialties', headers=headers)
        result = child_polik.json()['result']
        child_parse_result = {element['name']: element['countFreeTicket'] for element in result}
        child_keyboard = InlineKeyboardMarkup()
        for key, value in child_parse_result.items():
            if 'Вакцинация' not in key and value:
                child_keyboard.add(InlineKeyboardButton(key + ': ' + str(value), callback_data="address_"))
        await bot.send_message(callback_query.from_user.id, 'Номерки есть у следующих специалистов',
                               reply_markup=child_keyboard)
        await callback_query.answer(text="Спасибо, что воспользовались ботом!")
    else:
        await bot.send_message(callback_query.from_user.id, 'Ошибка')


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nБот поможет тебе получить немного полезной информации")


@dp.message_handler(commands=['choose_clinic'])
async def process_choose_clinic(message: types.Message):
    await message.reply("Выберите, пожалуйста, клинику", reply_markup=Clinic.clinic_markup)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('Тут будет помощь')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
