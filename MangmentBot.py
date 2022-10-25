from decouple import config
from asyncio.windows_events import NULL
from cgitb import text
from datetime import datetime
from email import message
from gc import callbacks
from itertools import product
import logging
from operator import index
from os import stat
from random import Random, random
from sre_parse import State
import time
from tkinter import Button
from typing import Awaitable
from unicodedata import name
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton,InlineKeyboardMarkup

import DBConnect
import main



BOT_TOKEN = config('MANGER_BOT_TOKEN')

Storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot,storage=Storage)

async def sendToManger(userID:str,dateOrder:str):
    print(str(userID)+','+str(dateOrder))

    inlineKeyboradType = InlineKeyboardMarkup(resize_keyboard=True)   
    inlineKeyboradType.add(InlineKeyboardButton(text = 'تم الأنجاز' ,callback_data = f'{userID},{dateOrder}'))

    cur = DBConnect.GetOrderInfo(userID,dateOrder)

    for row in cur.fetchall():
        await bot.send_message(5104035032,text = f'OrderID : {row[0]}\nUserID : {row[4]}\nProducts List : {row[1]}\nPriceList : {row[2]}\nDate Of Order : {row[3]}\nPhone Number : {row[8]}\nLoc : {row[7]}',reply_markup=inlineKeyboradType)


print(DBConnect.GetIDANDDateFromOrder())

@dp.callback_query_handler(text = DBConnect.GetIDANDDateFromOrder())
async def OrderDone(call : types.CallbackQuery, state:FSMContext):
    loc = ''
    await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id=call.message.message_id ,reply_markup = None)
    IDList = call.data.split(",")
    cur = DBConnect.GetOrderInfo(str(IDList[0]),str(IDList[1]))
    for row in cur:
        loc = str(row[7])

    DBConnect.UpdateDateOrder('تم العملية',str(IDList[1]),str(IDList[0]))
    await main.sendToUser(str(IDList[0]),loc)

if __name__ == '__main__':
    executor.start_polling(dp)

