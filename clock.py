from apscheduler.schedulers.blocking import BlockingScheduler

from parse import Meal
from parse import MenuParser

import datetime
import json

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=0, minute=0,
                     second=0, timezone='America/Los_Angeles')
def timed_job():
    shouldGetNutrition = False
    currentDate = datetime.datetime.today()
    dateString = currentDate.strftime('./menus/%Y-%m-%d')

    menus = {"Breakfast": [], "Lunch": [], "Dinner": []}

    # breakfast
    menu = MenuParser(currentDate, Meal.breakfast).getMenus(shouldGetNutrition)
    if menu is not None:
        menus["Breakfast"] = menu

    # lunch
    menu = MenuParser(currentDate, Meal.lunch).getMenus(shouldGetNutrition)
    if menu is not None:
        menus["Lunch"] = menu

    # dinner
    menu = MenuParser(currentDate, Meal.dinner).getMenus(shouldGetNutrition)
    if menu is not None:
        menus["Dinner"] = menu

    menuJSON = json.dumps(menus, separators=(',',':'))

    file = open(dateString, "w")
    file.write(menuJSON)
    file.close()

    print(menuJSON)

sched.start()
