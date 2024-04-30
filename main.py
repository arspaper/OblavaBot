import asyncio
import aiogram
from aiogram.types import Message

from aiogram.filters import CommandStart, Filter
from aiogram import Bot, types, Dispatcher, F
from aiogram import Router
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from aiogram.filters import CommandStart, Filter, CommandObject
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackQuery
from private.maindatabase_handler import *  # working with database
import logging
from datetime import datetime



logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')  # for logs in 'run' window

BOT_NAME = '@oblava67_bot'  # display name
TOKEN = '6827386058:AAGgan9cSSoBfzAv5hZgDVol2xcdodsES9U'

dp = Dispatcher()
router = Router()
bot = Bot(TOKEN)

#Flags:
role = ''
gender = ''
floor = ''
gender_toilet = ''
rating = 0
comment = ''


#private files
database_path = "private/maindatabase.db"
id = None


def raid_request(gender):
    return get_raider(gender)


def database_user_handler(id, type, gender):  # check if user already exists in the database (useless stuff)
    db_get_user = get_user(id)
    db_type, db_gender = db_get_user
    if db_type == None and db_gender == None:
        add_user(id, type, gender)


async def main():
    await dp.start_polling(bot)


def keyboard():
    builder = ReplyKeyboardBuilder()
    for i in ['/start', '/info', '/report']:
        builder.button(text=i)
    builder.adjust(2)
    return builder.as_markup()


class Command(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: types.Message) -> bool:
        return message.text == self.my_text


@dp.message(CommandStart())
async def welcome(message: types.Message):
    global id
    id = message.from_user.id
    await message.answer(text=f'Вас приветствует {BOT_NAME}', reply_markup=keyboard())
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Ученик',
        callback_data="Ученик")
    )

    builder.add(types.InlineKeyboardButton(
        text='Учитель',
        callback_data="Учитель")
    )

    await message.answer(
        "Выберите вашу роль!",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == 'Ученик')
async def student_welcome_msg(callback: types.CallbackQuery):
    global role
    role = 'Ученик'
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='М',
        callback_data="М")
    )
    builder.add(types.InlineKeyboardButton(
        text='Ж',
        callback_data="Ж")
    )
    await callback.message.answer(text='Выберите ваш пол!', reply_markup=builder.as_markup())

@dp.callback_query(F.data == 'Учитель')
async def teacher_welcome_msg(callback: types.CallbackQuery):
    global role
    role = 'Учитель'
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='М',
        callback_data="М")
    )
    builder.add(types.InlineKeyboardButton(
        text='Ж',
        callback_data="Ж")
    )
    await callback.message.answer(text='Выберите ваш пол!', reply_markup=builder.as_markup())

@dp.callback_query(F.data == 'М')
async def gender_selection_male(callback: types.CallbackQuery):
    global gender
    gender = 'М-'

    database_user_type = 2 if role == 'Ученик' else 1
    database_gender = 1

    await callback.message.answer(text='Можете доложить о нарушениях!'
                                    if role == 'Ученик' else 'Ожидайте уведомлений')

    database_user_handler(id, database_user_type, database_gender)


@dp.callback_query(F.data == 'Ж')
async def gender_selection_female(callback: types.CallbackQuery):
    global gender
    gender = 'Ж'

    database_user_type = 2 if role == 'Ученик' else 1
    database_gender = 2

    await callback.message.answer(text='Можете доложить о нарушениях!'
                                    if role == 'Ученик' else 'Ожидайте уведомлений')

    database_user_handler(id, database_user_type, database_gender)

@dp.message(Command("/info"))
async def info(message: types.Message):
    await message.answer(text=
                         f'Вас приветствует {BOT_NAME}!\nЕсли вы ещё не прошли аутентификацию - используйте /start\nЕсли вы учитель - ожидайте запросов\nЕсли вы ученик - вы можете использовать команду /report, для доклада о нарушении')

@dp.message(Command("/report"))
async def report(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='М',
        callback_data="Male_toilet")
    )
    builder.add(types.InlineKeyboardButton(
        text='Ж',
        callback_data="Female_toilet")
    )
    await message.answer(text=f'Где (М или Ж)', reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'Male_toilet')
async def toilet_gender_selection_male(callback: types.CallbackQuery):
    global gender_toilet
    gender_toilet = '1'
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='-1',
        callback_data="-1floor")
    )
    builder.add(types.InlineKeyboardButton(
        text='3',
        callback_data="3floor")
    )
    builder.add(types.InlineKeyboardButton(
        text='4',
        callback_data="4floor")
    )
    await callback.message.answer(text=f'Выберите этаж нарушения', reply_markup=builder.as_markup())

@dp.callback_query(F.data == 'Female_toilet')
async def toilet_gender_selection_male(callback: types.CallbackQuery):
    global gender_toilet
    gender_toilet = '2'
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='-1',
        callback_data="-1floor")
    )
    builder.add(types.InlineKeyboardButton(
        text='3',
        callback_data="3floor")
    )
    builder.add(types.InlineKeyboardButton(
        text='4',
        callback_data="4floor")
    )
    await callback.message.answer(text='Выберите этаж нарушения', reply_markup=builder.as_markup())

@dp.callback_query(F.data == '-1floor')
async def floor_selection1(callback: types.CallbackQuery):
    global floor
    floor = '-1'
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Подтвердить',
        callback_data="Done")
    )
    await callback.message.answer(text=f'Вы выбрали {gender_toilet} туалет/раздевалку на {floor} этаже', reply_markup=builder.as_markup())

@dp.callback_query(F.data == '3floor')
async def floor_selection3(callback: types.CallbackQuery):
    global floor
    floor = '3'
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Подтвердить',
        callback_data="Done")
    )
    await callback.message.answer(text=f'Вы выбрали {gender_toilet} туалет/раздевалку на {floor} этаже', reply_markup=builder.as_markup())

@dp.callback_query(F.data == '4floor')
async def floor_selection4(callback: types.CallbackQuery):
    global floor
    floor = '4'
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Подтвердить',
        callback_data="Done")
    )
    await callback.message.answer(text=f'Вы выбрали {gender_toilet} туалет/раздевалку на {floor} этаже', reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'Done')
async def notify_teachers(callback: types.CallbackQuery):
    teacher_ids = get_all_teachers()

    if not teacher_ids:  # Check if the list is empty
        print("No suitable teachers found.")
        await callback.message.answer("Подходящих рейдеров не найдено")  # Notify the user
        await callback.answer()
        return

    # Construct the notification message
    message = f"Внимание! Туалет {gender_toilet} на {floor} этаже."
    # Notify each teacher found
    for teacher_id in teacher_ids:
        try:
            await bot.send_message(chat_id=teacher_id, text=message)
            print(f"Message sent to teacher ID {teacher_id}")
        except Exception as e:
            print(f"Failed to send message to {teacher_id}: {e}")

    await callback.answer()  # Acknowledge the callback query


if __name__ == '__main__':
    print('BOT START SUCCESS')
    create_connection(database_path)  # start connection with database

    try:
        asyncio.run(main())  # start bot

    except KeyboardInterrupt:
        print('BOT STOPPED BY USER')

    finally:
        get_database(database_path)
        end_connection(database_path)