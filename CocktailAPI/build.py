#!usr/bin/env python3
"""Build Database"""

import csv
import pathlib

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

from model import IBACocktails

this_dir = pathlib.Path(__file__).parent
engine = sa.create_engine(f"sqlite:///{this_dir}/iba-cocktails-web.sqlite3")
session = scoped_session(sessionmaker(bind=engine))

def init_db(filename: str):
    """Initialize the database"""
    if pathlib.Path(f"{this_dir}/{filename}.sqlite3").exists():
        pathlib.Path(f"{this_dir}/{filename}.sqlite3").unlink()

    IBACocktails.metadata.create_all(engine)

    with open(f"{this_dir}/{filename}.csv", "r", encoding="utf8") as connection:
        list = csv.DictReader(connection)

        for item in list:

            _IBACocktails = IBACocktails(
                category=item["category"],
                name=item["name"],
                ingredients=item["ingredients"],
                method=item["method"],
                garnish=item["garnish"],
            )
            session.add(_IBACocktails)
            
        session.commit()

def main():
    init_db("iba-cocktails-web")

if __name__ == "__main__":
    main()