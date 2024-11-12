import re
import os
from pprint import pprint
import json
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from utils import load_from_json, save_to_json


data_folder_path = os.path.abspath(os.path.join(__file__, "./../../data"))

class PodAutomata():
    def __init__(self) -> None:
        # set up headless option
        service = Service()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def start_session(self, base_url):
        self.driver.get(base_url)

    def teardown(self):
        self.driver.quit()

    def find_links_by_regex(self, 
            regex='.*\d{1,4}/\d{1,2}/\d{1,2}/xadrez-verbal-podcast-\d{1,3}',
            ):
        """
        fronteiras-invisiveis-do-futebol
        """
        elems = self.driver.find_elements(By.XPATH, "//a[@href]")
        output = []
        for elem in elems:
            tmp = elem.get_attribute("href")
            if (re.match(regex, tmp)) and \
                (tmp.endswith(".mp3")):
                # (not tmp.endswith("#comments")):
                output.append(tmp)
        
        return list(set(output))

    def collect_urls_from_pages(self,
                                base_url, 
                                n_pages = 100,
                                regex = '.*\d{1,4}/\d{1,2}/\d{1,2}/xadrez-verbal-podcast-\d{1,3}',
                                podcast_name = "xadrez_verbal", # fronteiras_invisiveis
                                source_data = None):
        out = []
        for i in range(1,n_pages):
            url = f"{base_url}/{i}"
            print(f"{i} : {url}")
            self.start_session(url)
            out.extend(self.find_links_by_regex(
                regex=regex))
            self.driver.implicitly_wait(2)
            print(len(out))

        self.teardown()
        pprint(set(out))

        if source_data is not None and \
        os.path.exists(f'{data_folder_path}/{source_data}'):
            data = load_from_json(source_data)
            data.update({f'{podcast_name}': list(set(out))})
            save_to_json(data, info=podcast_name)
        else:
            save_to_json(list(set(out)), info=podcast_name)

    def list_eps_for_download(self,
                              episodes_sources,
                              podcast="fronteiras_invisiveis"):
        data = load_from_json(episodes_sources)

        out = []
        for i, item in enumerate(data[podcast]):
            print(i, item)
            self.start_session(item)
            out.extend(
                self.find_links_by_regex(
                    regex='.*mp3.*'))
            print(len(set(out)))
            self.driver.implicitly_wait(2)

        pprint(set(out))
        self.teardown()
        save_to_json(list(set(data)), info=f"episodes_{podcast}")

    def find_clickable(self, button_text='//button[text()="Posts mais antigos"]'):
        elems = self.driver.find_elements(By.XPATH, button_text)

        # print(elems)
        if elems:
            return elems[0]
        else: 
            return False

def download_ep(ep = "https://api.spreaker.com/download/episode/42461659/fronteiras_20_africa_do_sul.mp3",
                podcast= "fronteiras_invisiveis"):
    
    ep_name = "fronteiras_20_africa_do_sul"
    response = requests.get(ep)
    save_to = f"{data_folder_path}/{podcast}/{ep_name}.mp3"
    print(save_to)
    open(save_to, "wb").write(response.content)

if __name__=="__main__":
#    collect_urls()
    download_ep()