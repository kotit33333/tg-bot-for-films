import asyncio

from diffclass import ChoosingFilm
from aiogram.filters import CommandObject, Command
from aiogram.types import Message
from aiogram import Bot, types, F, Router
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
import pymysql

router = Router()

pysto = [
    [
        types.KeyboardButton(text="Вернуться в начало")

    ],
]
pysto_kb = types.ReplyKeyboardMarkup(
    keyboard=pysto,
    resize_keyboard=True,
    input_field_placeholder=""
)

last_kb = [
    [
        types.KeyboardButton(text="Нравится"),
        types.KeyboardButton(text="Не нравится"),
        types.KeyboardButton(text="Перестать выбирать фильмы"),

    ],
]
like_kb = types.ReplyKeyboardMarkup(
    keyboard=last_kb,
    resize_keyboard=True,
    input_field_placeholder=""
)
something = [
    [
        types.KeyboardButton(text="Выбирать фильмы"),

    ],
]
kbsomth = types.ReplyKeyboardMarkup(
    keyboard=something,
    resize_keyboard=True,
    input_field_placeholder=""
)


@router.message(F.text.lower() == 'вернуться в начало')
async def otkaz(message: types.Message):
    await message.answer('напишите /start, что бы вернуться в начало')


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здравствуйте! Я Телеграмм-бот для выбора фильма. Я имею следующие команды:\n"
                         "/id (номер id) - для привязки к Вашему другу\n"
                         "/myid - узнать Ваш id\n"
                         "/start - я снова повторю Вам мои команды \n"
                         "Я могу подробно все описать по команде /help!")


@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer('Я бот, который помогает Вам с Вашем с другом выбрать фильм. Как мной пользоваться? Все очень '
                         'просто: \n1. Узнайте у своего друга id. Это можно сделать прям у меня, написав команду /myid, '
                         'либо'
                         ',если Вы мне не доверяете, в любом другом боте ТГ. \n2. Вам нужно прописать команду /id (id '
                         'Вашего друга) и ему придёт потверждение запрос\n'
                         '3. Выберите, какой Вы хотите смотреть жанр и выбирайте нравится Вам фильм или нет. Вашему '
                         'другу будут предложены эти же фильмы и когда у вас будет совпадения, то я скажу Вам об этом')

# Обработчик команды /myid
@router.message(Command('myid'))
async def get_user_id(message: types.Message):
    user_id = message.from_user.id
    await message.answer(f"Ваш ID: {user_id}")


# Обработчик команды /id


@router.message(Command('id'))
async def set_friend_id(message: types.Message):
    # Проверяем, был ли передан аргумент вместе с командой /id
    if len(message.text.split()) > 1:
        friend_id = message.text.split()[1]

        # Проверяем, не пустой ли запрос
        if friend_id == "":
            await message.answer("Вы забыли указать id")
            return

        # Проверяем, указывается ли id того же человека, что и отправляет запрос
        if friend_id == str(message.from_user.id):
            await message.answer("У тебя нет друзей и ты пытаешься выбрать фильм один?")
            return

        # Подключаемся к базе данных
        connection = pymysql.connect(host='localhost',
                                     user='Kotit',
                                     password='141923vaniqwerty',
                                     db='pythonbot',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Проверяем, есть ли уже такой пользователь в БД
                sql_check_user = "SELECT * FROM user WHERE tgid = %s OR linktgid = %s"
                cursor.execute(sql_check_user, (message.from_user.id, friend_id))
                result = cursor.fetchone()
                if result:
                    # Если пользователь уже есть в БД, выводим клавиатуру

                    kb = [
                        [
                            types.KeyboardButton(text="Перестать выбирать фильмы"),
                            types.KeyboardButton(text="Продолжить выбирать фильмы")
                        ],
                    ]
                    keyboard = types.ReplyKeyboardMarkup(
                        keyboard=kb,
                        resize_keyboard=True,
                        input_field_placeholder=""
                    )
                    await message.answer("Этот пользователь уже добавлен в ваш список друзей.", reply_markup=keyboard)
                else:
                    # Отправляем пользователю с указанным id запрос на дружбу
                    kb = [
                        [
                            types.KeyboardButton(text="Принять"),
                            types.KeyboardButton(text="Отказаться")
                        ],
                    ]
                    keyboard = types.ReplyKeyboardMarkup(
                        keyboard=kb,
                        resize_keyboard=True,
                        input_field_placeholder=""
                    )

                    sql_add_user = "INSERT INTO user (tgid, linktgid, likefilm) VALUES (%s, %s, %s)"
                    cursor.execute(sql_add_user, (message.from_user.id, friend_id, 0))
                    sql_add_user = "INSERT INTO user (tgid, linktgid, likefilm) VALUES (%s, %s, %s)"
                    cursor.execute(sql_add_user, (friend_id, message.from_user.id, 0))
                    connection.commit()
                    await message.bot.send_message(friend_id,
                                                   "Вам отправили запрос на дружбу. Выберете дальнейшие действия:",
                                                   reply_markup=keyboard)
        finally:
            connection.close()
    else:
        await message.answer("Пожалуйста, укажите id вашего друга после команды /id.")


@router.message(F.text.lower() == 'отказаться')
async def otkaz(message: types.Message):
    await message.answer("Вы отказались от выбора фильмов!")
    connection = pymysql.connect(host='localhost',
                                 user='Kotit',
                                 password='141923vaniqwerty',
                                 db='pythonbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Удаляем записи из базы данных
            sql_delete_user = "DELETE FROM user WHERE tgid = %s OR linktgid = %s"
            cursor.execute(sql_delete_user, (message.from_user.id, message.from_user.id))
            connection.commit()
    finally:
        connection.close()


@router.message(F.text.lower() == 'принять')
async def accept(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Cемейный"),
            types.KeyboardButton(text="Фантастика"),
            types.KeyboardButton(text="Хоррор"),
            types.KeyboardButton(text="Боевик"),
            types.KeyboardButton(text="Мультик"),
            types.KeyboardButton(text="Триллер")

        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=""
    )
    await message.answer("Спасибо, что приняли запрос! Ваш друг сейчас выбирает жанры!")

    connection = pymysql.connect(host='localhost',
                                 user='Kotit',
                                 password='141923vaniqwerty',
                                 db='pythonbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Выполняем SQL-запрос для выборки строки из БД
            sql_select = "SELECT linktgid FROM user WHERE tgid = %s"
            cursor.execute(sql_select, (message.from_user.id,))

            # Получаем результат запроса
            result = cursor.fetchone()

            # Если строка найдена, читаем значение lingtgid
            if result:
                lingtgid_value = result['linktgid']
                await message.bot.send_message(lingtgid_value, 'Ваш друг принял запросы! Выберите жанр, который хотите '
                                                               'посмотреть', reply_markup=keyboard)
    finally:
        # Всегда закрываем соединение с БД после использования
        connection.close()


@router.message(F.text.lower() == 'cемейный')
async def famaly(message: types.Message):
    connection = pymysql.connect(host='localhost',
                                 user='Kotit',
                                 password='141923vaniqwerty',
                                 db='pythonbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql_select = "SELECT * FROM user WHERE tgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))

        result = cursor.fetchone()
        sql_select = "SELECT * FROM user WHERE linktgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))
        result2 = cursor.fetchone()
        if result2['nubmerfilm'] == 0:
            sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
            cursor.execute(sql_update, (1, result2['tgid']))
            # Подтверждаем изменения в БД
        connection.commit()
        if result2['nubmerfilm'] == 0:
            await message.bot.send_message(result2['tgid'], 'Ваш друг выбрал жанр. Готовы приступить к выбору фильмов?',
                                           reply_markup=kbsomth)
        lingtgid_value = result['linktgid']
        tgid_value = result['tgid']

    if result['nubmerfilm'] == 0:
        Family = ChoosingFilm(result['nubmerfilm'], 'family')
    else:
        Family = ChoosingFilm(1, 'family')
    if Family.check_film():
        await message.reply_photo(
            photo=types.FSInputFile(
                path=f'C:/Users/kotit/Desktop/егэ/{Family.check_film()["NumberFilm"]}.jpg'
            )
        )
        await message.bot.send_message(tgid_value, f'{Family.check_film()["NameFilm"]} \n '
                                                   f'{Family.check_film()["DescribeFilm"]}', reply_markup=like_kb)

        try:
            with connection.cursor() as cursor:
                # Выполняем SQL-запрос для обновления значения столбца numberfilm
                sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
                cursor.execute(sql_update, (Family.check_film()["NumberFilm"] + 1, message.from_user.id))
                # Подтверждаем изменения в БД
                connection.commit()

        finally:
            # Всегда закрываем соединение с БД после использования
            connection.close()


@router.message(F.text.lower() == 'фантастика')
async def fantasion(message: types.Message):
    connection = pymysql.connect(host='localhost',
                                 user='Kotit',
                                 password='141923vaniqwerty',
                                 db='pythonbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql_select = "SELECT * FROM user WHERE tgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))

        result = cursor.fetchone()
        sql_select = "SELECT * FROM user WHERE linktgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))
        result2 = cursor.fetchone()
        print(result2)
        if result2['nubmerfilm'] == 0:
            sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
            cursor.execute(sql_update, (21, result2['tgid']))
            # Подтверждаем изменения в БД
        connection.commit()
        if result2['nubmerfilm'] == 0:
            await message.bot.send_message(result2['tgid'], 'Ваш друг выбрал жанр. Готовы приступить к выбору фильмов?',
                                           reply_markup=kbsomth)
        lingtgid_value = result['linktgid']
        tgid_value = result['tgid']

    if result['nubmerfilm'] == 0:
        Fantasy = ChoosingFilm(21, 'fantasy')

        Fantasy = ChoosingFilm(result['nubmerfilm'], 'fantasy')
    else:
        Fantasy = ChoosingFilm(result['nubmerfilm'], 'fantasy')
    if Fantasy.check_film():
        await message.reply_photo(
            photo=types.FSInputFile(
                path=f'C:/Users/kotit/Desktop/егэ/{Fantasy.check_film()["NumberFilm"]}.jpg'
            )
        )
        await message.bot.send_message(tgid_value, f'{Fantasy.check_film()["NameFilm"]} \n '
                                                   f'{Fantasy.check_film()["DescribeFilm"]}', reply_markup=like_kb)

        try:
            with connection.cursor() as cursor:
                # Выполняем SQL-запрос для обновления значения столбца numberfilm
                sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
                cursor.execute(sql_update, (Fantasy.check_film()["NumberFilm"] + 1, message.from_user.id))
                # Подтверждаем изменения в БД
                connection.commit()

        finally:
            # Всегда закрываем соединение с БД после использования
            connection.close()


@router.message(F.text.lower() == 'хоррор')
async def horror(message: types.Message):
    connection = pymysql.connect(host='localhost',
                                 user='Kotit',
                                 password='141923vaniqwerty',
                                 db='pythonbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql_select = "SELECT * FROM user WHERE tgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))

        result = cursor.fetchone()
        sql_select = "SELECT * FROM user WHERE linktgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))
        result2 = cursor.fetchone()
        if result2['nubmerfilm'] == 0:
            sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
            cursor.execute(sql_update, (38, result2['tgid']))
            # Подтверждаем изменения в БД
        connection.commit()
        if result2['nubmerfilm'] == 0:
            await message.bot.send_message(result2['tgid'], 'Ваш друг выбрал жанр. Готовы приступить к выбору фильмов?',
                                           reply_markup=kbsomth)
        lingtgid_value = result['linktgid']
        tgid_value = result['tgid']

    if result['nubmerfilm'] == 0:
        horror1 = ChoosingFilm(38, 'horror')
    else:
        horror1 = ChoosingFilm(result['nubmerfilm'], 'horror')
    if horror1.check_film():
        await message.reply_photo(
            photo=types.FSInputFile(
                path=f'C:/Users/kotit/Desktop/егэ/{horror1.check_film()["NumberFilm"]}.jpg'
            )
        )
        await message.bot.send_message(tgid_value, f'{horror1.check_film()["NameFilm"]} \n '
                                                   f'{horror1.check_film()["DescribeFilm"]}', reply_markup=like_kb)

        try:
            with connection.cursor() as cursor:
                # Выполняем SQL-запрос для обновления значения столбца numberfilm
                sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
                cursor.execute(sql_update, (horror1.check_film()["NumberFilm"] + 1, message.from_user.id))
                # Подтверждаем изменения в БД
                connection.commit()

        finally:
            # Всегда закрываем соединение с БД после использования
            connection.close()


@router.message(F.text.lower() == 'боевик')
async def weaponer(message: types.Message):
    connection = pymysql.connect(host='localhost',
                                 user='Kotit',
                                 password='141923vaniqwerty',
                                 db='pythonbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql_select = "SELECT * FROM user WHERE tgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))

        result = cursor.fetchone()
        sql_select = "SELECT * FROM user WHERE linktgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))
        result2 = cursor.fetchone()
        if result2['nubmerfilm'] == 0:
            sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
            cursor.execute(sql_update, (61, result2['tgid']))
            sql_update = "UPDATE user SET nubmerfilm = %s WHERE linktgid = %s"
            cursor.execute(sql_update, (61, result2['tgid']))
            # Подтверждаем изменения в БД
        connection.commit()
        if result2['nubmerfilm'] == 0:
            await message.bot.send_message(result2['tgid'], 'Ваш друг выбрал жанр. Готовы приступить к выбору фильмов?',
                                           reply_markup=kbsomth)
        lingtgid_value = result['linktgid']
        tgid_value = result['tgid']

    if result['nubmerfilm'] == 0:
        weaponere = ChoosingFilm(61, 'weaponer')
        weaponere = ChoosingFilm(result['nubmerfilm'], 'weaponer')
    else:
        weaponere = ChoosingFilm(result['nubmerfilm'], 'weaponer')
    if weaponere.check_film():
        await message.reply_photo(
            photo=types.FSInputFile(
                path=f'C:/Users/kotit/Desktop/егэ/{weaponere.check_film()["NumberFilm"]}.jpg'
            )
        )
        await message.bot.send_message(tgid_value, f'{weaponere.check_film()["NameFilm"]} \n '
                                                   f'{weaponere.check_film()["DescribeFilm"]}', reply_markup=like_kb)

        try:
            with connection.cursor() as cursor:
                # Выполняем SQL-запрос для обновления значения столбца numberfilm
                sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
                cursor.execute(sql_update, (weaponere.check_film()["NumberFilm"] + 1, message.from_user.id))
                # Подтверждаем изменения в БД
                connection.commit()

        finally:
            # Всегда закрываем соединение с БД после использования
            connection.close()


@router.message(F.text.lower() == 'мультик')
async def cartoon(message: types.Message):
    connection = pymysql.connect(host='localhost',
                                 user='Kotit',
                                 password='141923vaniqwerty',
                                 db='pythonbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql_select = "SELECT * FROM user WHERE tgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))

        result = cursor.fetchone()
        sql_select = "SELECT * FROM user WHERE linktgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))
        result2 = cursor.fetchone()
        print(result2)
        if result2['nubmerfilm'] == 0:
            sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
            cursor.execute(sql_update, (80, result2['tgid']))
            sql_update = "UPDATE user SET nubmerfilm = %s WHERE linktgid = %s"
            cursor.execute(sql_update, (80, result2['tgid']))
            task2 = asyncio.create_task(dislikefiml(message))

            await task2
            # Подтверждаем изменения в БД
        connection.commit()
        if result2['nubmerfilm'] == 0:
            await message.bot.send_message(result2['tgid'], 'Ваш друг выбрал жанр. Готовы приступить к выбору фильмов?',
                                           reply_markup=kbsomth)
        lingtgid_value = result['linktgid']
        tgid_value = result['tgid']

    if result['nubmerfilm'] == 0:
        cartoon1 = ChoosingFilm(80, 'cartoon')
    else:
        cartoon1 = ChoosingFilm(result['nubmerfilm'], 'cartoon')
    if cartoon1.check_film():
        await message.reply_photo(
            photo=types.FSInputFile(
                path=f'C:/Users/kotit/Desktop/егэ/{cartoon1.check_film()["NumberFilm"]}.jpg'
            )
        )
        await message.bot.send_message(tgid_value, f'{cartoon1.check_film()["NameFilm"]} \n '
                                                   f'{cartoon1.check_film()["DescribeFilm"]}', reply_markup=like_kb)

        try:
            with connection.cursor() as cursor:
                # Выполняем SQL-запрос для обновления значения столбца numberfilm
                sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
                cursor.execute(sql_update, (cartoon1.check_film()["NumberFilm"] + 1, message.from_user.id))
                # Подтверждаем изменения в БД
                connection.commit()

        finally:
            # Всегда закрываем соединение с БД после использования
            connection.close()


@router.message(F.text.lower() == 'триллер')
async def triller(message: types.Message):
    connection = pymysql.connect(host='localhost',
                                 user='Kotit',
                                 password='141923vaniqwerty',
                                 db='pythonbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql_select = "SELECT * FROM user WHERE tgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))

        result = cursor.fetchone()
        sql_select = "SELECT * FROM user WHERE linktgid = %s"
        cursor.execute(sql_select, (message.from_user.id,))
        result2 = cursor.fetchone()
        if result2['nubmerfilm'] == 0:
            sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
            cursor.execute(sql_update, (100, result2['tgid']))
            # Подтверждаем изменения в БД
        connection.commit()
        if result2['nubmerfilm'] == 0:
            await message.bot.send_message(result2['tgid'], 'Ваш друг выбрал жанр. Готовы приступить к выбору фильмов?',
                                           reply_markup=kbsomth)
        lingtgid_value = result['linktgid']
        tgid_value = result['tgid']

    if result['nubmerfilm'] == 0:
        triller1 = ChoosingFilm(100, 'triller')
    else:
        triller1 = ChoosingFilm(result['nubmerfilm'], 'triller')
    if triller1.check_film():
        await message.reply_photo(
            photo=types.FSInputFile(
                path=f'C:/Users/kotit/Desktop/егэ/{triller1.check_film()["NumberFilm"]}.jpg'
            )
        )
        await message.bot.send_message(tgid_value, f'{triller1.check_film()["NameFilm"]} \n '
                                                   f'{triller1.check_film()["DescribeFilm"]}', reply_markup=like_kb)

        try:
            with connection.cursor() as cursor:
                # Выполняем SQL-запрос для обновления значения столбца numberfilm
                sql_update = "UPDATE user SET nubmerfilm = %s WHERE tgid = %s"
                cursor.execute(sql_update, (triller1.check_film()["NumberFilm"] + 1, message.from_user.id))
                # Подтверждаем изменения в БД
                connection.commit()

        finally:
            # Всегда закрываем соединение с БД после использования
            connection.close()


@router.message(F.text.lower() == 'нравится')
async def likefiml(message: types.Message):
    # Подключаемся к базе данных
    connection = pymysql.connect(host='localhost',
                                 user='Kotit',
                                 password='141923vaniqwerty',
                                 db='pythonbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql_select = "SELECT * FROM user WHERE tgid = %s"
            cursor.execute(sql_select, (message.from_user.id,))
            result = cursor.fetchone()
            nubmer_valuetg = result['nubmerfilm']
            like_valuetg = result['likefilm']
            sql_select = "SELECT * FROM user WHERE linktgid = %s"
            cursor.execute(sql_select, (message.from_user.id,))
            result2 = cursor.fetchone()

            like_value_link = result['likefilm']
            if like_valuetg:
                like_valuetg = like_valuetg.split()
                like_valuetg.append(str(int(nubmer_valuetg - 1)))
                like_valuetg.append(' ')
                like_valuetg = ' '.join(like_valuetg)
            else:
                like_valuetg = nubmer_valuetg - 1
            sql_update = "UPDATE user SET likefilm = %s WHERE tgid = %s"
            cursor.execute(sql_update, (like_valuetg, message.from_user.id))
            # Подтверждаем изменения в БД
            connection.commit()
            try:

                if str(nubmer_valuetg - 1) in result2['likefilm'].split():
                    sql_select = "SELECT * FROM film WHERE NumberFilm = %s"
                    cursor.execute(sql_select, (nubmer_valuetg - 1))
                    result3 = cursor.fetchone()
                    await message.answer(f'MATCH! Вам обоим понравился фильм {result3["NameFilm"]}. Спасибо, что '
                                         f'воспользовалсь мной')
                    task2 = asyncio.create_task(stop_choosing_genre(message))

                    await task2
            except TypeError:
                pass
            task2 = asyncio.create_task(dislikefiml(message))

            await task2

    finally:
        # Всегда закрываем соединение с БД после использования
        connection.close()


@router.message(F.text.lower() == 'выбирать фильмы')
async def perexod(message: types.Message):
    task2 = asyncio.create_task(dislikefiml(message))

    await task2


@router.message(F.text.lower() == 'не нравится')
async def dislikefiml(message: types.Message):
    connection = pymysql.connect(host='localhost',
                                 user='Kotit',
                                 password='141923vaniqwerty',
                                 db='pythonbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql_select = "SELECT * FROM user WHERE tgid = %s"
            cursor.execute(sql_select, (message.from_user.id,))

            result = cursor.fetchone()
            nubmer_value = result['nubmerfilm']
            if 1 <= nubmer_value <= 20:
                task2 = asyncio.create_task(famaly(message))

                await task2
            elif 21 <= nubmer_value <= 37:
                task2 = asyncio.create_task(fantasion(message))

                await task2
            elif 38 <= nubmer_value <= 60:
                task2 = asyncio.create_task(horror(message))

                await task2
            elif 61 <= nubmer_value <= 79:
                task2 = asyncio.create_task(weaponer(message))

                await task2
            elif 80 <= nubmer_value <= 99:
                task2 = asyncio.create_task(cartoon(message))

                await task2
            elif 100 <= nubmer_value <= 117:
                task2 = asyncio.create_task(triller(message))

                await task2

    finally:
        # Всегда закрываем соединение с БД после использования
        connection.close()


@router.message(F.text.lower() == 'перестать выбирать фильмы')
async def stop_choosing_genre(message: types.Message):
    # Подключаемся к базе данных
    connection = pymysql.connect(host='localhost',
                                 user='Kotit',
                                 password='141923vaniqwerty',
                                 db='pythonbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Удаляем записи из базы данных
            sql_delete_user = "DELETE FROM user WHERE tgid = %s OR linktgid = %s"
            cursor.execute(sql_delete_user, (message.from_user.id, message.from_user.id))
            connection.commit()
            await message.answer("Вы больше не будете выбирать фильмы.", reply_markup=pysto_kb)
    finally:
        connection.close()
