import sqlalchemy
from sqlalchemy.orm import sessionmaker

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

    users_exists = session.query(Users).filter(Users.telegram_id == personal_id).first()

    if users_exists:
        pass
    else:
        user = Users(telegram_id=personal_id)
        session.add(user)
        session.commit()



users = session.query(Users).all()
for user in users:
    print(user)

session.close()
