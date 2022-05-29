from aiogram.dispatcher import FSMContext
import json
import scrapy
import requests
import pandas as pd
import logging
from text import*
from utils import*
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import token, ADMINS
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

def LinearSearch(lys, element):
    for i in range(len(lys)):
        if str(lys[i]["aud_num"]) == str(element):
            return lys[i]
    return - 1

def searchChief(lys, element):
    for i in range(len(lys)):
        if str(lys[i]["group"]) == str(element):
            return lys[i]
    return - 1


@dp.message_handler(commands='start')
async def start_bot(message: types.Message):
    await message.answer(text=start, parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands='help')
async def helping(message: types.Message):
    await bot.send_message(message.from_user.id, "Список моих команд:")
    await bot.send_message(message.from_user.id, commands, parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands='cancel', state='*')
async def canceling(message: types.Message, state: FSMContext):
    await message.answer("Отменяю текущее действие", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands='faq')
async def faq(message: types.Message):
    #await responsing()
    await bot.send_message(message.from_user.id, FAQ, parse_mode=types.ParseMode.HTML)


@dp.message_handler(state=Statements.find)
async def find_chief(message: types.Message):
    temp = message.text
    print(temp)
    url = 'https://rinh-api.kovalev.team/employee/surname/' + temp
    response = requests.get(url)
    jsons = response.json()
    arr = []
    print(jsons[0]['id'], len(jsons))
    if len(jsons) > 0:
        for i in range(len(jsons)):
            arr.append(jsons[i]['id'])
        print(arr)

        for i in range(len(arr)):
            urlId = 'https://rinh-api.kovalev.team/employee/dto/' + str(arr[i])
            responseId = requests.get(urlId)
            jsonsId = responseId.json()['employee']
            #print(jsonsId)
            res = jsonsId['fullName']  + '\n'+ jsonsId['email'] + '\n' + jsonsId['phone'] + '\n' + jsonsId['avatarUrl']
            await bot.send_message(message.from_user.id, res)


@dp.message_handler(commands='find_teacher')
async def print_find_chief(message: types.Message):
    await message.answer('Введи фамилию преподавателя')
    await Statements.find.set()


@dp.message_handler(state=Statements.auditor)
async def find_aud(message: types.Message):
    temp = message.text

    url = 'https://629126d327f4ba1c65c8b27f.mockapi.io/api/room'
    response = requests.get(url)
    jsons = response.json()
    data = LinearSearch(jsons, temp)

    if LinearSearch(jsons, temp) == -1:
        await bot.send_message(message.from_user.id, "Корректно введи номер аудитории!")
    else:
        res = data['aud_num'] + '\n' + data['description'] + '\n' + data['urlImage']
        await bot.send_message(message.from_user.id, res)


@dp.message_handler(state=Statements.chief)
async def find_ch(message: types.Message):
    temp = message.text

    url = 'https://629126d327f4ba1c65c8b27f.mockapi.io/api/chief'
    response = requests.get(url)
    jsons = response.json()
    data = searchChief(jsons, temp)

    if searchChief(jsons, temp) == -1:
        await bot.send_message(message.from_user.id, "Корректно введи номер группы!")
    else:
        res = data['fullName'] + '\n' + data['group'] + '\n' + data['email'] + '\n' + data['contact'] + '\n' + data['imageUrl']
        await bot.send_message(message.from_user.id, res)


@dp.message_handler(commands='find_room')
async def finding_auditor(message: types.Message):
    await message.answer('Введи номер аудитории')
    await Statements.auditor.set()


@dp.message_handler(commands='find_chief')
async def finding_chief(message: types.Message):
    await message.answer('Введи название группы, например ИДБ-21-12')
    await Statements.chief.set()


@dp.message_handler(commands='lifehacks')
async def print_lifehack(message: types.Message):
    await bot.send_message(message.from_user.id, lifehacks, parse_mode=types.ParseMode.HTML)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
