import requests
import re
import random
import selenium
import asyncio
import aiohttp
from dataclasses import dataclass, field
from typing import Dict, List
import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as bs
from seleniumwire.undetected_chromedriver.webdriver import E
from seleniumwire.webdriver import EdgeOptions
import seleniumwire.request


class Driver_Obj:
    def __init__(self):
        self.user_agent = self.get_random_agent()
        self.proxy = "http://134.195.101.34:8080"
        edge_options = ue.EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument("headless")
        edge_options.add_argument("start-maximized")
        edge_options.page_load_strategy = "eager"
        edge_options.add_argument("disable-gpu")
        edge_options.add_argument("--proxy_server=%s" % self.proxy)
        edge_options.add_argument("--user_agents=%s" % self.user_agent)
        edge_options.add_argument("--disable-blink-features")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)
        self.driver = seleniumwire.webdriver.Edge(options=edge_options)

    def get_random_agent(self):
        with open("Master_User_Agents") as file:
            user_agent_list = file.read().strip().split("\n")
            self.user_agent = user_agent_list.pop(random.randint(0, len(user_agent_list)))
            return self.user_agent

    def interceptor(self, request):
        del request.headers['user-agent']
        del request.headers['sec-ch-ua']
        request.headers['user-agent'] = self.user_agent
        request.headers['sec-ch-ua'] = '"Mozilla";v="5.0", "Not;A=Brand";v="8"'
        return request.headers

    def scrape(self, deck_link):
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.request_interceptor = self.interceptor
        self.driver.get(deck_link)
        for i in self.driver.requests:
            print(f"{i.headers}")
