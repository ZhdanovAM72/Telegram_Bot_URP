# Есть еще вариант авторизации на 2022 год, Aiogram 2 версии + PostgresSQL (DB GINO). Используется FSM - машинное состояние. Получаем из БД юзера если где у этого юзера указан логин и пароль для авторизации.

# Код

from aiogram import types
from aiogram.dispatcher import FSMContext
from filters import IsPrivate_call
from loader import dp
from states import authorization_admins
from utils.misc import rate_limit
from utils.db_api import cmd_admins as commands



# Хендлер Авторизации Админа
@rate_limit(limit=5)
# вызывается с помощью инлаин кнопки либо можете указать dp.message.handler и назначить ему команду, в моём случае через колбэк.
@dp.callback_query_handler(IsPrivate_call(), text_contains='administrator')
async def auth_admin(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer(f'Введите Логин:')
    await authorization_admins.login.set()


@dp.message_handler(state=authorization_admins.login)
async def login(message: types.Message, state: FSMContext):
    login = message.text
    admins = await commands.select_admin(message.from_user.id)
    if login in admins.login:
        await message.answer('Логин принят')
    else:
        await message.answer('Не правильный логин')
    await state.update_data(text=login)
    await message.answer('Введите пароль: ')
    await authorization_admins.password.set()


@dp.message_handler(state=authorization_admins.password)
async def password(message: types.Message, state: FSMContext):
    password = message.text
    admins = await commands.select_admin(message.from_user.id)
    if password in admins.password:
        await message.answer('Пароль принят')
    else:
        await message.answer('Не правильный пароль')
    await message.answer('Вы авторизированы как Админ')
    await state.update_data(text=password)
    await state.finish()




from random import choice


def generate_code():
    digits = '0123456789'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    punctuation = '!#$%&*+-=?@^_'
    ally = digits + uppercase + lowercase + punctuation

    chars = ''

    pwd_length = int(input('Введите желаемую длину пароля: '))
    pwd_auto = input('Сгенерировать пароль автоматически? (y, n): ')

    if pwd_auto == 'y':
        chars += ally
    else:
        pwd_digits = input('Включить цифры (y, n): ')
        pwd_uppercase = input('Включить uppercase (y, n): ')
        pwd_lowercase = input('Включить lowercase (y, n): ')
        pwd_punctuation = input('Включить спец. символы (y, n): ')
        if pwd_digits == 'y':
            chars += digits
        if pwd_uppercase == 'y':
            chars += uppercase
        if pwd_lowercase == 'y':
            chars += lowercase
        if pwd_punctuation == 'y':
            chars += punctuation

    password = ''

    for i in range(pwd_length):
        password += choice(chars)
    print(password)
    return (password)



generate_code()