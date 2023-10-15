import seleniumwire
from seleniumwire import webdriver
from seleniumwire.webdriver import EdgeOptions
import asyncio
import traceback


class Driver_Adapter:
    def __init__(self, link):
        self.link = link
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument("start-maximized")
        edge_options.page_load_strategy = "eager"
        edge_options.add_argument("disable-gpu")
        edge_options.add_argument("headless")
        self.driver = seleniumwire.webdriver.Edge(options=edge_options)
        self.page = self.get_req()

    def __await__(self):
        async def closure():
            valid_resps = [200, 301, 302, 307, 404]
            await asyncio.sleep(2)
            for request in self.driver.requests:
                if (request.url == self.link) and (request.response.status_code in valid_resps):
                    print(f"Success! {request.response.status_code}")
                    return self
            return self
        return closure().__await__()

    def get_req(self):
        try:
            return self.driver.get(self.link)
        except Exception as e:
            print(f'Exception: {e}\n{traceback.format_exc()}')
async def task_coroutine(link):
    driver = await Driver_Adapter(link=link)
    return driver


async def main():
    with open("mxlinks", "r") as link_list:
        link_list = link_list.read().strip().split("\n")
        tasks = [asyncio.create_task(task_coroutine(link)) for link in link_list]
        for task in tasks:
            await asyncio.gather(task)



asyncio.run(main())