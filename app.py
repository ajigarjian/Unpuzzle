# importing necessary frameworks and libraries 
import os
from datetime import date
from flask import Flask, render_template, redirect, request
import sqlite3

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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

@app.route("/database", methods=['GET', 'POST'])
def database():
    """Show database page of 1Across"""

    if request.method == "POST":

        answer = request.form.get("answer")
        print(answer)

        rows = []
        for row in cursor.execute("SELECT * FROM general WHERE answer = ?", [answer]):
            rows.append(row)
        return render_template("databased.html", rows=rows)

    else:
        return render_template("database.html")

#syntax to run app.py
if __name__ == "__main__":
    app.run(debug=True)