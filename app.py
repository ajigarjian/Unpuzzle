# importing necessary frameworks and libraries 
from flask import Flask, render_template
import sqlite3

# Configure application
app = Flask(__name__)

# Connect to SQLite database pairs.db and initialize cursor based on connection
db = sqlite3.connect('pairs.db', check_same_thread=False)
cursor = db.cursor()

# Create route for logic behind home page. Fills list "rows" with rows from general table, and renders index.html template with "rows" as input
@app.route("/")
def index():
    """Show home page of 1Across"""
    rows = []
    for row in cursor.execute("SELECT * FROM general LIMIT 100"):
        rows.append(row)
    return render_template("index.html", rows=rows)

@app.route("/modules")
def modules():
    """Show modules page of 1Across"""

    return render_template("modules.html")

#syntax to run app.py
if __name__ == "__main__":
    app.run(debug=True)