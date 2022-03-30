from distutils.log import error
import imp
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://www.douban.com/group/596379/discussion?start=0&type=new'

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome = webdriver.Chrome(options=chrome_options)


def openbrower():
    chrome.maximize_window()
    chrome.get(url)


def crawling():

    counter = 0
    cc = 0
    file = open('douban_youxi.csv', mode='a', encoding='utf-8')

    while counter < 30:
        try:
            if counter < 29:
                
                print('Now get:')
                print(cc)

                lst = chrome.find_element(By.CLASS_NAME, 'olt').find_elements(
                    By.CLASS_NAME, 'title')

                time.sleep(1.5)

                lst[counter].find_element(By.TAG_NAME, 'a').click()

                host_content = chrome.find_element(
                    By.XPATH, '//*[@id="link-report"]/div/div').text

                host_content = host_content.encode('utf-8').decode()
                file.write(host_content)
                file.write(',')

                comments = chrome.find_element(
                    By.CLASS_NAME, 'topic-reply').find_elements(By.TAG_NAME, 'p')

                for comment in comments:
                    con = comment.text
                    con = con.encode('utf-8').decode()

                    file.write(con)
                    file.write(',')
                    file.write('\n')

                counter += 1
                cc += 1
                chrome.back()

                if cc == 9999:
                    file.close()
                    break

            elif counter == 29:
                file.flush()
                time.sleep(1.5)
                chrome.find_element(
                    By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/span[4]/a').click()
                counter = 5

        except WebDriverException:
            pass
        continue

        
        


if __name__ == '__main__':
    print('Start Browser')
    openbrower()
    crawling()
