import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

service = Service()
options = webdriver.ChromeOptions()

cryptoCurrency = []

with webdriver.Chrome(service=service, options=options) as driver:
    wait = WebDriverWait(driver, 10)
    for page in range(1, 11):
        driver.get(f'https://coinmarketcap.com/?page={page}')
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        pageContent = driver.page_source
        currentUrl = driver.current_url

        site = BeautifulSoup(pageContent, 'html.parser')
        trs = site.find('tbody').find_all('tr')

        cryptoCurrency += [
            {
                'name': ps[0].get_text() if (ps := third_td.find_all('p')) else spans[1].get_text(),
                'symbol': ps[1].get_text() if ps else spans[2].get_text(),
                'rank': index + 1,
                'price': (fourth_td := tds[3]).get_text(),
                'url': currentUrl,
            }
            for index, tr in enumerate(trs) if len((tds := tr.find_all('td'))) > 2
            for third_td in [tds[2]]
            for spans in [third_td.find_all('span')]
        ]

with open('cryptoCurrency.json', 'w') as file:
    json.dump(cryptoCurrency, file, indent=4)
