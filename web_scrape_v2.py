import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from winotify import Notification, audio


def get_news_flagman():
    url = 'https://www.flagman.bg/%D0%BF%D0%BE%D1%81%D0%BB%D0%B5%D0%B4%D0%BD%D0%BE-%D0%B2-%D0%B1%D0%B5%D1%81%D0%BE%D0%B2%D0%B5'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_news = soup.find_all("span", class_="boxNewsDescription")
    return page_news


def get_news_nova():
    url = 'https://nova.bg/news'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_news_nova = soup.find_all("div", class_="thumb-title")
    page_p_nova = soup.find_all("p", class_="visible-lg visible-md hidden-sm hidden-xs")

    return page_news_nova, page_p_nova


def all_news_flagman():
    news_container = {'title': []}
    count = 0
    for element in get_news_flagman():
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

    return news_container


def all_news_nova():
    news_container_nova = {'title': []}
    url = 'https://nova.bg/news'

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    page_news = soup.find_all("div", class_="thumb-title")

    for thumb_box in page_news:
        print('----------------')
        if thumb_box.h3 != None:

            title = thumb_box.h3.text
            print(title)
            if title not in news_container_nova:
                news_container_nova['title'].append(thumb_box.h3.text)
            print(thumb_box.a['href'])
        else:
            break
        print('---------------------')

    return news_container_nova


def check_news_update_nova():
    new_news = False
    page_news_nova, page_p_nova = get_news_nova()
    for thumb_box, p in zip(page_news_nova, page_p_nova):
        if thumb_box.h3 != None:
            title_nova = thumb_box.h3.text
            description_nova = p.text
            link_nova = thumb_box.a['href']

            if title_nova not in news_container_nova['title']:
                print(title_nova)
                print(description_nova)
                print(link_nova)
                news_container_nova['title'].append(title_nova)
                notify_article(title_nova, description_nova, link_nova)
                new_news = True
    print()
    if new_news == False:
        print("No new update from NOVA")


def check_news_update_flagman():
    new_news = False
    page_news = get_news_flagman()
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
            new_news = True
    print()
    if new_news == False:
        print("No news updates from FLAGMAN")


def progress_bar(value):
    pbar = tqdm(total=value)

    for i in range(1, value + 1):
        time.sleep(1)
        pbar.update(1)
        pbar.set_description("Progress untill next update ")
    pbar.close()
    print()
    return True


def notify_article(note_title: str, note_description: str, link_to_article: str):
    toast = Notification(app_id="News Update",
                         title=note_title,
                         msg=f"{note_description}\n",
                         duration="long",

                         )

    toast.set_audio(audio.Mail, loop=False)
    toast.add_actions(label='Check article', launch=link_to_article)
    toast.show()


news_container = all_news_flagman()
news_container_nova = all_news_nova()

while True:
    print('Job Start')
    print()
    progress_bar(60)
    print()
    check_news_update_flagman()
    check_news_update_nova()
    print("Job End")
