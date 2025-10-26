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
    salad = "Salad"
    soup = "Soup"
    main_dish = "Main Dish"
    appetizer = "Appetizer"
    dessert = "Dessert"
    snack = "Snack"
    beverage = "Beverage"
    breakfast = "Breakfast"
    brunch = "Brunch"
    side_dish = "Side Dish"
    pasta = "Pasta"
    grilled = "Grilled"
    smoothie = "Smoothie"
    bbq = "BBQ"
    slow_cooker = "Slow Cooker"
    stir_fry = "Stir Fry"
    fermented = "Fermented"
