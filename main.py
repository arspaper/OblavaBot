import asyncio
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


# TODO: Шлягеру:
## проверь private.maindatabase_handler

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')  # for logs in 'run' window
from aiogram.handlers import MessageHandler

TOKEN = '6805910622:AAFaoyIFq8QgK8msxdl6mNekSRk1XSoxbCs'

dp = Dispatcher()
bot = Bot(TOKEN)

#Flags:
role = ''
gender = ''
floor = ''
gender_toilet = ''

#private files
database_path = "private/maindatabase.db"
id = None

#TODO: Сделать функцию call_rade, которая по айди телеграмма будет отправлять сообщения рейдерам(Поликарпову)
def call_rade():
    pass


def database_user_handler(id, type, gender):
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
    await message.answer(text='Вас приветствует oblava_bot', reply_markup=keyboard())
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
        "Чтобы начать выберите кто вы:",
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
    await callback.message.answer(text='Вы отмечены, как ученик, теперь выберете пол.', reply_markup=builder.as_markup())

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
    await callback.message.answer(text='Вы отмечены, как учитель, теперь выберете пол.', reply_markup=builder.as_markup())

@dp.callback_query(F.data == 'М')
async def gender_selection_male(callback: types.CallbackQuery):
    global gender
    gender = 'М'

    database_user_type = 2 if role == 'Ученик' else 1
    database_gender = 1

    await callback.message.answer(text='Вы отмечены, как мужчина, теперь вы можете доложить о нарушении'
                                    if role == 'Ученик' else 'Вы отмечены, как мужчина, ожидайте уведомлений')

    database_user_handler(id, database_user_type, database_gender)


@dp.callback_query(F.data == 'Ж')
async def gender_selection_female(callback: types.CallbackQuery):
    global gender
    gender = 'Ж'

    database_user_type = 2 if role == 'Ученик' else 1
    database_gender = 2

    await callback.message.answer(text='Вы отмечены, как женщина, теперь вы можете доложить о нарушении'
                                    if role == 'Ученик' else 'Вы отмечены, как женщина, ожидайте уведомлений')

    database_user_handler(id, database_user_type, database_gender)

@dp.message(Command("/info"))
async def info(message: types.Message):
    await message.answer(text=
                         'Вас приветствует oblava_bot, если вы ещё не прошли аутентификацию - используйте /start, если вы прошли аутентификацию, то если вы учитель - ожидайте запросов, если вы ученик - вы можете использовать команду /report, для доклада о нарушении')



#Пока не работает репорт
# мне надо чтобы gender_toilet и floor писались отдельным сообщением в тг после message.answer


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
    await message.answer(text='Где нарушение(М или Ж)', reply_markup=builder.as_markup())

@dp.callback_query(F.data == 'Male_toilet')
async def toilet_gender_selection_male(callback: types.CallbackQuery):
    global gender_toilet
    gender_toilet = 'Male'
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
    await callback.message.answer(text='На каком этаже нарушение?', reply_markup=builder.as_markup())

@dp.callback_query(F.data == 'Female_toilet')
async def toilet_gender_selection_male(callback: types.CallbackQuery):
    global gender_toilet
    gender_toilet = 'Female'
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
    await callback.message.answer(text='На каком этаже нарушение?', reply_markup=builder.as_markup())

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
async def rade_called(callback: types.CallbackQuery):
    await callback.message.answer(text='Рейд вызван')
    #Функция отправки сообщения гангерам
    call_rade()

if __name__ == '__main__':
    print('BOT START SUCCESS')
    create_connection(database_path)  # start connection with database

    try:
        asyncio.run(main())  # start bot

    except KeyboardInterrupt:
        print('BOT STOPPED BY USER')

    finally:
        end_connection(database_path)
        get_database(database_path)