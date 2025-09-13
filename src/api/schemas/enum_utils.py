from enum import Enum


"""Activity Options"""


class ActivityLevel(str, Enum):
    sedentary = "sedentary"
    light = "light"
    moderate = "moderate"
    very = "very"


"""Silhouette Options"""


class Silhouette(str, Enum):
    ectomorph = "ectomorph"
    mesomorph = "mesomorph"
    endomorph = "endomorph"


"""Role Options"""


class Role(str, Enum):
    user = "user"
    admin = "admin"


"""Measure Options"""


class MeasureUnit(str, Enum):
    kilogram = "kg."
    gram = "g."
    liter = "l."
    milliliter = "ml."
    unit = ""


"""Preference Options"""


class Preference(str, Enum):
    like = "like"
    dislike = "dislike"
    alergic = "alergic to"
