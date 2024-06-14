from bs4 import BeautifulSoup
import requests
import re
import time
from datetime import datetime
import pytz

# URL страницы новостного сайта РИА Новости
url = "https://ria.ru/lenta/"

# Получаем текущее время
current_time = datetime.now(tz=pytz.timezone('Europe/Moscow'))

# Форматируем время без смещения от UTC
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

# Выводим время
print(formatted_time)

#Создаем множество для хранения уже обработанных ссылок
unique_links = ['link1', 'link2', 'link3']
processed_links = set()

# Функция для парсинга ссылок на статьи
def parse_links(html):
    global processed_links
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True, class_=re.compile(r'list-item__image')):
        href = a['href']
        if href not in processed_links:
            links.append(href)
            processed_links.add(href)
    return links

# Функция для получения HTML страницы
def get_html(url):
    response = requests.get(url)
    return response.text

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
s = soup.find('title').text

# Выводим заголовок страницы на экран
print(s, ':')
print('*****')

#Устанавливаем скрипт с интервалом 10 минут продолжительностью 4 часа
start_time = time.time()
duration = 14400  # продолжительность 4 часа
interval = 300  # интервал 5 минут

#Функция для проверки статьи на упоминание
def check_article(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    title_tag = soup.find('div', class_=re.compile(r'article__title'))
    summary_tag = soup.find('h1', class_=re.compile(r'article__second-title'))
    author_tag = soup.find('a', class_=re.compile(r'color-font-hover-only'))
    time_tag = soup.find('a', string=re.compile(r'\d{2}:\d{2} \d{2}.\d{2}.\d{4}'))

    title = title_tag.text.strip() if title_tag else 'Не найден'
    summary = summary_tag.text.strip() if summary_tag else 'Не найдена'
    author = author_tag.text.strip() if author_tag else 'Не найден'
    time = time_tag.text.strip() if time_tag else 'Не найдено'

    content_tags = soup.find_all('div', class_=re.compile(r'article__text'))
    content = ' '.join([div.text for div in content_tags])

    keywords = [  r'Байден\w+', r'Трамп\w+' ]      

    if any(re.search(keyword, content, re.IGNORECASE) for keyword in keywords):
        print(f"Заголовок статьи: {title}")
        print(f"Аннотация: {summary}")
        print(f"Автор: {author}")
        print(f"Время выхода статьи: {time}")
        #print(content)
        print('*****')

def print_divider():
    print("-" * 80)
   
while time.time() - start_time < duration:
    html = get_html(url)
    # Обновляем список ссылок на статьи внутри цикла while
    links = parse_links(html)
    for link in links:
        check_article(link)
        # Функция для вывода черты после каждого цикла поиска
    print_divider()
        
    time.sleep(interval)
    if time.time() - start_time >= duration:
        print("Период в 4 часа истек.")
        break  # Прерываем цикл, если период истек
