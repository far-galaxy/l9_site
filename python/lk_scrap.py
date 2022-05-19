# -*- coding: utf-8 -*-
"""Scrapper for cabinet.ssau.ru
by far-galaxy for l9labs.ru

NOTE: This program is written only for educational purposes.
They does not try to bypass the protection of the site, 
but only helps to get data from her account using her own username and password. 
Users utilize this program at their own risk and are entirely responsible for the consequences!

:copyright: (c) 2022 far-galaxy https://github.com/far-galaxy 
:license: GNU GPL v3.0, see LICENSE for more details.
"""
import requests
from bs4 import BeautifulSoup

class LoginError(Exception):
    pass

class APIError(Exception):
    pass

class Scrapper(object):
    """Scrapper object"""
    
    def __init__(self):
        
        self.session = requests.Session() 

    def login(self, name, password):
        """
        Login by name and password and save cookies for keep session
        
        Returns `True` if login succesful or :class:`LoginError` if login failed
        """
        
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
        """
        Auth to site with token from cookie
        
        Args:
            :token: [optional] :class:`str`, necessary if the login has not been executed by :class:`login` function
            
        Returns:
            :class:`bool` succesful auth
        """
        
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
        """
        Execute API method
        https://cabinet.ssau.ru/api/
        
        :TODO: make methods doc
        
        Args:
            :method: :class:`str` name of the method
            :params: :class:`str` params of the method
            
        Returns:
            :class:`list` json method result
            
            :class:`APIError` if happened some error
        """        
        
        resp = self.session.get(f"https://cabinet.ssau.ru/api/{method}", headers = self.headers, params = params)
        
        if resp.status_code == 200:
            return resp.json()
        else:
            raise APIError(resp.status_code)
        
if __name__ == "__main__":
    """
    Example:
    Login and print messages from first chat in the messenger
    
    Create file "login.txt" in the module directory with 
    login and password from you cabinet account
    
    login.txt content example:
    my_login my_password
    """
    
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