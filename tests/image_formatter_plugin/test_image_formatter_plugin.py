import pytest
import mkdocs.config.base
from image_formatter.image_formatter_plugin.image_formatter_plugin import (
    validate_dimentions,
)


# validate dimentions test
def test_given_valid_dimensions_when_validating_then_no_exception_raised():
    valid_dimensions = "100px"
    validate_dimentions(valid_dimensions)


def test_given_invalid_dimensions_when_validating_then_exception_raised():
    invalid_dimensions = "invalid"
    with pytest.raises(mkdocs.config.base.ValidationError) as err:
        validate_dimentions(invalid_dimensions)
    assert str(err.value) == "provided invalid dimensions: invalid"


def test_given_empty_string_when_validating_then_exception_raised():
    empty_dimensions = ""
    with pytest.raises(mkdocs.config.base.ValidationError) as err:
        validate_dimentions(empty_dimensions)
    assert str(err.value) == "provided invalid dimensions: "


def test_given_valid_multiple_dimensions_when_validating_then_exception_raised():
    multiple_dimensions = "100px 200px"
    with pytest.raises(mkdocs.config.base.ValidationError) as err:
        validate_dimentions(multiple_dimensions)
    assert str(err.value) == "provided invalid dimensions: 100px 200px"
