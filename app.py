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

        answer = (request.form.get("answer")).upper()
        clue = (request.form.get("clue"))
        start = request.form.get("start_date")
        end = request.form.get("end_date")

        if not answer:
            answer = ''

        # Date formatting
        if not start:
            start = "1900-01-01"
        
        if not end:
            end = "2100-01-01"

        formatted_start = ""
        formatted_end = ""

        if int(start[8:10]) > 9:
            if int(start[5:7]) > 9:
                formatted_start = start[5:7] + "/" + start[8:10] + "/" + start[0:2]
            else:
                formatted_start = start[6:7] + "/" + start[8:10] + "/" + start[0:2]
        else:
            if int(start[5:7]) > 9:
                formatted_start = start[5:7] + "/" + start[9:10] + "/" + start[0:2]
            else:
                formatted_start = start[6:7] + "/" + start[9:10] + "/" + start[0:2]

        if int(end[8:10]) > 9:
            if int(end[5:7]) > 9:
                formatted_end = end[5:7] + "/" + end[8:10] + "/" + end[0:2]
            else:
                formatted_end = end[6:7] + "/" + end[8:10] + "/" + end[0:2]
        else:
            if int(end[5:7]) > 9:
                formatted_end = end[5:7] + "/" + end[9:10] + "/" + end[0:2]
            else:
                formatted_end = end[6:7] + "/" + end[9:10] + "/" + end[0:2]


        # ------------ Search queries ---------------
        rows = []

        # for row in cursor.execute("SELECT * FROM general WHERE answer = ?", [answer]):
        #     rows.append(row)

        #  # 2/12 attempt at clue search
        # for row in cursor.execute("SELECT * FROM general WHERE clue LIKE ?", ["%" + clue + "%"]): 
        #     rows.append(row)

        for row in cursor.execute("SELECT * FROM general WHERE answer = COALESCE(NULLIF(?, ''), answer) AND clue LIKE COALESCE(NULLIF(?, ''), clue) LIMIT 1000", [answer, '%' + clue + '%']):
            rows.append(row)
        
        #this is the latest working trial of date search
        # if not answer:
        # for row in cursor.execute("SELECT * FROM general WHERE date BETWEEN date(?) AND date(?) ORDER BY date LIMIT 100", [start, end]):
        #    rows.append(row)

        return render_template("databased.html", rows=rows, clue_placeholder = clue, answer_placeholder = answer)

    else:
        return render_template("database.html")

#syntax to run app.py
if __name__ == "__main__":
    app.run(debug=True)