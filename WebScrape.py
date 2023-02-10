import requests
from bs4 import BeautifulSoup
import time 


while True:
    url = "https://www.idokep.hu/radar#riasztas"

    response = requests.get(url)

    # Parse a HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # ha kell masik div class csak modositsd 
    div = soup.find("div", {"class": "container ik alert-bar yellow p-0"})

    # a .text csak kiolvassa a divet ha letezik ha nem vissza adja hogy nincs riasztas.
    try:
        print(div.text) 
    except:
        print("Nincs Riasztas")
    
    time.sleep(360)
