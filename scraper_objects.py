import requests
import re
from bs4 import BeautifulSoup as bs


class Decks(object):
    def __init__(self):
        self.deck_list_database = self.get_ddb_list()
        self.proxies = 'http://43.157.8.79:8888'
        # self.proxies = proxy_pool.asyncio.run(main_proxy_pool())
        self.decks = []

    def get_ddb_list(self) -> list:
        url = "https://cedh-decklist-database.com/"
        page = requests.get(url)
        soup = bs(page.content, "html.parser")
        deck_hrefs = [element['href'] for element in soup.find_all('a', href=True)]
        # regex removes any href with the word discord, scryfall, docs and anything that starts with a /
        deck_hrefs = [re.sub('^/.+|.+discord.+|.+scryfall.+|.+docs.+|', '', href) for href in deck_hrefs]
        deck_hrefs = [href.strip() for href in deck_hrefs if '' != href if '/' != href]
        return deck_hrefs

