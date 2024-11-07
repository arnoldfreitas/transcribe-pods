from pprint import pprint
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By


class WebNavigator():
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

    def find_clickable(self, button_text='//button[text()="Posts mais antigos"]'):
        elems = self.driver.find_elements(By.XPATH, button_text)

        # print(elems)
        if elems:
            return elems[0]
        else: 
            return False