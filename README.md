<h1><strong>English Vocabulary Telegram Bot</strong></h1>
<p>Телеграм-бот для изучения английских слов с возможностью добавления и удаления слов пользователем.</p>

Возможности

<ul>
<li>Изучение английских слов через карточки</li>
<li>Выбор правильного перевода из вариантов</li>
<li>Удаление ранее добавленных слов</li>
<li>Хранение данных пользователей и слов в PostgreSQ</li>
</ul>


Установка и запуск
<ol>
<li>Клонируйте репозиторий</li>
<li>Установите зависимости</li>
<li>Настройте подключение к базе данных PostgreSQL в файле database.py</li>
<li>Запустите бота</li>
</ol>

Настройка базы данных
<ul>
<li>Создайте базу данных PostgreSQL</li>
<li>Убедитесь, что пользователь и пароль соответствуют настройкам в DSN</li>
<li>При первом запуске таблицы создадутся автоматически</li>
</ul>

Требования

<ul>
<li>Python 3.8 или выше</li>
<li>PostgreSQL</li>
<li>Telegram Bot Token</li>
</ul>

Использование

<ul>
<li>Отправьте команду /start или /cards в Телеграме, чтобы начать обучение</li>
<li>Выбирайте правильный перевод слова</li>
<li>Используйте кнопки "Добавить слово" и "Удалить слово" для управления словарём</li>
<li>Нажимайте "Дальше" для перехода к следующему слову</li>
</ul>


<h2>Автор</h2>
MaksPinch
Maksim Pinchuk