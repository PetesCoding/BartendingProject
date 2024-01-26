#!usr/bin/env python3

import pathlib
import re

from flask import Flask, render_template, make_response, request, flash, redirect, url_for
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import IBACocktails
from typing import *

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'notsureyet'
CORS(app)

this_dir = pathlib.Path(__file__).parent
engine = create_engine("sqlite:///" + str(
    this_dir/pathlib.Path("iba-cocktails-web.sqlite3")
), pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)

### Parsing Functions

def titlecase(s):
    result = re.sub(r"[A-Za-z]{3,}('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)
    result = re.sub("The", "the", result)
    result = re.sub("And", "and", result)
    return result

def stripList(list):
    strippedList = []
    for i in list:
        joiner = re.split(",", i)
        for j in joiner:
            new = j.replace("ml", "")
            new = re.sub(re.escape("-"), "", new)
            new = re.sub(re.escape("/"), "", new)
            new = re.sub(re.escape("+"), "", new)
            new = re.sub(re.escape("("), "", new)
            new = re.sub(re.escape(")"), "", new)
            new = new.replace("  ", "")
            new = new.replace("Fresh ", "")
            new = new.replace(" or Rye Whiskey", " Whiskey")
            new = new.replace(" or Prosecco", "")
            new = new.replace(" or Bourbon", "")
            new = new.replace(" or Malbech", "")
            new = new.replace("A pinch of ", "")
            new = new.replace("A pinch ", "")
            new = new.replace("dashes", "")
            new = new.replace("Dashes", "")
            new = new.replace("Dash of ", "")
            new = new.replace("Dash ", "")
            new = new.replace("dash ", "")
            new = new.replace("A dash of ", "")
            new = new.replace("A of ", "")
            new = new.replace("Bar Spoon ", "")
            new = new.replace("Bar Spoons ", "")
            new = new.replace("Table Spoon ", "")
            new = new.replace("drops ", "")
            new = new.replace("Drops ", "")
            new = new.replace("teaspoon ", "")
            new = new.replace("teaspoons ", "")
            new = new.replace("Teaspoons ", "")
            new = new.replace("quarter size ", "")
            new = new.replace("quarter size Sliced ", "")
            new = new.replace("Fill up with ", "")
            new = new.replace("Top with ", "")
            new = new.replace("Top up with ", "")
            new = new.replace("Top up ", "")
            new = new.replace("Splash ", "")
            new = new.replace("A splash ", "")
            new = new.replace("% ", "")
            new = new.replace(".", "")
            new = new.replace("tsp ", "")
            new = new.replace("pcs ", "")
            new = new.replace("strong ", "")
            new = new.replace("/ Bar Spoon ", "")
            new = new.replace("/ Bar Spoon of", "")
            new = new.replace("/ pcs ", "")
            new = new.replace("/ ", "")
            new = new.replace(" Up to taste", "")
            new = new.replace(" optional", "")
            new = new.replace(" Optional", "")
            new = new.replace(" replace water with chamomile", "")
            new = new.replace("Few Drops of ", "")
            new = new.replace(" cut into small wedges", "")
            new = new.replace("Few of ", "")
            new = new.replace("thin Slices ", "")
            new = new.replace(" Green", "")
            new = new.replace(" White", "")
            new = new.replace(" Brown", "")
            new = new.replace("of ", "")
            new = re.sub(r'[0-9]', "", new)
            new = new.replace(" Water Agave Nectar", "")
            new = new.strip()
            if titlecase(new) not in strippedList:
                strippedList.append(titlecase(new))
                
    strippedList.sort()
    return strippedList
    
    
    
### Path Functions

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/cocktaillist")
def cocktaillist():
    session = Session()
    query = session.query(IBACocktails)
    iba_cocktails = query.all()

    iba_cocktails_list = [
        {
            "Category": cocktail.category,
            "Name": cocktail.name,
            "Ingredients": cocktail.ingredients,
            "Method": cocktail.method,
            "Garnish": cocktail.garnish
        }

        for cocktail in iba_cocktails
    ]
    
    iba_cocktails_list = sorted(iba_cocktails_list, key = lambda k : k["Name"] )

    return render_template("index.html", cocktails=iba_cocktails_list)


@app.route("/bar", methods=("GET", "POST"))
def bar():
    bar = []
    session = Session()
    query = session.query(IBACocktails)
    iba_cocktails = query.all()
    
    iba_cocktails_list = [
        {
            "Name": cocktail.name,
            "Ingredients": cocktail.ingredients
        }

        for cocktail in iba_cocktails
    ]
    
    if request.method == "POST":
        ingredient = request.form["bar-ingredient"]
        ingredients = re.split(", ", request.cookies.get("ingredient"))
        
        if len(ingredients) == 1:
            resp = make_response(render_template("bar.html"))
            resp.set_cookie("ingredient", "", expires=0)
            return resp
        
        for i in iba_cocktails_list:
            counter = 0
            holder = []
            cocktailHolder = stripList(re.split(",", i["Ingredients"]))
            length = len(cocktailHolder)
            for j in cocktailHolder:
                if j in ingredients:
                    counter += 1
                    holder.append(j)
            if counter == length:
                bar.append(i["Name"])
        
        ingredients.remove(ingredient)
        resp = make_response(render_template("bar.html", ingredients=ingredients, cocktails=bar))
        resp.set_cookie("ingredient", ", ".join(ingredients))
        return resp
        
    if "ingredient" in request.cookies:
        ingredients = re.split(", ", request.cookies.get("ingredient"))
        
        for i in iba_cocktails_list:
            counter = 0
            holder = []
            cocktailHolder = stripList(re.split(",", i["Ingredients"]))
            length = len(cocktailHolder)
            for j in cocktailHolder:
                if j in ingredients:
                    counter += 1
                    holder.append(j)
            if counter == length:
                bar.append(i["Name"])
                    
        return render_template("bar.html", ingredients=ingredients, cocktails=bar)
    
    else:
        return render_template("bar.html")


@app.route("/ingredients", methods=('GET', 'POST'))
def ingredients():
    title = ""
    session = Session()
    query = session.query(IBACocktails)
    iba_cocktails = query.all()
    iba_cocktails_list = []

    for cocktail in iba_cocktails:
        iba_cocktails_list.append(cocktail.ingredients)
    
    ingredients = stripList(iba_cocktails_list)
    
    if request.method == "POST":
        if request.form["ingredient-search"] != "None":
            title = request.form["ingredient-search"]
            title = titlecase(title)
            
            if title == None:
                warning = ["Must provide an ingredient"]
                render_template("ingredients.html", ingredients=ingredients, warning=warning)
            
            if title in ingredients:
                return redirect(f"/ingredients#{title}")
            else:
                return redirect("/ingredients")
        
        elif request.form["ingredient-search"] == "None":
            
            if "ingredient" in request.cookies:
                ourIngredient = request.cookies.get("ingredient")
                ingredientToMove = request.form["ingredient-cookie"]
                
                if ingredientToMove in re.split(", ", ourIngredient):
                    warning = ["Ingredient already in bar"]
                    return render_template("ingredients.html", ingredients=ingredients, warning=warning)
                
                else:
                    ingredientToMove = f"{ourIngredient}, {ingredientToMove}"
                    resp = make_response(render_template("ingredients.html", ingredients=ingredients))
                    resp.set_cookie("ingredient", ingredientToMove)
                    return resp
            
            else:
                ingredientToMove = request.form["ingredient-cookie"]
                resp = make_response(render_template("ingredients.html", ingredients=ingredients))
                resp.set_cookie("ingredient", ingredientToMove)
                return resp
    
    return render_template("ingredients.html", ingredients=ingredients)


@app.route("/barcocktails", defaults={"cocktail": None})
@app.route("/barcocktails/<string:cocktail>")

@app.route("/cocktails", defaults={"cocktail": None})
@app.route("/cocktails/<string:cocktail>")
def cocktails(cocktail):

    if cocktail:
        session = Session()

        query = session.query(IBACocktails)
        query = query.filter_by(name=cocktail)
        iba_cocktails = query.all()

        iba_cocktails_list = [
            {
                "Category": cocktail.category,
                "Name": cocktail.name,
                "Ingredients": cocktail.ingredients,
                "Method": cocktail.method,
                "Garnish": cocktail.garnish
            }

            for cocktail in iba_cocktails
        ]
        
        cocktail_ingredients = re.split(", |,|\. ", iba_cocktails_list[0]["Ingredients"])
        cocktail_ingredients = [titlecase(ingredient.replace("NA", "")) for ingredient in cocktail_ingredients]
        
        cocktail_method = re.split(", |,|\. ", iba_cocktails_list[0]["Method"])
        cocktail_method = [titlecase(method.replace(".", "")) for method in cocktail_method]
        
        cocktail_garnish = iba_cocktails_list[0]["Garnish"]
        cocktail_garnish = titlecase(cocktail_garnish.replace(".", ""))

        if request.path == f"/barcocktails/{cocktail}":
            return render_template("bar-cocktails.html",
                                cocktails=iba_cocktails_list,
                               ingredients=cocktail_ingredients,
                               method=cocktail_method,
                               garnish=cocktail_garnish)
        else: 
            return render_template("cocktails.html",
                               cocktails=iba_cocktails_list,
                               ingredients=cocktail_ingredients,
                               method=cocktail_method,
                               garnish=cocktail_garnish)
    
    else:
        return render_template("cocktails.html")


@app.route("/popular")
def popular():
    return render_template("popular.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=3000, debug=True)