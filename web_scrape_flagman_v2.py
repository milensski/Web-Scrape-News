import time

import requests
from bs4 import BeautifulSoup
from winotify import Notification, audio


def get_news():
    url = 'https://www.flagman.bg/%D0%BF%D0%BE%D1%81%D0%BB%D0%B5%D0%B4%D0%BD%D0%BE-%D0%B2-%D0%B1%D0%B5%D1%81%D0%BE%D0%B2%D0%B5'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_news = soup.find_all("span", class_="boxNewsDescription")
    return page_news


def all_news():
    news_container = {'title': []}
    count = 0
    for element in get_news():
        count += 1
        description = None
        title = element.find('span', class_='boxNewsHeading').text.strip()
        if element.p:
            description = element.p.text
        link_to_article = 'flagman.bg' + element.find('a')['href']
        if title not in news_container['title']:
            news_container['title'].append(title)

        print('!----------!')
        print()
        print(title)

        if description:
            print(description)
        print(link_to_article)

        notify_article(title, description, link_to_article)

    return news_container


def notify_article(note_title: str, note_description: str, link_to_article: str):
    toast = Notification(app_id="News Update",
                         title=note_title,
                         msg=f"{note_description}\n",
                         duration="long",

                         )

    toast.set_audio(audio.Default, loop=False)
    toast.add_actions(label='Check article', launch=link_to_article)
    toast.show()


news_container = all_news()

while True:
    print('Job Start')
    time.sleep(60)
    page_news = get_news()
    for news in page_news:
        title = news.find('span', class_='boxNewsHeading').text.strip()
        if news.p:
            description = news.p.text
        else:
            description = None
        link_to_article = 'https://flagman.bg' + news.find('a')['href']
        if title not in news_container['title']:
            print(title)
            if description:
                print(description)
            print(link_to_article)

            news_container['title'].append(title)
            notify_article(title, description, link_to_article)

    print("Job End")
