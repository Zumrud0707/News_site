from bs4 import BeautifulSoup
import requests
import re
import time
from datetime import datetime
import pytz

# URL страницы новостного сайта РИА Новости
url = "https://ria.ru/lenta/"

# Получаем текущее время с учетом часового пояса
current_time = datetime.now(tz=pytz.timezone('Europe/Moscow'))

# Форматируем время без смещения от UTC
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

# Выводим время на экран
print(formatted_time)

#Создаем множество для хранения уже обработанных ссылок для исключения дубликатов
unique_links = []
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
print('*******')

#Устанавливаем скрипт с интервалом 5 минут продолжительностью 4 часа
start_time = time.time()
duration = 14400  # продолжительность 4 часа
interval = 300  # интервал 5 минут

#Проверяем статьи на упоминание ключевых слов
def check_article(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    all_title = soup.find('div', class_=re.compile(r'article__title'))
    all_summary = soup.find('h1', class_=re.compile(r'article__second-title'))
    all_author = soup.find('a', class_=re.compile(r'color-font-hover-only'))
    all_time = soup.find('a', string=re.compile(r'\d{2}:\d{2} \d{2}.\d{2}.\d{4}'))
    title = all_title.text.strip() if all_title else 'Не найден'
    summary = all_summary.text.strip() if all_summary else 'Не найдена'
    author = all_author.text.strip() if all_author else 'Не найден'
    time = all_time.text.strip() if all_time else 'Не найдено'

    all_content = soup.find_all('div', class_=re.compile(r'article__text'))
    content = ' '.join([div.text for div in all_content])

    keywords = [  r'Путин\w+', r'Байден\w+' ]      

    if any(re.search(keyword, content, re.IGNORECASE) for keyword in keywords):
        print(f"Заголовок статьи: {title}")
        print(f"Аннотация: {summary}")
        print(f"Автор: {author}")
        print(f"Время выхода статьи: {time}")
        #print(content)
        print('*******')

# Функция для вывода черты после каждого цикла поиска
def print_divider():
    print("-" * 80)

while time.time() - start_time < duration:
    html = get_html(url)
    # Обновляем список ссылок на статьи внутри цикла while
    links = parse_links(html)
    for link in links:
        check_article(link)
        # Выводим черту после каждого цикла поиска
    print_divider()

    time.sleep(interval)
    if time.time() - start_time >= duration:
        print("Период в 4 часа истек.")
        break  # Прерываем цикл, если период истек
