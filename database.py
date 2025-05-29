import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, CommonWords, UserWords, Users

DSN = 'postgresql://postgres:130006@localhost:5432/EnglishWord'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

word_1 = CommonWords(russian_word='Я', english_word='I')
word_2 = CommonWords(russian_word='Ты', english_word='You')
word_3 = CommonWords(russian_word='Он', english_word='He')
word_4 = CommonWords(russian_word='Она', english_word='She')
word_5 = CommonWords(russian_word='Мы', english_word='We')
word_6 = CommonWords(russian_word='Красный', english_word='Red')
word_7 = CommonWords(russian_word='Синий', english_word='Blue')
word_8 = CommonWords(russian_word='Зелёный', english_word='Green')
word_9 = CommonWords(russian_word='Чёрный', english_word='Black')
word_10 = CommonWords(russian_word='Белый', english_word='White')

session.add_all([word_1, word_2, word_3, word_4, word_5, word_6, word_7, word_8, word_9, word_10])
session.commit()

def create_user(telegram_id):


session.close()
