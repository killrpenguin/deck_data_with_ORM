from contextlib import asynccontextmanager
import random
import seleniumwire
from seleniumwire.request import *
from seleniumwire.webdriver import EdgeOptions


class Adapter_Error(Exception):
    pass


@asynccontextmanager
class Driver_Adapter(object):
    def __init__(self, link):
        self.link = link
        self.user_agent = self.get_random_agent
        self.proxy = "http://134.195.101.34:8080"
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument("headless")
        edge_options.add_argument("start-maximized")
        edge_options.page_load_strategy = "eager"
        edge_options.add_argument("disable-gpu")
        edge_options.add_argument("--proxy_server=%s" % self.proxy)
        edge_options.add_argument("--user_agents=%s" % self.user_agent)
        self.driver = seleniumwire.webdriver.Edge(options=edge_options)
        self.page = self.get_page()

    def __aiter__(self):
        return self

    def __anext__(self):


    async def get_page(self):
        page = self.driver.get(self.link)
        try:
            yield page
        except Exception as e:
            print(f"Error: {e}")

    @property
    def page_status_code(self):
        for request in self.driver.requests:
            if request.url == self.link:
                return request.response.status_code

    @property
    def get_random_agent(self):
        with open("Master_User_Agents") as file:
            user_agent_list = file.read().strip().split("\n")
            self.user_agent = user_agent_list.pop(random.randint(0, len(user_agent_list)))
            return self.user_agent
