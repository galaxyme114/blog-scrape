from selenium import webdriver 
import time
profile = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=profile)
driver.implicitly_wait(3)
#driver.set_window_size(1920, 1200)
driver.get('https://wordpress.org/themes/browse/popular/')
time.sleep(3)
for i in range(50):
    driver.execute_script("window.scrollTo(0, " + str(1500 * i) + ");") # slide down part
    time.sleep(1)
#driver.execute_script("window.scrollTo(501, 1500)")  # slide down part
#height = driver.execute_script("return document.documentElement.scrollHeight")
#driver.execute_script("window.scrollTo(0, " + str(height) + ");")
time.sleep(2)

titles = driver.find_elements_by_xpath(".//h3[@class = 'theme-name entry-title']")
print(len(titles))
for title in titles:
    title_name = title.text 
    print(title_name)

