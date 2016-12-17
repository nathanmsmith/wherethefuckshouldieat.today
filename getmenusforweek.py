from pymongo import MongoClient
from datetime import datetime, date, timedelta
from parse import Meal
from parse import MenuParser

import pprint

if __name__ == "__main__":

    today = date.today()
    shouldGetNutrition = False

    client = MongoClient('localhost', 27017)
    db = client.menus
    weeklymenus = db.weeklymenus

    for i in range(0, 7):
        dateTime = datetime.combine(today + timedelta(days=i), datetime.min.time())
        # Overwrite old entry if need be
        weeklymenus.find_one_and_delete({"Date": dateTime})

        menus = {"Date": dateTime, "Breakfast": [], "Lunch": [], "Dinner": []}

        # breakfast
        meal = Meal.breakfast
        parser = MenuParser(date, meal)
        menu = parser.getMenus(shouldGetNutrition)
        if menu is not None:
            menus["Breakfast"] = menu

        # lunch
        meal = Meal.lunch
        parser = MenuParser(date, meal)
        menu = parser.getMenus(shouldGetNutrition)
        if menu is not None:
            menus["Lunch"] = menu

        # dinner
        meal = Meal.dinner
        parser = MenuParser(date, meal)
        menu = parser.getMenus(shouldGetNutrition)
        if menu is not None:
            menus["Dinner"] = menu

        id = weeklymenus.insert_one(menus).inserted_id
        pprint.pprint(weeklymenus.find_one({"_id": id}))
