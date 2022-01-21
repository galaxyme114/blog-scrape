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
        file_name = 'blog_rsc.csv'
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
def blog_rsc_download():
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
            blog_rsc_data = driver.find_element_by_id("page")
            article_rsc = blog_rsc_data.find_element_by_xpath(".//div[@class='content-wrapper']")
            article_content = article_rsc.find_element_by_id("content")
            article = article_content.find_elements_by_xpath(".//div[contains(@class, 'post type-post status-publish format-standard hentry')]")

        except:
            pass
        for i in range(len(article)):

            try:
                if i != 0:
                    blog_rsc_data = driver.find_element_by_id("page")
                    article_rsc = blog_rsc_data.find_element_by_xpath(".//div[@class='content-wrapper']")
                    article_content = article_rsc.find_element_by_id("content")
                    article = article_content.find_elements_by_xpath(".//div[contains(@class, 'post type-post status-publish format-standard hentry')]")

                blog_nature = []
                article_date = article[i].find_element_by_xpath(".//div[@class='postdate date']").text
                print("article_date:", article_date)
                blog_nature.append(article_date)
                article_title = article[i].find_element_by_xpath(".//h2/a").text
                article_url = article[i].find_element_by_xpath(".//h2/a").get_attribute('href')

                article_detail = article[i].find_element_by_xpath(".//h2/a")
                article_detail.click()
                time.sleep(1.5)
                article_content_list = driver.find_element_by_xpath(".//div[@class='content-wrapper']")
                article_content = article_content_list.find_element_by_xpath(".//div[@class='widecolumn']/div[contains(@class, 'post type-post status-publish format-standard hentry')]/div[@class='entry']").text
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
            old = driver.find_elements_by_xpath('.//div[@class="clearfix navigation wplnavg"]')
            old_temp = old[1]
            old_entry = old_temp.find_element_by_xpath(".//div[@class='alignleft fl wplleft']/a")

            old_entry.click()
            print("========================old entry========================")
        except:
            break
    print("===============================Success!,  Done!====================================")
    print("--- %s hours ---" % ((time.time() - start_time) / 3600))
    driver.quit()  # web browser close part




# Firefox driver calling part
def run_Firefox():
    profile = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=profile)
    driver.implicitly_wait(3)
    return driver


OPTIONS = ["http://blogs.rsc.org/tx/"]

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
    button_start = Button(master, command=blog_rsc_download)
    button_start["text"] = "Start"
    button_start.pack(padx=30, pady=30, fill=X)
    master.mainloop()