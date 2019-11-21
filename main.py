import telebot
import requests
from random import randrange
from datetime import timedelta, datetime

TOKEN = "1002176547:AAEnJt0ZVYhoTARB-5wDCT38OC0hhhMWfmk"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to my test bot. To use it simply type any number.")


@bot.message_handler(commands=['randompicoftheday'])
def handle_nasa_pic(message):
    def random_date(start, end):
        """
        This function will return a random datetime between two datetime
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    d1 = datetime.strptime('6/16/1995', '%m/%d/%Y')
    d2 = datetime.strptime('11/20/2019 4:50 AM', '%m/%d/%Y %I:%M %p')

    while (True):
        date = random_date(d1, d2)

        api_key = 'kVk83GPVbuiFjHvZl57eZXtucbF9n6k3vE2djtWh'
        args = {
            "api_key": api_key,
            "date": str(date.year) + "-" + str(date.month) + "-" + str(date.day)
        }
        response = requests.get("https://api.nasa.gov/planetary/apod", args)
        if len(response.json()['explanation']) < 200: break

    bot.send_photo(message.json['chat']['id'], response.json()['url'], caption=response.json()['explanation'],
                   reply_to_message_id=message.json['message_id'])


@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
    bot.reply_to(message, "https://i.imgur.com/ckh5qRC.jpg")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    params = {
        "json": "true"
    }
    if message.text.isnumeric():
        r = requests.get("http://numbersapi.com/" + message.text + "/math", params)
        bot.reply_to(message, r.json()['text'])


bot.polling()
