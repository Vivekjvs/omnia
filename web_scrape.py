import requests
from bs4 import BeautifulSoup
import json

class codeforces:
    def __init__(self,urls: dict):
        self.urls = urls
 
    def get_users(self,username: str) -> dict:
        data = requests.get(self.urls['cf_userinfo'] + username)
        return json.loads(data)
    
    def get_problems(self,username:str):
        data = requests.get(self.urls['cf_problems'] + username)
        return json.loads(data)
        