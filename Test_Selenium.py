from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/snap/chromium/1967/usr/lib/chromium-browser/chromedriver')
driver.get("https://www.google.com")


search_box = driver.find_element_by_xpath("//input[@class='gLFyf gsfi']")
search_box.send_keys("Yamaha")

search_btn = driver.find_element_by_xpath("(//input[@class='gNO89b'])[2]")
search_btn.click()

driver.close()