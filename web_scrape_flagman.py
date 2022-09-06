from bs4 import BeautifulSoup
import requests



url = 'https://www.flagman.bg/%D0%BF%D0%BE%D1%81%D0%BB%D0%B5%D0%B4%D0%BD%D0%BE-%D0%B2-%D0%B1%D0%B5%D1%81%D0%BE%D0%B2%D0%B5'

page = requests.get(url)


soup = BeautifulSoup(page.content, 'html.parser')

page_title = soup.title.string

page_news = soup.find_all("span", class_="boxNewsDescription")

for element in page_news:
    title = element.find('span', class_='boxNewsHeading').text.strip()

    description = element.p.text

    link_to_article = 'flagman.bg'+element.find('a')['href']
    print('!----------!')
    print(title)
    print(description)
    print(link_to_article)

    print('****************************')
    print()
