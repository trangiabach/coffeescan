from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
import csv


PATH = 'D:/research_tools/chromedriver.exe'
URL = 'https://www.instagram.com/bemycoffee.hn/'


driver = webdriver.Chrome(service=Service(PATH))

username = "gbt2201"
password = "Bach123@"
INSTA = ("https://www.instagram.com/accounts/login/")
driver.get(INSTA)
time.sleep(5)
user = driver.find_element(by=By.CSS_SELECTOR, value='#loginForm > div > div:nth-child(1) > div > label > input')
user.send_keys(username)
passw = driver.find_element(by=By.CSS_SELECTOR, value='#loginForm > div > div:nth-child(2) > div > label > input')
passw.send_keys(password)
driver.find_element(by=By.CSS_SELECTOR, value='#loginForm > div > div:nth-child(3) > button').click()
time.sleep(5)


driver.get(URL)

def log_out():
    time.sleep(5)
    ele = driver.find_element(by=By.CLASS_NAME, value='_aa8i')
    ele.click()
    time.sleep(5)
    btns = driver.find_elements(by=By.CLASS_NAME, value='_abm4')
    btns[-1].click()
    time.sleep(5)

def scroll_down():
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")
    posts = set()


    with open('urls.csv', mode='w') as csv_file:
        fieldnames = ['url']
        writer =  csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while True:

            links = driver.find_elements(by=By.TAG_NAME, value='a')
            for link in links:
                post = link.get_attribute('href')
                if '/p/' in post and post not in posts:
                    posts.add(post)
                    writer.writerow({'url' : post})
                    print(str(len(posts)) + ' POSTS ADDED')
            # Scroll down to the bottom.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(5)

            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:

                break

            last_height = new_height
    return posts


posts = scroll_down()
log_out()

for post in posts:
    driver.get(post)
    time.sleep(5)
    ele = driver.find_element(by=By.CLASS_NAME, value="se6yk ")
    print(ele.text)
    
