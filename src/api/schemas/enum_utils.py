from enum import Enum


class ActivityLevel(str, Enum):
    sedentary = "sedentary"
    light = "light"
    moderate = "moderate"
    very = "very"


class Silhouette(str, Enum):
    ectomorph = "ectomorph"
    mesomorph = "mesomorph"
    endomorph = "endomorph"


class Role(str, Enum):
    unconfirmed = "unconfirmed"
    user = "user"
    admin = "admin"


class MeasureUnit(str, Enum):
    kilogram = "kg."
    gram = "g."
    liter = "l."
    milliliter = "ml."
    unit = ""


class Preference(str, Enum):
    like = "like"
    dislike = "dislike"
    alergic = "alergic to"


class Category(str, Enum):
    Salad = "Salad"
    Soup = "Soup"
    MainDish = "Main Dish"
    Appetizer = "Appetizer"
    Dessert = "Dessert"
    Snack = "Snack"
    Beverage = "Beverage"
    Breakfast = "Breakfast"
    Brunch = "Brunch"
    SideDish = "Side Dish"
    Pasta = "Pasta"
    Grilled = "Grilled"
    Smoothie = "Smoothie"
    BBQ = "BBQ"
    SlowCooker = "Slow Cooker"
    StirFry = "Stir Fry"
    Fermented = "Fermented"
