import re
import requests

session = requests.Session()
# Get_DCU
send_url = 'https://api.gibdd.mail.ru/statistic/send'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://gibdd.mail.ru',
    'Referer': 'https://gibdd.mail.ru/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}
start_send_data = 'action=main_page_show&stat_data={}'
start_send_req = session.put(send_url, headers=headers, data=start_send_data)
dcu = re.findall(r'dcu=*(\S{32})*;', start_send_req.headers['Set-Cookie'])

# Send_car_data
dcu_header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Cookie': f'dcu={dcu[0]}',
}
car_data = 'action=car_docs_send&stat_data={"number":"Х473АН178","numberChecked":true,"numberError":false,"sts":"78 49 910917","stsChecked":true,"agree":true}'.encode()
session.put(send_url, headers=dcu_header, data=car_data)
# Send_driver_data
driver_data = 'action=driver_docs_send&stat_data={"driver_license_number":"99 21 240131"}'
session.put(send_url, headers=dcu_header, data=driver_data)
# Get_CSRF
session.put('https://api.gibdd.mail.ru/user')

# Get_car_fines
car_real_data = f'car_number=Х473АН178&car_registration_number=78 49 910917'.encode()
car_req = session.post('https://api.gibdd.mail.ru/entity/car', headers=headers, data=car_real_data)
print(car_req.text)
# Get_driver_fines
driver_data = 'driver_license_number=99 21 240131'
driver_req = session.post('https://api.gibdd.mail.ru/entity/driver', headers=headers, data=driver_data)
print(driver_req.text)

final = session.get('https://api.gibdd.mail.22ru/entities/', headers=headers)
print(final.json()['data'])

# Х473АН178
# 7849910917
# 9921240131


# @dp.message_handler(commands='check_fines')
# async def check_fines(message: types.Message):
#     await Form.car_number.set()
#     await message.reply('Напишите номер машины в формате А001АА78')
#     # await Form.car_registration_number.set()
#     # await message.reply('Напишите номер СТС в формате 11 11 111111')
#     # await Form.driver_license_number.set()
#     # await message.reply('Напишите номер водительского удостоверения в формате 11 11 111111')
#
#
# @dp.message_handler(state=Form.car_number)
# async def process_fines(message: types.Message, state: FSMContext):
#     async with state.proxy() as data_car:
#         data_car['car_number'] = message.text
#         async with state.proxy() as data_car_reg:
#             await Form.car_registration_number.set()
#             await bot.send_message(message.chat.id, text='Напишите номер СТС в формате 11 11 111111')
#             data_car_reg['car_registration_number'] = message.text
#             async with state.proxy() as data_driver_license:
#                 await Form.driver_license_number.set()
#                 await bot.send_message(message.chat.id, text='Напишите номер водительского удостоверения в формате 11 11 111111')
#                 data_driver_license['driver_license_number'] = message.text
#                 # print(data_car['car_number'])
#                 # print(data_car_reg['car_registration_number'])
#                 # print(data_driver_license['driver_license_number'])
#     await state.finish()