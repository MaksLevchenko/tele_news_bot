import datetime
import json
from aiogram.utils.markdown import hbold, hunderline, hlink, hcode
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from config import token
from get_news import difirense_news, get_news

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(messege: types.Message):
    start_button = ["Горячие новости", "Все новости", "Последние 5 новостей"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    await messege.answer("Привет, свежих новостей не хочешь?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(messege: types.Message):
    get_news()
    with open("fresh_news.json", "r", encoding="utf-8") as file:
        new_dict = json.load(file)
    # print(new_dict)
    for k, v in sorted(new_dict.items()):
        # news = f"На <b>{datetime.datetime.now().strftime('%Y-%m-%d')} {v['date']}</b>\n" \
        #        f"<u>{v['news']}</u>\n" \
        #        f"{v['news_link']}"
        news = f"На {hbold(datetime.datetime.now().strftime('%Y-%m-%d'))} {hbold(v['date'])}\n" \
               f"{hlink(v['news'], v['news_link'])}"
        # print(news)
        await messege.answer(news)


@dp.message_handler(Text(equals="Последние 5 новостей"))
async def get_last_five_news(messege: types.Message):
    with open("fresh_news.json", "r", encoding="utf-8") as file:
        new_dict = json.load(file)
    for k, v in sorted(new_dict.items())[-5:]:
        news = f"На {hbold(datetime.datetime.now().strftime('%Y-%m-%d'))} {hbold(v['date'])}\n" \
               f"{hlink(v['news'], v['news_link'])}"

        await messege.answer(news)


@dp.message_handler(Text(equals="Горячие новости"))
async def get_fresh_news(messege: types.Message):
    fresh_news = difirense_news()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"На {hbold(datetime.datetime.now().strftime('%Y-%m-%d'))} {hbold(v['date'])}\n" \
                   f"{hlink(v['news'], v['news_link'])}"

            await messege.answer(news)
    else:
        await messege.answer("Пока нет свежих новостей...")


@dp.message_handler()
def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
