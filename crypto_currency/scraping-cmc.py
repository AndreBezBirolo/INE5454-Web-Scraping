from bs4 import BeautifulSoup
from selenium import webdriver;
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time;
import json;

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

currentUrl = ''
driver.get('https://coinmarketcap.com/')
time.sleep(5)
pageContent = driver.page_source
currentUrl = driver.current_url
driver.quit()

cryptoCurrency = []

site = BeautifulSoup(pageContent, 'html.parser')
trs = site.find('tbody').find_all('tr')

for index, tr in enumerate(trs):
  tds = tr.find_all('td')
  if len(tds) > 2:
    third_td = tds[2]
    fourth_td = tds[3]
    ps = third_td.find_all('p')
    spans = third_td.find_all('span')
    if ps:
      cryptoCurrency.append({
        'name': ps[0].get_text(),
        'symbol': ps[1].get_text(),
        'rank': index + 1,
        'price': fourth_td.get_text(),
        'url': currentUrl,
      })
    elif spans:
      cryptoCurrency.append({
        'name': spans[1].get_text(),
        'symbol': spans[2].get_text(),
        'rank': index + 1,
        'price': fourth_td.get_text(),
        'url': currentUrl,
      })

with open('cryptoCurrency.json', 'w') as file:
  file.write(str(json.dumps(cryptoCurrency, indent=4)))
