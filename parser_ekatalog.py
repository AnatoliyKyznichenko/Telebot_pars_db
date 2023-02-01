from aiogram import types, executor, Dispatcher, Bot
from bs4 import BeautifulSoup
import requests
from key import my_key

bot = Bot(my_key)
dp = Dispatcher(bot)

#command start
@dp.message_handler(commands=['start'])
async def start(message: types.message):
    await bot.send_message(message.chat.id, """Hi! I'm bot that helps you find products quickly 
    <b><a href="https://ek.ua/ua/">E Katalog</a></b>
    я отправлю тебе товар, введи в поле его название...""",
    parse_mode="html", disable_web_page_preview=0)


@dp.message_handler(content_types=['text'])
async def parser(message: types.message):
    url = f'https://ek.ua/ek-list.php?search_=' + message.text
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    all_links = soup.find_all("a", class_="model-short-title no-u")
    for item in all_links:
        url = f'https://ek.ua/ua/' + item['href'][4:]
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')

        name = soup.find('div', class_='fix-menu-name')
        price = name.find('a').text
        name.find('a').extract()  # метод extract() вырезает элимент из библиотекиname = name.text
        name = name.text
        img = soup.find('div', class_='img200')
        img = img.findChildren('img')[0]  # Достаем дочерний элимент Потомки#
        #img = 'https://ek.ua/ua/' + img["src"]#img = img["src"]
        img = img["src"]

        '''Отправка спарсенных данных в роли бота        
        message.chat.id = Куда отправлять       
        img = Что отправлять, то есть ссылка       
        price = Выделенна курсивом'''

        
        await bot.send_photo(message.chat.id, img,
        caption="<b>" + name + "</b>\n<i>" + price + f"</i>\n<a href='{url}'>Ссылка на сайт</a>",
        parse_mode='html')

        # if all_links.index(item) == 9:
        #     break

executor.start_polling(dp)