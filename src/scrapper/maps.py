import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Maps:

    lat = '@19.432608'
    lng = '-99.133209'
    api_url = "https://serpapi.com/playground?engine=google_maps&q=coffee&ll={}%2C{}%2C14z&hl=en&type=search"
    categories = ["cafeteria"]
    mapData = []
    jsonName = "data.json"
    driver = None

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=options)
        f = open(self.jsonName)
        self.mapData = json.load(f)

    def run(self):
        self.driver.get(self.api_url.format(self.lat, self.lng))

        for category in self.categories:
            url = self.getApiUrl(category)
            self.getData(url)
            time.sleep(5)

        with open(self.jsonName, 'w') as file:
            json.dump(self.mapData, file)

    def getData(self, url):
        r = requests.get(url)
        data = r.json()

        for result in data["local_results"]:
            if not any(item['title'] == result["title"] for item in self.mapData):
                self.mapData.append({
                    "title": result["title"] if 'title' in result else '',
                    "address": result["address"] if 'address' in result else '',
                    "phone": result["phone"] if 'phone' in result else '',
                    "website": result['website'] if 'website' in result else ''
                })

    def getApiUrl(self, category):
        time.sleep(5)
        elem = self.driver.find_element(By.ID, "q")
        elem.clear()
        elem.send_keys(category)
        elem.send_keys(Keys.RETURN)
        time.sleep(5)
        inputHidden = self.driver.find_element(By.ID,"html-url")
        inputHidden = inputHidden.get_attribute('value')

        return "{}&async=true".format(inputHidden.replace("search.html","search.json"))

    def __del__(self):
        self.driver.close()
