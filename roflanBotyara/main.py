#!venv/bin/python
import logging
import config
import requests
import random
import time
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup as BS
logging.basicConfig(level=logging.INFO)

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)

#погода
r = requests.get('https://sinoptik.ua/погода-ульяновск/')
html = BS(r.content, 'html.parser')
for el in html.select('#content'):
    t_min = el.select('.temperature .min')[0].text
    t_max = el.select('.temperature .max')[0].text
    text = el.select('.wDescription .description')[0].text
    #print(t_min + ', ' + t_max + '\n' + text)




# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_keyboard.add(types.KeyboardButton(text="Узнать прогноз погоды в Ульяновске ⛅"))
    menu_keyboard.add(types.KeyboardButton(text="Вывести случайное число от 0 до 100 🎲"))
    menu_keyboard.add(types.KeyboardButton(text="Вывести случайный анекдот 🤡"))
    menu_keyboard.add(types.KeyboardButton(text="Отмена"))
    await message.answer("Используйте кнопки ниже для взаимодействия с ботом!", reply_markup=menu_keyboard)

#
@dp.message_handler(commands=["help"])
async def welcome(message):
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("Добро пожаловать, <strong>{0.first_name}</strong>! \n\nМеня зовут <b>РофланБотяра</b> \n\nИ здесь ты можешь узнать: \n•Прогноз погоды в Ульяновске ⛅ \n•Вывести случайное число от 0 до 100 🎲 \n•Вывести случайный анекдот 🤡".format(message.from_user), parse_mode='html')
    await message.answer("Введите /start чтобы начать работу 😎")

@dp.message_handler(commands=["rofl"])
async def welcome(message):
    await message.answer("-Зравдствуйте, у вас есть сеть магазинов? \n-Да \n-А удочка? АХВАПХАПВХАПХА 🤡")
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBCTBfC2m8oAeECq6SF_U1KqL-r2LZcQAClgIAAvNWPxdOT4yU9UEszhoE')


# Хэндлер на текстовое сообщение с текстом “Отмена”
@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено. Введите /start, чтобы начать заново.", reply_markup=remove_keyboard)

#
@dp.message_handler(content_types=['text'])
async def keyboard_answer(message: types.message):
    if message.chat.type == 'private':
        if message.text == 'Узнать прогноз погоды в Ульяновске ⛅':
            await bot.send_message(message.chat.id, "На сегодня погода в Ульяновске обстоит так:\n" + t_min + ', ' + t_max + '\n' + text)
        elif message.text == 'Вывести случайное число от 0 до 100 🎲':
            await bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'Вывести случайный анекдот 🤡':
            anekdot = 'http://anecdotica.ru/'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
            full_page = requests.get(anekdot, headers=headers)
            soup = BS(full_page.content, 'html.parser')
            convert = soup.findAll("div", {"class": "item_text"})[0].text
            await bot.send_message(message.chat.id, "🤪 RoflanAnekdot 🤣\n\n" + convert)
        else:
            await bot.send_message(message.chat.id, "Я ничего не понимаю 🤯\n\nИспользуй меню для взаимодействия со мной 🤖\n\nИли воспользуйся командами /help или /start 👨‍🦽🏳️‍🌈")



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)