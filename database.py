import sqlalchemy
from sqlalchemy.orm import sessionmaker
import random
from random import shuffle



from models import create_tables, CommonWords, UserWords, Users
from sqlalchemy.exc import IntegrityError
DSN = 'postgresql://postgres:130006@localhost:5432/EnglishWord'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

words = [
    ('Я', 'I'),
    ('Ты', 'You'),
    ('Он', 'He'),
    ('Она', 'She'),
    ('Мы', 'We'),
    ('Красный', 'Red'),
    ('Синий', 'Blue'),
    ('Зелёный', 'Green'),
    ('Чёрный', 'Black'),
    ('Белый', 'White'),
]

for rus, eng in words:
    exists = session.query(CommonWords).filter(CommonWords.russian_word == rus).first()

    if exists:
        continue
    else:
        word = CommonWords(russian_word=rus, english_word=eng)
        session.add(word)
        session.commit()

def create_user(personal_id):
    session = Session()
    try:
        users_exists = session.query(Users).filter(Users.telegram_id == personal_id).first()

        if users_exists:
            pass
        else:
            user = Users(telegram_id=personal_id)
            session.add(user)
            session.commit()
    except Exception as e:
        print("Ошибка при создании пользователя")
    finally:
        session.close()


def existsts_users(personal_id):
    session = Session()
    try:
        users_exists = session.query(Users).filter(Users.telegram_id==personal_id).first()

        if users_exists:
            return True
        else:
            return False
    except Exception as e:
        print("Ошибка при нахождении пользователя")
    finally:
        session.close()

def get_user_db_id(telegram_id):
    session = Session()
    try:
        user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
        return user.id if user else None
    finally:
        session.close()


def user_has_words(telegram_id):
    session = Session()
    try:
        user_id = get_user_db_id(telegram_id)
        if not user_id:
            return False

        count = session.query(UserWords).filter(UserWords.user_id == user_id).count()
        return count > 0

    except Exception as e:
        print(f'Ошибка {e}')
    finally:
        session.close()

def get_all_words_if_user_doesnt_exists():
    session = Session()
    try:
        lst_of_words = session.query(CommonWords.id).all()
        random.shuffle(lst_of_words)
        random_id = lst_of_words[0][0]
        russian_word, target_word = session.query(CommonWords.russian_word, CommonWords.english_word).filter(
            CommonWords.id == random_id).first()


        lst_of_other_words = [word[0] for word in session.query(CommonWords.english_word).filter(CommonWords.id != random_id).all()[:3]]

        return [russian_word, target_word, lst_of_other_words]
    except Exception as e:
        session.rollback()
        print("Ошибка при выыоде учебных слов")

    finally:
        session.close()

def get_all_word_if_user_exists(telegram_id):
    session = Session()

    try:
        user_id = get_user_db_id(telegram_id)
        if user_has_words(telegram_id):
            lst_of_common_words = session.query(CommonWords.russian_word, CommonWords.english_word).all()
            first_lst = [word for word in lst_of_common_words]
            lst_of_users_words = session.query(UserWords.russian_word, UserWords.english_word).filter(
                UserWords.user_id == user_id)
            second_lst = [word for word in lst_of_users_words]

            final_lst = first_lst + second_lst

            random.shuffle(final_lst)

            russian_word, target_word = final_lst[0]

            other_words = [option[1] for option in final_lst[1:4]]

            return russian_word, target_word, other_words
        else:
            russian_word, target_word, other_words = get_all_words_if_user_doesnt_exists()
            return russian_word, target_word, other_words
    except Exception as e:
        print(f'Ошибка при проверке слов пользователя: {e}')
    finally:
        session.close()

def save_word_to_db(user_id, russian_word, english_word):
    session = Session()
    try:
        existing_word = session.query(UserWords).filter(
            UserWords.user_id == user_id,
            UserWords.russian_word == russian_word
        ).first()

        if existing_word:
            existing_word.english_word = english_word
            session.commit()
            return "Слово обновлено"
        else:
            new_word = UserWords(user_id=user_id, russian_word=russian_word, english_word=english_word)
            session.add(new_word)
            session.commit()
            return "Слово добавлено"
    except Exception as e:
        session.rollback()
        print("Ошибка при добавлении слова")
    finally:
        session.close()

def delete_the_word_from_the_userwords_table(user_id, telegram_id, word_to_delete):
    session = Session()
    try:
        if user_has_words(telegram_id):
            word = session.query(UserWords).filter(UserWords.user_id == user_id, UserWords.russian_word == word_to_delete).first()
            if word:
                session.delete(word)
                session.commit()
                return True
            else:
                print('Слово не найдено')
                return False
        else:
            print('Ошибка. У вас нет дополнительных слов')
            return False
    except Exception as e:
        print(f'Ошибка при удалении слова: {e}')
        return False
    finally:
        session.close()






session.close()
