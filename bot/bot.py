# -*- coding: utf-8 -*-
import telebot
import config
from telebot import types
from covid_parser import *
from newsapi import NewsApiClient

bot = telebot.TeleBot(config.token)

totalCasesKeyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
totalCasesBtn1 = types.KeyboardButton(text="ℹ️Общая информация")
totalCasesBtn2 = types.KeyboardButton(text="🇨🇳Информация по странам")
totalCasesBtn3 = types.KeyboardButton(text="📰Новости коронавируса")
totalCasesKeyboard.add(totalCasesBtn1, totalCasesBtn2, totalCasesBtn3)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Вас приветствует бот с актуальной информацией о covid 19", reply_markup=totalCasesKeyboard)


@bot.message_handler(content_types=["text"])
def text(message):
    if message.text == "Меню":
        bot.send_message(message.chat.id, "Выберите ", reply_markup=totalCasesKeyboard)
        bot.register_next_step_handler(message, text)
    elif message.text == "ℹ️Общая информация":
        cases = getCases()
        deaths = getDeaths()
        recovered = getRecovered()
        mes = f"<b>Актуальная информация по всему миру</b> \n🤧Зараженных : <i>{ cases }</i> \n☠️Смертей : <i>{ deaths }</i>\n😀Выздоровивших : <i>{ recovered }</i>"
        bot.send_message(message.chat.id, text=mes, parse_mode = "HTML")
    elif message.text == "📰Новости коронавируса":
        getNews(message, 1)
    elif message.text == "🇨🇳Информация по странам":
        source = requests.get("https://www.worldometers.info/coronavirus/").text
        soup = BeautifulSoup(source, "lxml")
        cases = soup.find_all("div", class_="maincounter-number")
        table = soup.find("table", id="main_table_countries_today").tbody
        trs = table.find_all("tr")
        countries = []
        CountryChooseKeyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        CountryChooseButton = types.KeyboardButton(text="◀️Назад")
        CountryChooseKeyboard.add(CountryChooseButton)
        j = 8
        while j < 218:
            country = trs[j]
            tds = country.find_all("td")
            country_name = tds[0].string
            CountryChooseButton1 = types.KeyboardButton(text=str(country_name))
            countries.append(str(country_name))

            country = trs[j+1]
            tds = country.find_all("td")
            country_name = tds[0].string
            CountryChooseButton2 = types.KeyboardButton(text=str(country_name))
            countries.append(str(country_name))

            country = trs[j+2]
            tds = country.find_all("td")
            country_name = tds[0].string
            CountryChooseButton3 = types.KeyboardButton(text=str(country_name))
            countries.append(str(country_name))

            CountryChooseKeyboard.add(CountryChooseButton1, CountryChooseButton2, CountryChooseButton3)

            j += 3
            

        bot.send_message(message.chat.id, "Выберите страну", reply_markup=CountryChooseKeyboard)
        bot.register_next_step_handler(message, getInfoByCountry,CountryChooseKeyboard, countries)

def getInfoByCountry(message, keyboard, countries):
    if message.text == "◀️Назад":
        message.text = "Меню"
        text(message)
    elif message.text not in countries:
        bot.send_message(message.chat.id, "Выберите корректное название страны из панели с низу")
        message.text = "🇨🇳Информация по странам"
        text(message)
    else:
        source = requests.get("https://www.worldometers.info/coronavirus/").text
        soup = BeautifulSoup(source, "lxml")
        cases = soup.find_all("div", class_="maincounter-number")
        table = soup.find("table", id="main_table_countries_today").tbody
        trs = table.find_all("tr")
        j = 8
        while j < 218:
            country = trs[j]
            tds = country.find_all("td")
            country_name = tds[0].string
            if country_name == message.text:
                total_cases = tds[1].string
                new_cases = tds[2].string
                total_deaths = tds[3].string
                new_deaths = tds[4].string
                total_recovered = tds[5].string
                active_cases = tds[6].string
                critical = tds[7].string
                cases1m = tds[8].string
                deaths1m = tds[9].string
                total_tests = tds[10].string
                tests1m = tds[11].string
                mes = f"<b>Информация страны {country_name}</b> \nЗараженных: <i>{total_cases}</i> \nЗараженных за день: <i>{new_cases}</i> \nСмертей: <i>{total_deaths}</i> \nСмертей за день: <i>{new_deaths}</i> \nВыздоровивших: <i>{total_recovered}</i> \nАктивные случаи: <i>{active_cases}</i> \nКритичные: <i>{critical}</i> \nЗараженных на 1 млн: <i>{cases1m}</i> \nСмертей на 1 млн: <i>{deaths1m}</i> \nВсего тестов: <i>{total_tests}</i> \nТестов на 1 млн: <i>{tests1m}</i>"
                bot.send_message(message.chat.id, mes, parse_mode="HTML", reply_markup=keyboard)
                bot.register_next_step_handler(message, getInfoByCountry, keyboard, countries)
                break
            else:
                j += 1

def getNews(message, page):
    news = NewsApiClient(api_key='990b728f8ea245bfbc63329adfd21522')
    top_headlines = news.get_top_headlines(q='коронавирус', language='ru', page_size=1, page=page)
    
    for i in top_headlines["articles"]:
        title = i["title"]
        desc = i["description"]
        url = i["url"]
        urlToImage = i['urlToImage']
        publishedAt = i["publishedAt"][0:10]

        mes = f"<b>{title}</b> \n{desc} \n{urlToImage} \nИсточнк: {url} \nДата публикации: {publishedAt}"
        getNewsKeyboard = types.InlineKeyboardMarkup()
        getNewsKeyButton1 = types.InlineKeyboardButton(text="Пред", callback_data=f"n{page-1}")
        getNewsKeyButton2 = types.InlineKeyboardButton(text="Отмена", callback_data=f"Отмена")
        getNewsKeyButton3 = types.InlineKeyboardButton(text="След", callback_data=f"n{page+1}")

        if page > 1:
            getNewsKeyboard.add(getNewsKeyButton1, getNewsKeyButton2, getNewsKeyButton3)
        elif page == 1:
            getNewsKeyboard.add(getNewsKeyButton2, getNewsKeyButton3)
        
        if page > 1:
            bot.edit_message_text(chat_id = message.chat.id, message_id = message.message_id,text= mes, parse_mode="HTML", reply_markup=getNewsKeyboard)
        elif page == 1:
            bot.send_message(message.chat.id, mes, parse_mode="HTML", reply_markup=getNewsKeyboard)
        
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data[0:1] == "n":
        getNews(message = call.message, page = int(call.data[1::]))
    elif call.data == "Отмена":
        call.message.text = "Меню"
        m = call.message
        bot.delete_message(call.message.chat.id, call.message.message_id)
        text(m)
if __name__ == '__main__':
    bot.polling(none_stop=True)