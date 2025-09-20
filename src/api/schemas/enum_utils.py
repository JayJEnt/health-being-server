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
