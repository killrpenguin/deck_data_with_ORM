import seleniumwire
import asyncio
from seleniumwire import webdriver
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
        self.page = self.driver.get(self.link)

    def __await__(self):
        async def closure():
            for request in self.driver.requests:
                if (request.url == self.link) and (request.response.status_code in self.valid_resps):
                    print(f"Success! {request.response.status_code}")
                    print(f"{self.driver.page_source}")
                    return self
            return self
        return closure().__await__()


async def task_coroutine(link: str):
    driver = await Driver_Adapter(link=link)
    return driver


async def main():
    with open("mxlinks", "r") as link_list:
        link_list = link_list.read().strip().split("\n")
        tasks = [asyncio.create_task(task_coroutine(link)) for link in link_list]
        for task in tasks:
            await task


asyncio.run(main())
