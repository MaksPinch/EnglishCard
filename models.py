import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class CommonWords(Base):

    __tablename__ = 'common_words'

    id = sq.Column(sq.Integer, primary_key=True)
    russian_word = sq.Column(sq.String(length=50), unique=True)
    english_word = sq.Column(sq.String(length=50), unique=True)

    def __str__(self):

        return f'{self.id}: {self.russian_word} - {self.english_word}'


class UserWords(Base):

    __tablename__ = 'user_words'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'), nullable=False)
    russian_word = sq.Column(sq.String(length=50))
    english_word = sq.Column(sq.String(length=50))

    user = relationship('Users', back_populates='words')





class Users(Base):

    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True)
    telegram_id = sq.Column(sq.Integer, unique=True)

    words = relationship('UserWords', back_populates='user')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



