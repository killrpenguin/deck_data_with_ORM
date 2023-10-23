import seleniumwire
import asyncio
from seleniumwire import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from seleniumwire.webdriver import EdgeOptions


class Driver_Adapter(webdriver.Edge):
    def __init__(self, link, *args, **kwargs):
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument("start-maximized")
        edge_options.page_load_strategy = "eager"
        edge_options.add_argument("disable-gpu")
        edge_options.add_argument("headless")
        edge_options.add_argument("--proxy_server=%s" % "http://24.158.29.166:80")
        super().__init__(edge_options=edge_options)
        self.link = link
        self.valid_resps = [200, 301, 302, 307, 404]
        self.page = self.get(self.link)
        self.top_16 = self.top_16()

    def top_16(self) -> set:
        xpath = '//*[@id="root"]/div/div[2]/table/tbody/descendant::a'
        wait = WebDriverWait(self, 30)
        top_16_decks = wait.until(ec.presence_of_all_elements_located((By.XPATH, xpath)))
        top_16_decks = [attribute.get_attribute("href") for attribute in top_16_decks]
        return set(top_16_decks)


page_link = "https://edhtop16.com/commander/Kraum,%20Ludevic's%20Opus%20+%20Tymna%20the%20Weaver?tourney_filter__size__" \
       "%24gte=64&tourney_filter__dateCreated__%24gte=1660826678"
test = Driver_Adapter(link=page_link)
for link in test.top_16:
    print(f"{link}")

print(f"{len(test.top_16)}")
