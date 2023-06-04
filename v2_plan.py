# Вот самый простой код. Пишете боту команду /admin - а он отвечает в зависимости от ситуации. Например, если user_id есть в базе, и user_group_id = '1' - тогда бот приветствует админа, если user_group_id не равно '1', тогда бот приветствует пользователя. Если user_id вообще нет в базе - тогда пишет, что пользователь не зарегистрирован в базе.
import sqlite3

import telebot

token = 'ТОКЕН'

bot = telebot.TeleBot(token)


def get_access(user_id):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_group_id FROM users WHERE user_id=?',
                       (user_id,))
        result = cursor.fetchone()
        return result


@bot.message_handler(commands=['admin'])
def repeat_all_message(message):
    print(message.chat.id)
    bot.send_message(message.chat.id, message.text)

    access = get_access(message.chat.id)

    if access:
        if access[0] == '1':
            bot.send_message(message.chat.id, 'Привет Admin!')
        else:
            bot.send_message(message.chat.id, 'Привет User!')
    else:
        bot.send_message(message.chat.id, 'Вы не зарегистрированны в системе!')


if __name__ == '__main__':
    bot.polling(none_stop=True)

# PS: У меня user_group_id является строкой, но можно сделать и int;
# PS: Скорее всего за вас код никто писать не будет, потому что вы тогда ничего не поймете.
