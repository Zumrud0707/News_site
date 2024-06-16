Задание для студентов МИИГАиК - Вариант 1 (2024г).
Используя скриптовый язык Python написать скрипт, извлекающий новости (отдельно заголовок, аннотацию, авторов, время выпуска статьи) из веб-страницы новостного агентства, но не используя RSS. Требуется написать такой скрипт, который будучи запущен на 4 часа, автоматически выделит и отобразит/запишет в лог все статьи, которые будут опубликованы за этот период (т.е. только новые), при этом выводить нужно новости содержащие упоминания о президентах России и США  - Путине и Байдене.
Работа сдается в виде:
1) одиночного файла скрипта, готового для запуска
2) указание на зависимые библиотеки (если есть)
3) лог работы скрипта на протяжении 4 часов с выводом всех найденных новостей 
Библиотеки:
from bs4 import BeautifulSoup,
import requests,
import re,
import time,
from datetime import datetime,
import pytz.
При первом цикле парсинга код выводит все найденные на текущий момент статьи с упоминанием ключевых слов. В дальнейшем в течение 4-х часов с интервалом 5 минут происходит поиск и выводятся на печать сведения о заголовке, аннотации, авторе и времени выхода вновь найденных новых статей.
![image](https://github.com/Zumrud0707/News_site/assets/170760445/f0892b62-27ba-4e38-8d79-626332471777)

