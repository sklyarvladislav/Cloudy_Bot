#--- Telegram Бот погоды Cloudy ---#

Бот на aiogram, который выводит погоду исходя из введенного города, присылает погоду по установленному времени

# Технологии
~ Python 3.11+
~ aiogram 3
~ APScheduler
~ SQLite
~ OpenWeatherMap API

# Возможности:
~ Команды /start, /time
~ Вывод погоды по введенному городу
~ Автоопредление города и вывод погоды по геолокации
~ Установка уведомлений
~ Возможность установить до 3 параметров времен, когда будут приходить уведомления

# Установка через GitHub

git clone https://github.com/CJArthur/Cloudy_Bot.git
cd Cloudy_Bot
pip install -r requirements.txt

# Быстрый запуск с помощью Docker
1. Установите Docker(https://www.docker.com/)
2. Создайте файл .env на основе example.env и добавте туда свои ключи
3. Запустите контейнер: docker run -d --env-file .env kab0chinator0385/cloudy_bot:latest