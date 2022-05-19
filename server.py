from flask import *

app = Flask(__name__)

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

app.run(host="localhost", port=5000)