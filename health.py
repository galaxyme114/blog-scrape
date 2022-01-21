# Library IMPORTING
from selenium import webdriver
import time
import csv
from time import gmtime, strftime
import tkinter as tk
from tkinter import *

print("================================DATA SCRAPING... PLEASE WAIT FOR A WHILE=================================")

start_time = time.time()  # start time

# csv file making part
def csv_make():
    try:
        # csv header part defination
        curdate = strftime("%Y-%m-%d %H-%M-%S", gmtime())
        print("Data scraping date and time:", curdate)
        file_name = 'health.csv'
        header = ['article_date', 'article_title', 'article_content', 'article_url']

        # data save into CSV file
        with open(file_name, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(header)  # write the header
        f.close()
    except:
        pass

    return file_name

# main function
def health_download():
    driver = run_Firefox()
    url = variable.get()
    file_name = csv_make()
    driver.get(url)  # requesting
    time.sleep(2)
    article_blog_data = [[]]
    article_blog_data.clear()
    while True:
        try:
            page_url = driver.current_url
            health_data = driver.find_element_by_xpath(".//div[@class='hfeed post-list']")
            article = health_data.find_elements_by_xpath(".//div[@class='post-wrapper']")
        except:
            pass
        for i in range(len(article)):
            try:
                if i != 0:
                    health_data = driver.find_element_by_xpath(".//div[@class='hfeed post-list']")
                    article = health_data.find_elements_by_xpath(".//div[@class='post-wrapper']")

                blog_nature = []
                article_date = article[i].find_element_by_xpath(".//header[@class='entry-header']/time[@class='published']").text
                print("article_date:", article_date)
                blog_nature.append(article_date)
                article_title = article[i].find_element_by_xpath(".//header[@class='entry-header']/h2/a").text
                article_url = article[i].find_element_by_xpath(".//header[@class='entry-header']/h2/a").get_attribute('href')

                article_detail = article[i].find_element_by_xpath(".//header[@class='entry-header']/h2/a")
                article_detail.click()
                time.sleep(1.5)
                article_content_list = driver.find_element_by_xpath(".//section[@class='entry-content']")
                article_content = article_content_list.text
                print("article_title:", article_title)
                print("article_content:", article_content)

                driver.execute_script("window.history.go(-1)")
                time.sleep(1.5)
                print("article_url:", article_url)
                blog_nature.append(article_title)
                blog_nature.append(article_content)
                blog_nature.append(article_url)
                article_blog_data.append(blog_nature)

            except:
                pass
        try:
            # write csv file from array
            with open(file_name, 'a', newline='', encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=',')
                for line in article_blog_data:
                    writer.writerow(line)
            f.close()
            article_blog_data.clear()

        except:
            pass

        try:
            driver.get(page_url)
            driver.execute_script("window.scrollTo(0, 6000)")  # slide down part
            old_entry = driver.find_element_by_xpath('//a[contains(text(), "Older posts")]')
            old_entry.click()
            print("========================old entry========================")
        except:
            break

    print("=================================Success!,  Done!====================================")
    print("--- %s hours ---" % ((time.time() - start_time) / 3600))
    driver.quit()  # web browser close part

# Firefox driver calling part
def run_Firefox():
    profile = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=profile)
    driver.implicitly_wait(3)
    return driver

OPTIONS = ["https://www.health.harvard.edu/blog/"]

if __name__ == "__main__":

    # GUI setting part using tkinter
    master = Tk()
    master.title("Python Data Scraper")  # scraping interface title
    master.geometry("300x180")  # interface size
    Label = Label(master)
    Label["text"] = "URL:"
    Label.pack(padx=10, pady=10)
    variable = StringVar(master)
    variable.set(OPTIONS[0])  # default value
    w = OptionMenu(master, variable, *OPTIONS)
    w.pack()
    button_start = Button(master, command=health_download)
    button_start["text"] = "Start"
    button_start.pack(padx=30, pady=30, fill=X)
    master.mainloop()