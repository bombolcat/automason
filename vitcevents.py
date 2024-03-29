import requests
import asyncio
import aiohttp
import re
import json
import time
from bs4 import BeautifulSoup
from pprint import pprint

class VITCEvents:

    def __init__(self):
        total_card_count=0


    async def get_all_cards(self):
        '''
        This function returns a list of all the values of the cards in the website.
        The values can be used to get all the data about a particular card/event.
        This function also updates the total_card_count variable which is the total number of cards in the website.
        '''

        with requests.Session() as s:
            response= s.get('https://vitchennaievents.com/conf1/')
            soup = BeautifulSoup(response.text, 'html.parser')
            all_cards=soup.find_all('div', class_='card')
            '''all_cards contain some cards which are not events. They are just divs with h1 tag.
            They have the heading as df,so we can filter them out by checking the df in the heading'''

            self.total_card_count=0
            all_card_values=[]

            total_cards=0

            for card in all_cards:
                headings=card.find_all('h1')
                
                if(len(headings)==1 and headings[0].text=="df"):
                    continue

                try:
                    value_match = re.search(r'value="([^"]+)"', str(card))
                    # print(f"{value_match.group(1)} is the value for {headings[0].text}")
                    total_cards+=1
                    all_card_values.append(value_match.group(1))
                except AttributeError:
                    pass

            if(total_cards>=self.total_card_count):
                self.total_card_count=total_cards
                # self.push_all_cards(all_card_values)

            return all_card_values
    
    async def push_all_cards(self,write=True):

        all_card_values=await self.get_all_cards()
        all_list=[]
        with requests.Session() as session:
            for card_value in all_card_values:
                with session.get(f'https://vitchennaievents.com/conf1/det/getEventData.php?eid={card_value}') as response:
                    text_data=response.json()
                    all_list.append(text_data)

        with open(f"cards.json", "w+") as json_file:
            json.dump(all_list, json_file)

        return all_list
    
    async def push_card():
        pass

if __name__=="__main__":
    scrape=VITCEvents()
    asyncio.run(scrape.push_all_cards(write=True))