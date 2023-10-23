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
        super().__init__(options=edge_options)
        self.link = link
        self.valid_resps = [200, 301, 302, 307, 404]
        self.driver = seleniumwire.webdriver.Edge(options=edge_options)
        self.top_16 = []

    def __await__(self):
        async def closure():
            for request in self.driver.requests:
                if (request.url == self.link) and (request.response.status_code in self.valid_resps):
                    print(f"Success! {request.response.status_code}")
                    print(f"{self.driver.page_source}")
                    return self
            return self
        return closure().__await__()

    def get_top16(self) -> list:
        link = "https://edhtop16.com/commander/Kraum," \
               "%20Ludevic's%20Opus%20+%20Tymna%20the%20Weaver?tourney_filter__size__%24gte=64" \
               "&tourney_filter__dateCreated__%24gte=1660826678"
        xpath = '//*[@id="root"]/div/div[2]/table/tbody/tr[1]/td[2]/span/a'
        wait = WebDriverWait(self.driver, 30)
        self.top_16 = wait.until(ec.presence_of_element_located((By.XPATH, xpath))).text.strip()
        return self.top_16

async def task_coroutine(link: str):
    driver = await Driver_Adapter(link=link)
    driver.get_top16()
    print(f"{driver.top_16}")
    return driver


async def main():
    with open("mxlinks", "r") as link_list:
        link_list = link_list.read().strip().split("\n")
        tasks = [asyncio.create_task(task_coroutine(link)) for link in link_list]
        for task in tasks:
            await task


asyncio.run(main())
