import random
from telebot import types
import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot import custom_filters

from database import create_user


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'


class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()


TOKEN = '7829008577:AAGmBYr4GGHclO_2mwtjdcHclXEAjEXLskI'


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))


@bot.message_handler(commands=['start'])
def start_the_bot(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    user_telegram_id = message.from_user.id
    create_user(user_telegram_id)




    russian_word = 'Мир'
    target_word = 'Peace'
    target_word_btn = types.KeyboardButton(target_word)
    other_words = ['Blue', 'Hello', 'University']
    other_words_btns = [types.KeyboardButton(word) for word in other_words]

    buttons = [target_word_btn] + other_words_btns
    random.shuffle(buttons)


    buttons.extend([
        types.KeyboardButton(Command.NEXT),
        types.KeyboardButton(Command.ADD_WORD),
        types.KeyboardButton(Command.DELETE_WORD)
    ])

    markup.add(*buttons)

    bot.send_message(message.chat.id, f'Какой перевод у слова {russian_word}?', reply_markup=markup)


    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = russian_word
        data['other_words'] = other_words


@bot.message_handler(state=MyStates.target_word, content_types=['text'])
def check_the_answer(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']

    if message.text == target_word:
        bot.send_message(message.chat.id, '✅ Верно!')
    else:
        bot.send_message(message.chat.id, '❌ Неверно. Попробуй ещё!')

if __name__ == '__main__':
    print('Bot is running...')
    bot.polling()
