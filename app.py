from datetime import datetime, date
import random
import os
from pymongo import MongoClient

from flask import Flask
from flask import render_template

app = Flask(__name__)


def isWeekend(date):
    if date.weekday() == 5 or date.weekday() == 6:
        return True
    else:
        return False


def fuckShitUp(s):
    # Divide into words
    words = s.split(' ')
    # Pick a random spot to insert the fucking
    n = random.randint(0, len(words)-1)
    s = ' '.join(words[:n]) + ' Fucking ' + ' '.join(words[n:])
    return s

# Needed so we can use in the jinja templates
app.jinja_env.globals.update(isWeekend=isWeekend)
app.jinja_env.globals.update(fuckShitUp=fuckShitUp)

uri = os.environ.get('MONGODB_URI')

client = MongoClient(uri)
db = client.heroku_80660qwq

today = datetime.today()

menus = db.weeklymenus.find_one({"Date": datetime.combine(date.today(), datetime.min.time())})
if menus is None:
    menus = {"Breakfast": [], "Lunch": [], "Dinner": []}
print(menus)


@app.route('/')
def showIndexPage():
    if isWeekend(today):
        if 3 <= today.hour <= 10:
            menu = menus["Breakfast"]
        elif 10 < today.hour <= 12+2:
            menu = menus["Lunch"]
        else:
            menu = menus["Dinner"]
    else:
        if 3 <= today.hour <= 12+2:
            menu = menus["Lunch"]
        else:
            menu = menus["Dinner"]

    # dinner
    return render_template('main.html', menu=menu, today=today)


@app.route('/breakfast')
def showBreakfastPage():
    if not isWeekend(today):
        menu = menus["Breakfast"]
        return render_template('main.html', menu=menu, today=today)
    else:
        failText = "There's no breakfast on the weekend, motherfucker."
        return render_template('fail.html',
                               failText=failText,
                               today=today)


@app.route('/brunch')
def showBrunchPage():
    if isWeekend(today):
        menu = menus["Lunch"]
        return render_template('main.html', menu=menu, today=today)
    else:
        failText = "There's no brunch on weekdays, motherfucker."
        return render_template('fail.html',
                               failText=failText,
                               today=today)


@app.route('/lunch')
def showLunchPage():
    if not isWeekend(today):
        menu = menus["Lunch"]
        return render_template('main.html', menu=menu, today=today)
    else:
        failText = "There's no lunch on the weekend, motherfucker."
        return render_template('fail.html', failText=failText,
                               today=today)

    menu = menus["Lunch"]
    return render_template('main.html', menu=menu, today=today)


@app.route('/dinner')
def showDinnerPage():
    menu = menus["Dinner"]
    return render_template('main.html', menu=menu, today=today)


if __name__ == "__main__":
    app.run()
