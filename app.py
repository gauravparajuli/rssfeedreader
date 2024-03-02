from flask import Flask

app = Flask(__name__)

@app.get('/')
def home():
    return dict(message="it's working"), 200