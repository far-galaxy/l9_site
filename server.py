from flask import *
from python.lk_scrap import Scrapper
import os

app = Flask(__name__)
scrapper = Scrapper()

@app.route('/')
def index():
    return send_file("index.html")

@app.route('/lk')
def lk():
    return send_file("lk.html")

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
    
    if request.headers['Accept'].find("text/html") != -1:
        return send_file("lk.html")

    path = os.path.abspath("python/login.txt")
    with open(path, "r", encoding="utf-8") as f:
        login, password = f.read().split()  
        
    if scrapper.login(login, password):
        chats = scrapper.method("chats", {"isArchive":0})
        response = app.response_class(
                response=json.dumps(chats),
                mimetype='application/json')        
        return response
    

app.run(host="localhost", port=5000)