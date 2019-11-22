import time
import telebot
import requests
from random import randrange
from datetime import timedelta, datetime
from urllib.request import urlopen
from PIL import Image
import random
import io
import schedule
import threading

TOKEN = "1002176547:AAEnJt0ZVYhoTARB-5wDCT38OC0hhhMWfmk"

bot = telebot.TeleBot(TOKEN)


def notifications():
    ids = [392596821]  # 443124676,346024384
    schedule.every().monday.at("04:30").do(send_msg, ids, "https://i.imgur.com/rkmDE9P.jpg")
    schedule.every().tuesday.at("04:30").do(send_msg, ids, "https://i.imgur.com/rkmDE9P.jpg")
    schedule.every().wednesday.at("06:30").do(send_msg, ids, "https://i.imgur.com/rkmDE9P.jpg")
    schedule.every().thursday.at("06:30").do(send_msg, ids, "https://i.imgur.com/rkmDE9P.jpg")
    schedule.every().friday.at("04:30").do(send_msg, ids, "https://i.imgur.com/rkmDE9P.jpg")
    schedule.every().saturday.at("10:00").do(send_msg, ids,
                                             "https://kartinki-life.ru/cards/2019/06/23/prosypaysya-sonya-s-dobrym-utrom-puskay-etot-den-budet-luchshe-chem-vchera-zhelau-udachnyh-del-i-horosh.jpg")
    schedule.every().sunday.at("10:00").do(send_msg, ids,
                                           "https://3d-galleru.ru/cards/12/83/1cg3302a2l3qhfxs/vy-uzhe-prosnulis-togda-dobrogo-utrechka.jpg")
    while True:
        schedule.run_pending()
        time.sleep(1)


def send_msg(ids: list, link: str):
    for id in ids:
        bot.send_photo(id, link)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to my test bot. To use it simply type any number.")


@bot.message_handler(commands=['randompicoftheday'])
def handle_nasa_pic(message):
    def random_date(start, end):
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

        if len(response.json()['explanation']) < 1025: break
    bot.send_photo(message.json['chat']['id'], response.json()['url'], caption=response.json()['explanation'],
                   reply_to_message_id=message.json['message_id'])


@bot.message_handler(commands=['meme'])
def random_meme(message):
    r = requests.get("https://meme-api.glitch.me/dank")
    bot.send_photo(message.json['chat']['id'], r.json()['meme'], reply_to_message_id=message.json['message_id'])


@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
    path_to_file = "https://api.telegram.org/bot" + TOKEN + "/getFile?file_id=" + message.json['photo'][0]["file_id"]
    file = "https://api.telegram.org/file/bot" + TOKEN + "/" + requests.get(path_to_file).json()['result']['file_path']
    img = Image.open(urlopen(file))
    width, height = img.size
    BLOCKLENX = 1
    BLOCKLENY = 1
    xblock = width / BLOCKLENX
    yblock = height / BLOCKLENY
    blockmap = [(xb * BLOCKLENX, yb * BLOCKLENY, (xb + 1) * BLOCKLENX, (yb + 1) * BLOCKLENY)
                for xb in range(int(xblock)) for yb in range(int(yblock))]

    shuffle = list(blockmap)
    random.shuffle(shuffle)

    result = Image.new(img.mode, (width, height))
    for box, sbox in zip(blockmap, shuffle):
        c = img.crop(sbox)
        result.paste(c, box)
    imgByteArr = io.BytesIO()
    result.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    bot.send_photo(message.json['chat']['id'], imgByteArr, reply_to_message_id=message.json['message_id'])


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    params = {
        "json": "true"
    }
    if message.text.isnumeric():
        r = requests.get("http://numbersapi.com/" + message.text + "/math", params)
        bot.reply_to(message, r.json()['text'])


def run_bot():
    bot.polling()


if __name__ == '__main__':
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=notifications)
    t1.start()
    t2.start()
