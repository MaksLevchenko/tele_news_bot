import requests
from bs4 import BeautifulSoup
import json


def get_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
    }
    url = r"https://lenta.ru/"
    r = requests.get(url=url, headers=headers)
    news_dict = {}
    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(r.text)

    with open("index.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        big_new = soup.find_all('a', {"class": "card-mini"})
        for news in big_new[:10]:
            date = news.text[-5:]
            news_w = news.text[:-5]
            news_link = "https://lenta.ru/" + news.get("href")
            title_news = news.get('href').split('/')[-2]
            news_dict[title_news] = {
                "date": date,
                "news": news_w,
                "news_link": news_link
            }
    with open("fresh_news.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def difirense_news():
    with open("fresh_news.json", "r", encoding="utf-8") as file:
        news_dict = json.load(file)
    # print(news_list)
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
    }
    url = r"https://lenta.ru/"
    r = requests.get(url=url, headers=headers)
    fresh_news = {}
    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(r.text)

    with open("index.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        big_new = soup.find_all('a', {"class": "card-mini"})
        for news in big_new[:10]:
            title_news = news.get('href').split('/')[-2]
            if title_news in news_dict:
                continue
            else:
                date = news.text[-5:]
                news_w = news.text[:-5]
                news_link = "https://lenta.ru/" + news.get("href")
                title_news = news.get('href').split('/')[-2]

                news_dict[title_news] = {
                    "date": date,
                    "news": news_w,
                    "news_link": news_link
                }

                fresh_news[title_news] = {
                    "date": date,
                    "news": news_w,
                    "news_link": news_link
                }

    with open("fresh_news.json", "w", encoding="utf-8") as file:
        json.dump(fresh_news, file, indent=4, ensure_ascii=False)
    return fresh_news


def main():
    get_news()


if __name__ == "__main__":
    main()
