import requests
from bs4 import BeautifulSoup
import PyPDF2
import re
import json

url = 'https://ru.ufsc.br/ru/'
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.content, 'html.parser')
article = soup.find('article')
ul = article.find('ul')
li = ul.find('li')
link = li.find('a')['href']
pdf_response = requests.get(link, verify=False)
with open('../ignore/ru_menu.pdf', 'wb') as pdf_file:
    pdf_file.write(pdf_response.content)

with open('../ignore/ru_menu.pdf', 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    pdf_text = ''.join(page.extract_text() for page in pdf_reader.pages[1:3])  # Lê apenas as páginas 2 e 3
    pdf_text = re.sub(r'\s+', ' ', pdf_text)  # Remove espaços extras

days_of_week = ['Segunda -Feira', 'Terça -Feira', 'Quarta -Feira', 'Quinta -Feira', 'Sexta -Feira']
menu = []

for i, dia in enumerate(days_of_week):
    start = pdf_text.find(dia + ':')
    end = pdf_text.find(days_of_week[i + 1] + ':') if i + 1 < len(days_of_week) else len(pdf_text)
    section = pdf_text[start:end].strip()
    data_match = re.search(r'\d{2} ?/\d{2}/\d{4}', section)
    if data_match:
        data = data_match.group().replace(' ', '')
        ingredientes = section[data_match.end():].strip()
        menu.append({
            'day': dia.replace(' -', '-'),
            'date': data,
            'ingredients': ingredientes,
            'link': url
        })

with open('weekly_menu.json', 'w', encoding='utf-8') as json_file:
    json.dump({'menu': menu}, json_file, indent=4, ensure_ascii=False)

print("Menu saved in 'weekly_menu.json'")