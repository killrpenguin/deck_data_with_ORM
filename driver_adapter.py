import seleniumwire
import asyncio
import random
from seleniumwire import webdriver
from seleniumwire.webdriver import EdgeOptions

class Adapter_Error(Exception):
    pass


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
        self.user_agent = ''
        # self.proxy = 'http://24.158.29.166:80'

    def __await__(self) -> webdriver:
        async def closure():
            for request in self.requests:
                if (request.url == self.link) and (request.response.status_code in self.valid_resps):
                    print(f"Success! {request.response.status_code}")
                    return self
            return self

        return closure().__await__()

    @property
    def get_random_agent(self):
        with open("Master_User_Agents") as file:
            user_agent_list = file.read().strip().split("\n")
            self.user_agent = user_agent_list.pop(random.randint(0, len(user_agent_list)))
            return self.user_agent
