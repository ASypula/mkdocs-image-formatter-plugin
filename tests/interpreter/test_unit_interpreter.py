from image_formatter.interpreter.interpreter import Interpreter
import pytest


def test_given_empty_image_tags_properties_then_interpreter_is_created():
    image_size_tags = {}
    assert Interpreter(image_size_tags).required_properties == {"width", "height"}


def test_given_image_tag_property_when_properties_are_not_dictionaries_then_it_is_not_valid():
    image_size_tags = {"small": "a"}
    assert Interpreter(image_size_tags).are_image_tags_properties_valid(image_size_tags) is False


@pytest.mark.parametrize("properties", [{"small": {"width": "100"}}, {"small": {"a": "100"}}])
def test_given_image_tag_properties_when_properties_do_not_have_required_attributes_then_they_are_not_valid(properties):
    assert Interpreter(properties).are_image_tags_properties_valid(properties) is False


@pytest.mark.parametrize(
    "properties", [{"small": {"width": "100", "height": "100"}}, {"small": {"height": "100", "width": "100"}}]
)
def test_given_image_tags_properties_when_properties_are_valid_then_interpreter_is_created(properties):
    assert Interpreter(properties).are_image_tags_properties_valid(properties) is True


@pytest.mark.parametrize(
    "properties",
    [{"small": {"width": "100", "height": "100", "c": []}}, {"small": {"height": "100", "width": "100", "c": "D"}}],
)
def test_given_image_tags_properties_when_tags_contain_required_properties_and_more_then_interpreter_is_created(
    properties,
):
    assert Interpreter(properties).are_image_tags_properties_valid(properties) is True
