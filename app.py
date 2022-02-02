import os

from flask import Flask, render_template
import sqlite3

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = sqlite3.connect('pairs.db', check_same_thread=False)
cursor = db.cursor()

@app.route("/")
def index():
    """Show home page of UnPuzzle"""


    rows = []
    for row in cursor.execute("SELECT * FROM general LIMIT 100"):
        rows.append(row)
    return render_template("index.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)