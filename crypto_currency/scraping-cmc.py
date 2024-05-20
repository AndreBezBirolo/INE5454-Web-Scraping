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
    rank = 0  # Variável para acompanhar o rank globalmente
    for page in range(1, 11):
        driver.get(f'https://coinmarketcap.com/?page={page}')
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        pageContent = driver.page_source
        currentUrl = driver.current_url

        site = BeautifulSoup(pageContent, 'html.parser')
        trs = site.find('tbody').find_all('tr')

        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) > 2:
                third_td = tds[2]
                fourth_td = tds[3]
                ps = third_td.find_all('p')
                spans = third_td.find_all('span')
                if ps or spans:
                    rank += 1  # Incrementa o rank
                    cryptoCurrency.append({
                        'name': ps[0].get_text() if ps else spans[1].get_text(),
                        'symbol': ps[1].get_text() if ps else spans[2].get_text(),
                        'rank': rank,
                        'price': fourth_td.get_text(),
                        'url': currentUrl,
                    })

with open('cryptoCurrency.json', 'w') as file:
    json.dump(cryptoCurrency, file, indent=4)
