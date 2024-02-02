from bs4 import BeautifulSoup
import requests
import io
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

bot_token = '6717237649:AAHofPLIUAdhaSsrdSgaHA44eIzLWpxLuH8'
chat_id = '907940199'

response = requests.get('https://www.ethiopianreporter.com/')
soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all('div', class_='vc_column_inner tdi_140 wpb_column vc_column_container tdc-inner-column td-pb-span4')
titles = soup.find_all('h3', class_='entry-title td-module-title')
images = soup.find_all('div', class_='td-image-container')

def send_to_telegram(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, params=params)
    return response.json()

for index, article in enumerate(articles):
    title = titles[index].get_text(strip=True)
    
    # Extract the link for each article
    link = article.find('a', href=True)['href']

    # Extract image URL if it exists
    image_element = images[index].find('img')
    if image_element:
        image_url = image_element.get('src')
    else:
        image_url = "No image available"

    texts = f"Title: {title}\nLink: {link}\nImage: {image_url}\n"
    response = send_to_telegram(bot_token, chat_id, texts)
    print(response)
    time.sleep(30)

