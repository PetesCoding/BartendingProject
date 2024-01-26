import re

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

iba_cocktails_list = [
    {
    "Category": "Contemporary Classics",
    "Garnish": "NA",
    "Ingredients": "50 ml Vodka,20 ml Coffee Liqueur",
    "Method": "Pour the ingredients into the old fashioned glass filled with ice cubes. Stir gently.  Note: WHITE RUSSIAN - Float fresh cream on the top and stir in slowly.",
    "Name": "Black Russian"
    },
    {
    "Category": "Contemporary Classics",
    "Garnish": "NA",
    "Ingredients": "60 ml Cacha\u00e7a,1 Lime cut into small wedges,4 Teaspoons White Cane Sugar",
    "Method": "Place lime and sugar into a double old fashioned glass and muddle gently. Fill the glass with cracked ice and add Cacha\u00e7a. Stir gently to involve ingredients. Note: CAIPIROSKA - Instead of Cacha\u00e7a use Vodka;",
    "Name": "Caipirinha"
  },
    {
    "Category": "The Unforgettables",
    "Garnish": "Squeeze oil from lemon peel onto the drink, or garnish with green olives if requested.",
    "Ingredients": "60 ml Gin,10 ml Dry Vermouth",
    "Method": "Pour all ingredients into mixing glass with ice cubes. Stir well. Strain into chilled martini cocktail glass.",
    "Name": "Dry Martini"
  }
]

ingredients = ["Gin", "Dry Vermouth"]

bar = []

for i in iba_cocktails_list:
    counter = 0
    holder = []
    cocktailHolder = re.split(",", i["Ingredients"])
    cocktailHolder = stripList(cocktailHolder)
    length = len(cocktailHolder)
    for j in cocktailHolder:
        if j in ingredients:
            counter += 1
            holder.append(j)
    if counter == length:
        bar.append(i["Name"])
                    
print(bar)
