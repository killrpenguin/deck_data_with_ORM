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
        # edge_options.add_argument("headless")
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

    async def testing(self):
        self.execute_script("$.get(page_link%s)" % self.link)
        print("show me something")
        return self

page_link = "https://www.moxfield.com/decks/DujxA8PlG0eTQZ_hawsTmQ"


async def task_coroutine(link: str):
    driver = await Driver_Adapter(link=link)
    await driver.testing()
    return driver


async def main():
    with open("mxlinks", "r") as link_list:
        link_list = link_list.read().strip().split("\n")
        tasks = [asyncio.create_task(task_coroutine(link)) for link in link_list]
        for task in tasks:
            await task


asyncio.run(main())
