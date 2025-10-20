import pytest


@pytest.fixture
def example_micronutrients():
    return [
        {
            "calories_per_100": 18.0,
            "protein_per_100": 0.9,
            "fat_per_100": 0.2,
            "carbon_per_100": 3.9,
            "fiber_per_100": 1.2,
            "sugar_per_100": 2.6,
            "salt_per_100": 0.01,
        },
        {
            "calories_per_100": 264.0,
            "protein_per_100": 14.2,
            "fat_per_100": 21.3,
            "carbon_per_100": 4.1,
            "sugar_per_100": 4.1,
            "salt_per_100": 2.2,
        },
    ]


@pytest.fixture
def example_micronutrients_total():
    return [
        {
            "calories": 18.0,
            "protein": 0.9,
            "fat": 0.2,
            "carbon": 3.9,
            "fiber": 1.2,
            "sugar": 2.6,
            "salt": 0.01,
        },
        {
            "calories": 264.0,
            "protein": 14.2,
            "fat": 21.3,
            "carbon": 4.1,
            "sugar": 4.1,
            "salt": 2.2,
        },
    ]
