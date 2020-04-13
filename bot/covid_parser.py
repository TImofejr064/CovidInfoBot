from bs4 import BeautifulSoup
import requests

# source = requests.get("https://www.worldometers.info/coronavirus/").text
# soup = BeautifulSoup(source, "lxml")

# cases = soup.find_all("div", class_="maincounter-number")
# num = 1

# print("-------------")
# print(cases[0].span.text)
# print("-------------")

# table = soup.find("table", id="main_table_countries_today").tbody
# trs = table.find_all("tr")
# # print(trs[2].text)
# tds = trs[1].find_all("td")
# print(tds[1].text)

def getCases():
    source = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(source, "lxml")
    cases = soup.find_all("div", class_="maincounter-number")

    return cases[0].span.text

def getRecovered():
    source = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(source, "lxml")
    cases = soup.find_all("div", class_="maincounter-number")

    return cases[2].span.text

def getDeaths():
    source = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(source, "lxml")
    cases = soup.find_all("div", class_="maincounter-number")

    return cases[1].span.text
