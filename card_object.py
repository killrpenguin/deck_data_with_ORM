import asyncio
import aiohttp
import json
import traceback
import requests
import time
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import List, Dict


class Card(Deck):
    def __init__(self, card_name):
        super().__init__(self.deck_link, self.proxy)
        self.deck_link = self.deck_link
        self.proxy = self.proxy
        self.card_name = card_name
        self.card_dict = self.get_json_dict(card_name)
        self.card_layout = self.card_dict['layout']
        self.faces = self.make_faces(self.card_dict)
        self.legal_status = self.card_dict['legalities']['commander']

    def display_card(self):
        print(f"Card Name: {self.card_name}\n"
              f"Layout: {self.card_layout}")
        for face in self.faces:
            print(f"\ncmc: {face.cmc}, mc: {face.mana_cost}, type: {face.card_type}, colors: {face.color_ident}")

    def get_json_dict(self, card) -> Dict:
        link = "https://api.scryfall.com/cards/named?fuzzy=" + card
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")
        card_dict = json.loads(soup.text)
        time.sleep(.25)
        return card_dict

    def make_faces(self, card) -> list:
        faces = []
        try:
            for side in range(len(card['card_faces'])):
                faces.append(Face(face_name=card['card_faces'][side]['name'],
                                  cmc=card['cmc'], mana_cost=card['card_faces'][side]['mana_cost'],
                                  card_type=card['card_faces'][side]['type_line'],
                                  card_text=card['card_faces'][side]['oracle_text'],
                                  color_ident=card['color_identity']))
        except KeyError:
            faces.append(Face(face_name=card['name'], cmc=card['cmc'], mana_cost=card['mana_cost'],
                              card_type=card['type_line'], card_text=card['oracle_text'],
                              color_ident=card['color_identity']
                              ))
        return self.faces

@dataclass
class Face(object):
    face_name: str = field(default=str)
    cmc: float = field(default=float)
    mana_cost: str = field(default=str)
    card_type: str = field(default=str)
    card_text: List = field(default=list)
    color_ident: str = field(default=str)


async def card_coroutine(session, card_name):
    valid_status = [200, 301, 302, 307, 404]
    try:
        async with session.get(f"https://api.scryfall.com/cards/named?fuzzy={card_name}",
                               ssl=False,
                               timeout=500) as scryfall_req:
            await scryfall_req.text()
            if scryfall_req.status in valid_status:
                print(f"{scryfall_req.text}")
    except Exception as e:
        print(f"Exception: {e}\n{traceback.format_exc()} ")



async def main_card_data_collection(card_list):
    tcp_connection = aiohttp.TCPConnector(limit=250)
    header = {"Authorization": "Basic bG9naW46cGFzcw=="}
    async with aiohttp.ClientSession(connector=tcp_connection,
                                     headers=header,
                                     trust_env=True) as session:
        try:
            tasks = [asyncio.create_task(card_coroutine(session=session,
                                                        card_name=card_name)) for card_name in card_list]
            for task in tasks:
                await task
        except Exception as e:
            print(f"{e}")
        await asyncio.sleep(0)


with open("card_list", "r") as card_list:
    asyncio.run(main_card_data_collection(card_list))