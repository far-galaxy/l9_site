from flask import *
from python.lk_scrap import Scrapper
import os

app = Flask(__name__)
scrapper = Scrapper()

@app.route('/')
def hello_world():
    return "hello"

@app.route('/<path:path>')
def get_files(path):
    try:
        if (path.find("style") != -1 or 
        path.find("media") != -1 or
        path.find(".html") != -1):
            return send_file(path)
        else:
            abort(404)
    except FileNotFoundError:
        abort(404)
        
@app.route('/msg', methods=['GET'])
def get():
    
    path = os.path.abspath("python/login.txt")
    with open(path, "r", encoding="utf-8") as f:
        login, password = f.read().split()  
        
    if scrapper.login(login, password):
        chats = scrapper.method("chats", {"isArchive":0})
        return chats
    

app.run(host="localhost", port=5000)