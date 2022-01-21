import csv
import sys
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

import time

output_file = 'blog_data01.csv'

def setUpChrome():
    global driver
    # Using Chrome
    chrome_options = webdriver.ChromeOptions()
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    #chrome_options.add_argument('headless')

    scriptpath = os.path.realpath(__file__)
    foldername = os.path.basename(scriptpath)
    scriptpath = scriptpath[:scriptpath.find(foldername)]

    scriptpath += 'chromedriver'

    driver = webdriver.Chrome(scriptpath, options=chrome_options)
    return driver

def add_csv_head():
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['date', 'title', 'content'])

def add_csv_row(date, title, content):
    with open(output_file, 'a', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [date, title, content])

#pages = input('Enter number of pages to scrape: ')
pages = 2

driver = setUpChrome()
add_csv_head()

driver.get('http://blogs.nature.com/')

article_dates = []
article_titles = []
article_contents = []

try:
    pages = int(pages)
    for i in range(0, pages):
        page_url = driver.current_url
        article_urls = []
        titles = driver.find_elements_by_xpath('//h2[contains(@class, "wpn-post-title")]')
        for title in titles:
            article_url = title.find_element_by_xpath('.//a').get_attribute('href')
            article_urls.append(article_url)
        for url in article_urls:
            driver.get(url)
            article_title = driver.find_element_by_xpath('//h1[contains(@class, "wpn-post-title")]').text
            article_date = driver.find_element_by_xpath('//span[contains(@class, "published")]').text
            article_content_block = driver.find_element_by_xpath('//div[contains(@class, "wpn-entry-content")]')
            article_content_pieces = article_content_block.find_elements_by_xpath('.//p')
            article_content_texts = []
            for piece in article_content_pieces:
                article_content_texts.append(piece.text)
            article_content = '\n'.join(article_content_texts)

            article_dates.append(article_date)
            article_titles.append(article_title)
            article_contents.append(article_content)

            # Wait for n seconds
            time.sleep(2)
            
        driver.get(page_url)
        driver.find_element_by_xpath('//span[contains(text(), "Older entries")]').click()
                
    print(len(article_titles))
    print(len(article_dates))
    print(len(article_contents))

    driver.quit()

    for i in range(0, len(article_dates)):
        add_csv_row(article_dates[i], article_titles[i], article_contents[i])

except:
    print(e)
    print('Please enter a valid number.')
    driver.quit()
