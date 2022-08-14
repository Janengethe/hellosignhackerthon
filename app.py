#!/usr/bin/env python3
from flask import Flask
from database.engine import Transaction, Agent, Customer, DB

app = Flask(__name__)

app.url_map.strict_slashes = False

@app.route("/")
def index():
    t = Transaction()
    a = Agent()
    c = Customer()
    db = DB()
    return ("Am Micheal Scott")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)