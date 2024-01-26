#!usr/bin/env python3
"""Model Holder"""

from config import db, ma

class IBACocktails(db.Model):
    """IBA Copcktails class"""
    __tablename__ = "IBACocktails"
    an_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    method = db.Column(db.Integer)
    garnish = db.Column(db.String)


    def __repr__(self):
        return f"<IBACocktails(name={self.name!r})>"
    
class IBACocktailsSchema(ma.SQLAlchemySchema):
    """IBA Cocktails schema"""
    class Meta:
        """IBA Cocktails metadata"""
        model = IBACocktails
        load_instance = True

    an_id = ma.auto_field()
    category = ma.auto_field()
    name = ma.auto_field()
    ingredients = ma.auto_field()
    method = ma.auto_field()
    garnish = ma.auto_field()