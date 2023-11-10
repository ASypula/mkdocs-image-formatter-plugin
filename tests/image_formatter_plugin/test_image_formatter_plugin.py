import pytest
import mkdocs.config.base
from image_formatter.image_formatter_plugin.image_formatter_plugin import (
    validate_dimensions,
)


# validate dimensions test
def test_given_valid_dimensions_when_validating_then_no_exception_raised():
    valid_dimensions = ("height", "100px")
    validate_dimensions(valid_dimensions)


def test_given_invalid_units_when_validating_then_exception_raised():
    invalid_dimensions = ("width", "invalid")
    with pytest.raises(mkdocs.config.base.ValidationError) as err:
        validate_dimensions(invalid_dimensions)
    assert str(err.value) == "provided invalid dimensions: ('width', 'invalid')"


def test_given_invalid_dimension_when_validating_then_exception_raised():
    invalid_dimensions = ("invalid", "10px")
    with pytest.raises(mkdocs.config.base.ValidationError) as err:
        validate_dimensions(invalid_dimensions)
    assert str(err.value) == "provided invalid dimensions: ('invalid', '10px')"


def test_given_empty_string_when_validating_then_exception_raised():
    empty_dimensions = ()
    with pytest.raises(mkdocs.config.base.ValidationError) as err:
        validate_dimensions(empty_dimensions)
    assert str(err.value) == "Expected 2 elements in tuple but 0 provided"


def test_given_valid_multiple_dimensions_when_validating_then_exception_raised():
    multiple_dimensions = ("width", "100px 200px")
    with pytest.raises(mkdocs.config.base.ValidationError) as err:
        validate_dimensions(multiple_dimensions)
    assert str(err.value) == "provided invalid dimensions: ('width', '100px 200px')"
