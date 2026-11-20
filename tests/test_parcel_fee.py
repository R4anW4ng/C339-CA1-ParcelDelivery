import pytest

from src.parcel_fee import delivery_fee


# --- correct fee per weight band ---

@pytest.mark.parametrize(
    "weight_grams, expected_fee",
    [
        (1, 500),        # bottom of the light band
        (500, 500),
        (1000, 500),     # top of the light band (inclusive)
        (1001, 1000),   
        (10000, 1000),
        (20000, 1000),  
    ],
)
def test_valid_weight_returns_correct_fee(weight_grams, expected_fee):
    assert delivery_fee(weight_grams) == expected_fee


def test_fee_is_returned_as_int():
    # fee is in whole cents, so float or bool coming back would be a bug
    assert type(delivery_fee(500)) is int


# --- valid int, but outside the accepted weight range ---

@pytest.mark.parametrize(
    "weight_grams",
    [0, -1, -500, 20001, 100000],
)
def test_weight_outside_permitted_range_raises_value_error(weight_grams):
    with pytest.raises(ValueError):
        delivery_fee(weight_grams)


# --- wrong types ---

@pytest.mark.parametrize(
    "weight_grams",
    [
        "500",
        500.0,     # whole-number float is still a float
        500.5,
        None,
        [500],
        True,      # bool subclasses int but shouldn't be accepted
        False,
    ],
)
def test_weight_with_invalid_type_raises_type_error(weight_grams):
    with pytest.raises(TypeError):
        delivery_fee(weight_grams)
