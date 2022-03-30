import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E5%8F%91%E7%8E%B0'

file = open('weibo_new_发现.csv', mode='a', encoding='utf-8')

print('Starting Browser...')

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome = webdriver.Chrome(options=chrome_options)

score_times = 0
maxTime = 600

chrome.maximize_window()
chrome.get(url)
time.sleep(3)

# 热门
# chrome.find_element(
#     By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div/ul/li[8]/span').click()

# 实时
chrome.find_element(
    By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div/ul/li[3]/span').click()


while score_times < maxTime:

    chrome.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(1)
    score_times += 1

time.sleep(1)

html_text = chrome.page_source

page = BeautifulSoup(html_text,'html.parser')
[s.extract() for s in page('a')]

contents = page.select('div[class="weibo-text"]')

print("Row data size:",len(contents))

counter = 0
texts = []

for counter in range(len(contents)):

    comment = contents[counter]
    text = comment.text
    text = text.encode('utf-8').decode()
    texts.append(text)


cleaned_texts = list(set(texts))
print('Cleaned data size:',len(cleaned_texts))

for text in cleaned_texts:
    file.write(text)
    file.write(',')
    counter+=1

file.close()
