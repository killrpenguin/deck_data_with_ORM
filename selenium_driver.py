import requests
import re
import random
import selenium
import asyncio
import aiohttp
import seleniumwire
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
from selenium import webdriver
from seleniumwire.webdriver import EdgeOptions


class Driver_Obj:
    def __init__(self):
        self.user_agent = self.get_random_agent()
        self.proxy = "http://134.195.101.34:8080"
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument("headless")
        edge_options.add_argument("start-maximized")
        edge_options.page_load_strategy = "eager"
        edge_options.add_argument("disable-gpu")
        edge_options.add_argument("--proxy_server=%s" % self.proxy)
        edge_options.add_argument("--user_agents=%s" % self.user_agent)
        self.driver = webdriver.Edge(options=edge_options)

    def get_random_agent(self):
        with open("Master_User_Agents") as file:
            user_agent_list = file.read().strip().split("\n")
            self.user_agent = user_agent_list.pop(random.randint(0, len(user_agent_list)))
            return self.user_agent


