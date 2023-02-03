import requests
from bs4 import BeautifulSoup
import time 


while True:
    url = "https://www.idokep.hu/radar#riasztas"

    response = requests.get(url)

    # Parse HTML
    soup = BeautifulSoup(response.content, "html.parser")

    div = soup.find("div", {"class": "container ik alert-bar yellow p-0"})

    # read the div out
    try:
        print(div.text) 
    except:
        print("Nincs Riasztas")
    
    time.sleep(360)
