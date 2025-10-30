import pytest

from api.metrics.micronutrients_summary import (
    micronutrients_summary,
    scale_micronutrients,
)
from api.schemas.utils import MicronutrientsTotal


def test_micronutrients_summary_adds_all_fields(example_micronutrients_total):
    ingredients = []
    for ingredient in example_micronutrients_total:
        ingredients.append(MicronutrientsTotal(**ingredient))
    total = micronutrients_summary(ingredients)

    assert total == MicronutrientsTotal(
        calories=282.0,
        protein=15.1,
        fat=21.5,
        carbon=8.0,
        fiber=1.2,
        sugar=6.699999999999999,
        salt=2.21,
    )


@pytest.mark.parametrize(
    "measure_unit,expected_amount",
    [
        ("kg.", 1000.0),
        ("l.", 1000.0),
        ("ml.", 100.0),
        ("", 50.0),
        ("g.", 100.0),
    ],
)
def test_scale_micronutrients_all_units(
    measure_unit, expected_amount, example_micronutrients
):
    rho = 1.0
    default_weight = 50.0
    amount = 100.0

    if measure_unit == "ml.":
        expected_amount = amount * rho
    elif measure_unit == "l.":
        expected_amount = 1000.0 * amount * rho
    elif measure_unit == "kg.":
        expected_amount = 1000.0 * amount
    elif measure_unit == "":
        expected_amount = default_weight * amount

    result = scale_micronutrients(
        amount, measure_unit, rho, default_weight, example_micronutrients[0]
    )

    assert isinstance(result, MicronutrientsTotal)
    assert (
        pytest.approx(result.calories, rel=1e-3)
        == example_micronutrients[0]["calories_per_100"] * expected_amount / 100
    )


def test_scale_micronutrients_raises_on_invalid_unit(example_micronutrients):
    with pytest.raises(ValueError):
        scale_micronutrients(100, "unknown.", 1.0, 50.0, example_micronutrients[0])
