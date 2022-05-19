# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

class LoginError(Exception):
    pass

class APIError(Exception):
    pass

class Scrapper(object):
    def __init__(self):
        
        self.session = requests.Session() 

    def login(self, name, password):
        
        data = {}
        data["name"] = name
        data["password"] = password
        
        resp = self.session.post("https://cabinet.ssau.ru/login", data = data)
        
        if resp.status_code == 403:
            raise LoginError("Incorrect login/password")
        elif resp.status_code == 404:
            raise LoginError("Not Found, check connection")        
        elif resp.status_code == 200:
            self.token = resp.cookies["laravel_session"]
            return self.auth()
        
    def auth(self, token=None):
        
        if token == None: token = self.token
        cookie = {}
        cookie["laravel_session"] = token
        cookie["laravel_token"] = token
        
        resp = self.session.get("https://cabinet.ssau.ru/", cookies=cookie)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'lxml')
            csrf_token = soup.select_one('meta[name="csrf-token"]')['content']
            self.headers = {}
            self.headers['Accept'] = 'application/json'
            self.headers['X-CSRF-TOKEN'] = csrf_token
            return True
        else:
            return False
        
    def method(self, method, params):
        
        resp = self.session.get(f"https://cabinet.ssau.ru/api/{method}", headers = self.headers, params = params)
        
        if resp.status_code == 200:
            return resp.json()
        else:
            raise APIError(resp.status_code)
        
if __name__ == "__main__":
    scrap = Scrapper()
    
    with open("login.txt", "r", encoding="utf-8") as f:
        login, password = f.read().split()
    
    try:
        if scrap.login(login, password):
            print("Login succesful")
            chats = scrap.method("chats", {"isArchive":0})
            print([i["id"] for i in chats])
            first_id = chats[0]["id"]
            chat = scrap.method(f"chats/{first_id}", {"limit":100, "offset":0})
            print([i["text"] for i in chat])
        else:
            print("Some error")
    except LoginError as e:
        print(f"Login failed: {e}")