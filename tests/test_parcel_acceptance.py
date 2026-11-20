import pytest

from src.parcel_acceptance import is_parcel_accepted


# --- happy path ---

@pytest.mark.parametrize(
    "weight_grams, length_cm",
    [
        (1, 1),          # smallest valid parcel
        (10000, 100),    # typical mid-range
        (20000, 1),      # max weight
        (1, 200),        # max length
        (20000, 200),    # both at the edge
    ],
)
def test_parcel_within_both_limits_is_accepted(weight_grams, length_cm):
    assert is_parcel_accepted(weight_grams, length_cm) is True


# --- out-of-range values should be rejected ---

@pytest.mark.parametrize(
    "weight_grams, length_cm",
    [
        (0, 100),        # zero is not a valid weight
        (100, 0),        # zero is not a valid length
        (0, 0),
        (20001, 100),    # one gram over the weight limit
        (100, 201),      # one cm over the length limit
        (20001, 201),    # both over
        (100000, 100),
        (100, 1000),
        (0, 201),
    ],
)
def test_parcel_outside_a_limit_is_rejected(weight_grams, length_cm):
    assert is_parcel_accepted(weight_grams, length_cm) is False


def test_result_is_a_python_bool():
    assert type(is_parcel_accepted(100, 100)) is bool
    assert type(is_parcel_accepted(0, 100)) is bool


# --- negative inputs are physically impossible, so raise ValueError ---

@pytest.mark.parametrize(
    "weight_grams, length_cm",
    [
        (-1, 100),
        (100, -1),
        (-1, -1),
        (-500, 100),
        (100, -500),
        (0, -1),
        (-1, 201),
    ],
)
def test_negative_measurement_raises_value_error(weight_grams, length_cm):
    with pytest.raises(ValueError):
        is_parcel_accepted(weight_grams, length_cm)


# --- wrong types: floats, strings, bools, None, etc. ---

@pytest.mark.parametrize(
    "weight_grams, length_cm",
    [
        ("100", 100),
        (100, "100"),
        (100.5, 100),
        (100, 100.5),
        (100.0, 100),    # whole-number float is still a float
        (100, 100.0),
        (None, 100),
        (100, None),
        (True, 100),     # bool subclasses int but shouldn't be accepted
        (100, True),
        (False, 100),
        (100, False),
        ([100], 100),
        (100, [100]),
    ],
)
def test_invalid_argument_type_raises_type_error(weight_grams, length_cm):
    with pytest.raises(TypeError):
        is_parcel_accepted(weight_grams, length_cm)
