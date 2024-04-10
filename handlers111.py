import time
import asyncio


import random
from aiogram.filters import CommandObject, Command
from aiogram.types import Message
from aiogram import Bot, types, F, Router
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from sub import bot
from databaseoffilms import filmlist

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Узнать свой ID."),
            types.KeyboardButton(text="Привязать аккаунты.")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=""
    )
    await message.answer("1", reply_markup=keyboard)


@router.message(F.text.lower() == 'узнать свой id.')
async def with_puree(message: types.Message):
    await message.reply(f"Ваш ID: {message.from_user.id}")


@router.message(F.text.lower() == 'привязать аккаунты.')
async def with_puree4e(message: types.Message):
    await message.reply("Введите ID партнера с помощью команды /id.", reply_markup=types.ReplyKeyboardRemove())


@router.message(Command("privet"))
async def cmd_start1(message: types.Message):
    await bot.send_message(554730226, 'Спасибо')


@router.message(Command("id"))
async def cmd_start1(message: types.Message, command: CommandObject):
    try:
        with open(f'{message.from_user.id}') as read:
            readid = read.read()
            readid = readid[len('link_with_account') + 1:readid.find(' ')]
        await message.answer(f'Вы уже привязаны к пользователю с ID{readid}')
    except:
        await message.answer('ID принят. Запрос отправляется...')
        global iduser
        global iduser2
        global keyboard
        iduser = command.args
        iduser2 = message.from_user.id

        kb2 = [
            [
                types.KeyboardButton(text="Принять"),

            ],
        ]
        keyboard2 = types.ReplyKeyboardMarkup(
            keyboard=kb2,
            resize_keyboard=True,
            input_field_placeholder=""
        )
        await bot.send_message(iduser, f'Вам отправлен запрос на привязку аккаунта от {iduser2}',
                               reply_markup=keyboard2)
        await message.answer('Запрос отправлен!')



@router.message(F.text.lower() == 'принять')
async def with_puree3e(message: types.Message):
    openfile = open(f'{iduser2}', 'w')
    openfile.write(f'{iduser} \n3    ')
    openfile = open(f'{iduser}', 'w')
    openfile.write(f'{iduser2} \n3 ')
    kb3 = [
        [
            types.KeyboardButton(text="Выбрать фильм"),

        ],
    ]
    keyboard3 = types.ReplyKeyboardMarkup(
        keyboard=kb3,
        resize_keyboard=True,
        input_field_placeholder=""
    )
    await message.reply("Спасибо за подключение. Вы можете начать выбирать фильмы по кнопке ниже!",
                        reply_markup=keyboard3)
    await bot.send_message(iduser2, 'Ваш партнер принял ваш запрос!', reply_markup=keyboard3)


@router.message(F.text.lower() == 'выбрать фильм')
async def chosejanr(message: types.Message):
    global film
    film = random.randint(0, 100)

    kb4 = [
        [
            types.KeyboardButton(text="Комедия"),
            types.KeyboardButton(text="Хоррор"),
            types.KeyboardButton(text="Детектив")
        ],
    ]
    keyboard4 = types.ReplyKeyboardMarkup(
        keyboard=kb4,
        resize_keyboard=True,
        input_field_placeholder=""
    )
    await message.reply("Выберети жанр фильма",
                        reply_markup=keyboard4)


@router.message(F.text.lower() == 'комедия')
async def chosefilm(message: types.Message):
    with open(f"{message.from_user.id}", 'r') as read:
        global read2
        global read1
        readall = read.read
        read1 = read.readline()
        read2 = read.readline()
        read3 = read.readline()
        read4 = read.readline()

        nubmer_of_comedy = read2[read2.rfind(' '):len(read2)]
    with open('filmbase.txt', 'r', encoding='UTF-8') as read:
        filmnamewriteinfile = read.read()

    if filmnamewriteinfile.find('3') != -1:
        global filmnameanswer
        filmnameanswer = filmnamewriteinfile[
                         filmnamewriteinfile.find(str(int(read2) - 1)) + 2: filmnamewriteinfile.find(
                             str(read2)) - 1]
        kb5 = [
            [
                types.KeyboardButton(text="Лайк"),
                types.KeyboardButton(text="Не лайк"),
                types.KeyboardButton(text="Выбрать другой жанр")
            ],
        ]
        keyboard5 = types.ReplyKeyboardMarkup(
            keyboard=kb5,
            resize_keyboard=True,
            input_field_placeholder=""
        )

        await message.reply(f'Ваш фильм:{filmnameanswer}.',
                            reply_markup=keyboard5)
        read2 = int(read2) + 1
        with open(f'{message.from_user.id}', 'w', encoding='UTF-8') as write:

            whatisit = str(read1) + str(read2) + '\n' + str(read3)

            write.writelines(whatisit)


    else:

        kb6 = [
            [

                types.KeyboardButton(text="Выбрать другой жанр")
            ],
        ]
        keyboard6 = types.ReplyKeyboardMarkup(
            keyboard=kb6,
            resize_keyboard=True,
            input_field_placeholder=""
        )
        await message.reply('Комедеии для вас закончились! Ждите обновление списка фильмов!', reply_markup=keyboard6)


@router.message(F.text.lower() == 'лайк')
async def with_puree1e(message: types.Message):
    kb7 = [
        [

            types.KeyboardButton(text="Продолжить выбирать фильм")
        ],
    ]
    keyboard7 = types.ReplyKeyboardMarkup(
        keyboard=kb7,
        resize_keyboard=True,
        input_field_placeholder=""
    )
    with open(f'{message.from_user.id}', 'r', encoding='UTF-8') as read:
        infoaboutuser = read.read()

    with open(f'{message.from_user.id}', 'w', encoding='UTF-8') as write:
        write.write(infoaboutuser + ' ' + str(read2))

    with open(f'{read1[:len(read1) - 1]}', 'r', encoding='UTF-8') as read:
        readfirst = read.readline()
        readsecond = read.readline()
        readthied = read.readline()

        if readthied.find(str(read2)) != -1:
            await message.reply(f'СОВПАДЕНИЕ. Фильм:{filmnameanswer} ', reply_markup=keyboard7)
            await bot.send_message(read1[:len(read1) - 1],
                                   f'Ваш партер выбрал фильм, который вам так же понравился. Фильм: {filmnameanswer}',
                                   reply_markup=keyboard7)

        else:
            task2 = asyncio.create_task(chosefilm(message))
            await task2


@router.message(F.text.lower() == 'не лайк')
async def with_puree1e(message: types.Message):
    task2 = asyncio.create_task(chosefilm(message))
    await task2


@router.message(F.text.lower() == 'продолжить выбирать фильм')
async def with_puree1e(message: types.Message):
    task2 = asyncio.create_task(chosefilm(message))
    await task2


@router.message(F.text.lower() == 'выбрать другой жанр')
async def with_puree1e(message: types.Message):
    task1 = asyncio.create_task(chosejanr(message))
    await task1
