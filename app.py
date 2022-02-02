import os

from flask import Flask, render_template
import sqlite3

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = sqlite3.connect('pairs.db', check_same_thread=False)

@app.route("/")
def index():
    """Show home page of UnPuzzle"""

    rows = db.execute("SELECT answer FROM general LIMIT 10")
    rows = rows.fetchall()
    return render_template("index.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)