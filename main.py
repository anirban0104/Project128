import pandas as pd 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Navigate to the Wikipedia page listing Brown Dwarf stars
START_url = 'https://en.wikipedia.org/wiki/List_of_brown_dwarfs'
browser = webdriver.Chrome("chromedriver.exe")
browser.get(START_url)
time.sleep(10)

# Scraping data
dwarf_stars_data = []

def scrape():
    for i in range(0, 10):
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        table_tag = soup.find_all('table')[2] # Selecting the 3rd table (Field brown dwarfs)
        tbody_tag = table_tag.find('tbody')
        for tr_tag in tbody_tag.find_all('tr')[1:]: # Skip the first row (header row)
            temp_list = []
            for td_tag in tr_tag.find_all('td'):
                temp_list.append(td_tag.get_text().strip())
            dwarf_stars_data.append(temp_list)
        browser.find_element(by=By.XPATH, value='//*[@id="mw-content-text"]/div[1]/table/tbody/tr/td[3]/span/a').click() # Clicking on the next page link

scrape()

# Creating DataFrame and saving data to CSV
headers = ['Name', 'Constellation', 'Right ascension', 'Declination', 'App. mag.']
dwarf_stars_df = pd.DataFrame(dwarf_stars_data, columns=headers)
dwarf_stars_df.to_csv('dwarf_stars.csv', index=False)
