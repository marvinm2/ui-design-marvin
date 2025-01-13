"""Importing flask"""
from flask import Flask, render_template
from dotenv import load_dotenv
#import os
#import requests

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    """Route to index page"""
    return render_template('/index.html')


if __name__ == '__main__':
    app.run(debug=True)
