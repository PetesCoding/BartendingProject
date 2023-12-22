#!usr/bin/env python3

import werkzeug
import pathlib
import re

from flask_bcrypt import Bcrypt
from logging.config import dictConfig
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify, json
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import IBACocktails


###
### Title Capitalize Regex Function
###

def titlecase(s):
    result = re.sub(r"[A-Za-z]{3,}('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)
    result = re.sub("The", "the", result)
    result = re.sub("And", "and", result)
    return result

# https://python.land/string-to-title-case

###
### Create App
###

app = Flask(__name__)

# CORS Initialization
CORS(app)

# Encryption Initialization
bcrypt = Bcrypt(app)

###
### Configure Logger
###

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

###
### Initialize SQLAlchemy Engine
###

this_dir = pathlib.Path(__file__).parent
engine = create_engine("sqlite:///" + str(
    this_dir/pathlib.Path("iba-cocktails-web.sqlite3")
))
Session = sessionmaker(bind=engine)


###
### API Get Functionality
###


@app.route("/cocktails", defaults={"cocktail": None})
@app.route("/cocktails/<string:cocktail>")
def getCocktails(cocktail):
    session = Session()

    try:
        query = session.query(IBACocktails)

        if cocktail:
                if cocktail.casefold() == "kir":
                    cocktail = "KIR"

                elif cocktail.casefold() == "dark 'n' stormy"\
                    or cocktail.casefold() == "dark n stormy"\
                    or cocktail.casefold() == "dark n' stormy"\
                    or cocktail.casefold() == "dark 'n stormy":
                    cocktail = "Dark 'n' stormy"

                elif cocktail.casefold() == "lemon drop martini":
                    cocktail = "Lemon drop Martini"

                elif cocktail.casefold() == "ve.n.to":
                    cocktail = "VE.N.TO"

                elif cocktail.casefold() == "vieux carre":
                    cocktail = "Vieux Carrè"

                else:
                    cocktail = titlecase(cocktail)
                query = query.filter_by(name=cocktail)

                # Can't get "Corpse Reviver #2" to work

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

        response = jsonify(iba_cocktails_list)
        return response
    
    except:
        ErrorHandler = {"Error": "Found"}
        return jsonify(ErrorHandler)

    finally:
        session.close()


###
### Select Functions
###

# Find all categories of the Cocktails
@app.route("/categories")
def getCategories():

    try:
        session = Session()

        iba_categories_list = [
            {
                "Category": distinctCategory.category
            }

            for distinctCategory in session.query(IBACocktails.category).distinct()
        ]

        response = jsonify(iba_categories_list)
        return response

    except:
        ErrorHandler = {"Error": "Found"}
        return jsonify(ErrorHandler)

    finally:
        session.close()

# Filter the cocktails by spirit
@app.route("/ingredients", defaults={"ingredient": None})
@app.route("/ingredients/<string:ingredient>")
def getNameBySpirit(ingredient):
    session = Session()
    query = session.query(IBACocktails)

    try:
        spiritNames = query.all()

        if ingredient:
            ingredient = titlecase(ingredient)

            iba_cocktail_by_spirit_list = []

            for cocktail in spiritNames:
                if f"{ingredient}" in cocktail.ingredients:
                    iba_cocktail_by_spirit_list.append(
                        {
                            "Name": cocktail.name,
                            "Ingredients": cocktail.ingredients
                        })

            response = jsonify(iba_cocktail_by_spirit_list)
            return response
        
        else:
            iba_cocktail_by_spirit_list = [
                {
                    "Name": cocktail.name,
                    "Ingredients": cocktail.ingredients
                }
                for cocktail in spiritNames
            ]

            response = jsonify(iba_cocktail_by_spirit_list)
            return response

    except:
        ErrorHandler = {"Error": "Found"}
        return jsonify(ErrorHandler)

    finally:
        session.close()

###
### Error Handler
###

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_BadRequest(e):
    ErrorHandler = {
        "Error": "Found",
        "ErrorHandler": f"{e}"
    }

    return jsonify(ErrorHandler)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "Error Code": e.code,
        "Error Name": e.name,
        "Error Description": e.description,
    })

    response.content_type = "application/json"
    return response


###
### Run
###

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=3000, debug=True)