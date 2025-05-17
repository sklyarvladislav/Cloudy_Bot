# Telegram Бот погоды Cloudy 

Бот на aiogram, который выводит погоду исходя из введенного города, присылает погоду по установленному времени

## Зависимости
* aiogram 3.19.0
* aiosqlite 0.20.0
* uv 
* python 3.12
* SQLite 
* OpenWeatherMap API
* APScheduler


## Перед запуском запустите команду
```bash
cp example.env .envrc 
```

## Возможности:
* Команды /start, /time
* Вывод погоды по введенному городу
* Автоопредление города и вывод погоды по геолокации
* Установка уведомлений
* Возможность установить до 3 параметров времен, когда будут приходить уведомления 

## Установка через докер 

# Бот запускается при команде 
```bash 
make run
```

# Установка через GitHub

```bash
git clone https://github.com/CJArthur/Cloudy_Bot.git
cd Cloudy_Bot
```

# Быстрый запуск с помощью Docker
1. Установите Docker(https://www.docker.com/)
2. Создайте файл .env на основе example.env и добавте туда свои ключи
3. Запустите контейнер: docker run -d --env-file .env kab0chinator0385/cloudy_bot:latest