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

        print(days_checked)

        #editing dates to format the db data
        formatted_start = (start[0:4] + "-" + start[5:7].lstrip("0") + "-" + start[8:10].lstrip("0"))
        formatted_end = (end[0:4] + "-" + end[5:7].lstrip("0") + "-" + end[8:10].lstrip("0"))

        # ------------ Search queries ---------------
        rows = []

        placeholder= '?'
        placeholders= ', '.join(placeholder * len(days_checked))
        print(placeholders)

        # #independent query for dates that works
        # query = """SELECT * FROM general WHERE 
        #             weekday IN (%s)
        #             ORDER BY date
        #             LIMIT 1000""" % placeholders

        # for row in cursor.execute(query, days_checked):
        #     rows.append(row)

        # trial for combined search
        qm = "?"

        query = """SELECT * FROM general WHERE 
                    answer = COALESCE(NULLIF(%s, ''), answer) 
                    AND clue LIKE COALESCE(NULLIF(%s, ''), clue) 
                    AND date >= %s AND date <= %s
                    AND weekday IN (%s)
                    ORDER BY date
                    LIMIT 1000""" % (qm, qm, qm, qm, placeholders)

        for row in cursor.execute(query, [answer, '%' + clue + '%', formatted_start, formatted_end, days_checked]):
            rows.append(row)

        # #original search function that worked before
        # for row in cursor.execute("""SELECT * FROM general WHERE answer = COALESCE(NULLIF(?, ''), answer) 
        #                             AND clue LIKE COALESCE(NULLIF(?, ''), clue) 
        #                             AND (date >= ? AND date <= ?) 
        #                             ORDER BY date
        #                             LIMIT 1000""", [answer, '%' + clue + '%', formatted_start, formatted_end]):
        #     rows.append(row)
        
        #TO DO: add footer in table in html, and have it return X results akin to Google using jinja syntrax in html and count in python
        #TO DO: fix date clause in main SQL query

        return render_template("databased.html", rows = rows, count = len(rows), clue_placeholder = clue, answer_placeholder = answer, days = DAYS)

    else:
        return render_template("database.html", days = DAYS)

#syntax to run app.py
if __name__ == "__main__":
    app.run(debug=True)