from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Clinic:
    button1 = InlineKeyboardButton('Городская поликлиника №106, Р.Зорге 1', callback_data='button1')
    button2 = InlineKeyboardButton('Детское отделение №53, Р.Зорге 13', callback_data='button2')
    button3 = InlineKeyboardButton('Детское отделение №74, М.Захарова 31', callback_data='button3')
    clinic_markup = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        button1).add(button2).add(button3)


class Currency:
    usd_btn = KeyboardButton('USD')
    eur_btn = KeyboardButton('EUR')
    cny_bth = KeyboardButton('CNY')
    currency_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    currency_kb.row(usd_btn, eur_btn, cny_bth)


class Ticker:
    aapl_btn = KeyboardButton('AAPL')
    tsla_btn = KeyboardButton('TSLA')
    msft_bth = KeyboardButton('MSFT')
    ticker_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    ticker_kb.row(aapl_btn, tsla_btn, msft_bth)


class Weather:
    spb_btn = KeyboardButton('Санкт-Петербург')
    moscow_btn = KeyboardButton('Москва')
    ekat_bth = KeyboardButton('Екатеринбург')
    weather_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    weather_kb.add(spb_btn).add(moscow_btn).add(ekat_bth)
