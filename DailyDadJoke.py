import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time 

# Create a new instance of the Firefox driver
options = webdriver.EdgeOptions()
options.headless = True
driver = webdriver.Edge(options=options)

# Navigate to the website you want to scrape
driver.get("https://www.beagreatteacher.com/daily-fun-fact/")

# Extract the page source
page_source = driver.page_source

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(page_source, 'html.parser')

# Find the elements you want to scrape
elements = soup.find_all('div', class_='content-sidebar-wrap')

# Do something with the elements, e.g. extract text
for element in elements:
    headers = element.find_all(['h2'])
    paragraphs = element.find_all('p')
    heads=[]
    answers=[]
    for header in headers:
        heads.append(header.text)

    for paragraph in paragraphs:
        answers.append(paragraph.text)
    
    dictionary = dict(zip(heads, answers))
    print(dictionary)


# Close the browser
driver.quit()


