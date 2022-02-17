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

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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
        days_checked = request.form.getlist("Day_checked")

        if not answer:
            answer = ''

        if not clue:
            clue = ''

        # Date formatting
        if not start:
            start = "1900-01-01"
        
        if not end:
            end = "2100-01-01"

        if not days_checked:
            days_checked= DAYS

        #editing dates to format the db data
        formatted_start = (start[0:4] + "-" + start[5:7].lstrip("0") + "-" + start[8:10].lstrip("0"))
        formatted_end = (end[0:4] + "-" + end[5:7].lstrip("0") + "-" + end[8:10].lstrip("0"))

        # ------------ Search queries ---------------

        # Create string of dynamic length of ?s, e.g. if 3 checkboxes are selected for weekdays, the string is "?, ?, ?"
        placeholders= ', '.join('?' * len(days_checked))

        # add days we're checking for into a new list plus the other parameters we're checking for. These are all the ? values"
        parameters = []
        for value in days_checked:
            parameters.append(value)
        parameters.extend((answer, '%' + clue + '%', formatted_start, formatted_end))

        #main query
        query = """SELECT * FROM general WHERE 
                    weekday IN (%s)
                    AND answer = COALESCE(NULLIF(?, ''), answer)
                    AND clue LIKE COALESCE(NULLIF(?, ''), clue) 
                    AND date >= ? AND date <= ?
                    ORDER BY date
                    LIMIT 1000""" % placeholders

        rows = []

        for row in cursor.execute(query, parameters):
            rows.append(row)

        #TO DO: fix date clause in main SQL query

        return render_template("databased.html", rows = rows, count = len(rows), clue_placeholder = clue, answer_placeholder = answer, days = DAYS)

    else:
        return render_template("database.html", days = DAYS)

#syntax to run app.py
if __name__ == "__main__":
    app.run(debug=True)