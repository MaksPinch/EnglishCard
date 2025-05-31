import sqlalchemy
from time import sleep
import random
from telebot import types
import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot import custom_filters

from database import create_user, existsts_users, get_all_words_if_user_doesnt_exists, save_word_to_db, get_user_db_id, get_all_word_if_user_exists, delete_the_word_from_the_userwords_table


class Command:
    ADD_WORD = 'Добавить слово'
    DELETE_WORD = 'Удалить слово'
    NEXT = 'Дальше'


class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()
    new_target_word = State()
    delete_word = State()


TOKEN = '7829008577:AAGmBYr4GGHclO_2mwtjdcHclXEAjEXLskI'


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))


@bot.message_handler(commands=['start', 'cards'])
def start_the_bot(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    user_telegram_id = message.from_user.id

    if not existsts_users(user_telegram_id):
        create_user(user_telegram_id)
        russian_word, target_word, other_words = get_all_words_if_user_doesnt_exists()
    else:
        russian_word, target_word, other_words = get_all_word_if_user_exists(user_telegram_id)

    buttons = [types.KeyboardButton(target_word)] + [types.KeyboardButton(word) for word in other_words]
    random.shuffle(buttons)
    buttons.extend([
        types.KeyboardButton(Command.NEXT),
        types.KeyboardButton(Command.ADD_WORD),
        types.KeyboardButton(Command.DELETE_WORD)
    ])
    markup.add(*buttons)

    bot.send_message(message.chat.id, f'Какой перевод у слова {russian_word}?', reply_markup=markup)

    bot.set_state(user_telegram_id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(user_telegram_id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = russian_word
        data['other_words'] = other_words

@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word_step1(message):
    bot.set_state(message.from_user.id, MyStates.translate_word, message.chat.id)
    bot.send_message(message.chat.id, 'Введите новое слово на русском:')

@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word_handler(message):
    bot.set_state(message.from_user.id, MyStates.delete_word, message.chat.id)
    bot.send_message(message.chat.id, 'Введите слово, которое хотите удалить:')


@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_word_handler(message):
    # Здесь должна быть логика перехода к следующему слову
    pass

@bot.message_handler(state=MyStates.target_word, content_types=['text'])
def check_the_answer(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']

    if message.text == target_word:
        bot.send_message(message.chat.id, '✅ Верно!')
        # здесь я должен вызывать функцию которая будет брать новое слово и варианты ответов
        sleep(1.5)
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        user_telegram_id = message.from_user.id
        russian_word, target_word, other_words = get_all_word_if_user_exists(user_telegram_id)

        buttons = [types.KeyboardButton(target_word)] + [types.KeyboardButton(word) for word in other_words]
        random.shuffle(buttons)
        buttons.extend([
            types.KeyboardButton(Command.NEXT),
            types.KeyboardButton(Command.ADD_WORD),
            types.KeyboardButton(Command.DELETE_WORD)
        ])
        markup.add(*buttons)

        bot.send_message(message.chat.id, f'Какой перевод у слова {russian_word}?', reply_markup=markup)

        bot.set_state(user_telegram_id, MyStates.target_word, message.chat.id)
        with bot.retrieve_data(user_telegram_id, message.chat.id) as data:
            data['target_word'] = target_word
            data['translate_word'] = russian_word
            data['other_words'] = other_words
    else:
        bot.send_message(message.chat.id, '❌ Неверно. Попробуй ещё!')


@bot.message_handler(state=MyStates.translate_word)
def add_word_step2(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['new_translate_word'] = message.text.strip()

    bot.set_state(message.from_user.id, MyStates.new_target_word, message.chat.id)
    bot.send_message(message.chat.id, 'Теперь введите перевод на английском:')


@bot.message_handler(state=MyStates.new_target_word)
def add_word_step3(message):
    telegram_id = message.from_user.id
    user_db_id = get_user_db_id(telegram_id)
    if user_db_id is None:
        bot.send_message(message.chat.id, "Пользователь не найден в базе!")
        return

    english_word = message.text.strip()
    with bot.retrieve_data(telegram_id, message.chat.id) as data:
        russian_word = data.get('new_translate_word')

    save_word_to_db(user_db_id, russian_word, english_word)
    bot.send_message(message.chat.id, "Слово добавлено! Давай попробуем новый вопрос.")

    russian_word, target_word, other_words = get_all_word_if_user_exists(telegram_id)

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(target_word)] + [types.KeyboardButton(word) for word in other_words]
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

@bot.message_handler(state=MyStates.delete_word)
def delete_the_word_from_db(message):
    word_to_delete = message.text.strip()
    user_telegram_id = message.from_user.id
    user_id = get_user_db_id(user_telegram_id)

    if delete_the_word_from_the_userwords_table(user_id, user_telegram_id, word_to_delete):
        bot.send_message(message.chat.id, "Слово успешно удаленно! Давай попробуем новый вопрос.")

        russian_word, target_word, other_words = get_all_word_if_user_exists(user_telegram_id)

        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = [types.KeyboardButton(target_word)] + [types.KeyboardButton(word) for word in other_words]
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




if __name__ == '__main__':
    print('Bot is running...')
    bot.polling()
