import datetime
import requests
from config import weather_token, bot_tg_token
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=bot_tg_token)
BotW = Dispatcher(bot)

@BotW.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Я бот созданный для показа информации о погоде\nНапиши мне город который интересует 😊')

@BotW.message_handler()
async def weather_info(message: types.Message):
    smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        i = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric'
        )
        data = i.json()


        weather_description = data['weather'][0]['main']
        if weather_description in smile:
            wd = smile[weather_description]
        else:
            wd = 'Неизвестная погода'

        city = data['name']
        temp_weather = data['main']['temp']
        humidity = data['main']['humidity']
        wind_weather = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        len_time = datetime.datetime.fromtimestamp(
            data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])

        await message.reply(f"---{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}---\n"

        f"Погода в городе: {city}\nТемпература: {temp_weather}C° {wd}\n"
        f"Влажность: {humidity}%Ветер: {wind_weather} м/с\n"
        f"Восход солнца: {sunrise}\nЗакат солнца: {sunset}\nПродолжительность дня: {len_time}\n"
        f"---Хорошего дня!---"
        )

    except:
        await message.reply('Я не заню такого города 😢')


if __name__ == '__main__':
    executor.start_polling(BotW)
