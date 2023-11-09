import os
import tempfile
from unittest.mock import patch
import pytest

from mkdocs.structure.files import File
from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig

from image_formatter.image_formatter_plugin.image_formatter_plugin import ImageFormatterPlugin

TEST_DIR = "test"
TEST_FILE = "test.md"
CONFIG_FILE = "config.yml"


@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def image_formatter_plugin(temp_directory):
    def plugin(page, config):
        p = ImageFormatterPlugin()
        p.on_config(config)
        return p.on_page_read_source(page, config)

    return plugin


def test_converts_basic(image_formatter_plugin, temp_directory):
    os.mkdir(os.path.join(temp_directory, TEST_DIR))
    file_path = os.path.join(temp_directory, TEST_DIR, TEST_FILE)
    with open(file_path, "w") as f:
        f.write("some test page")

    page = Page(title="Test", file=File(file_path, temp_directory, temp_directory, False), config={})

    image_sizes = {
        "image_formatter": {
            "large": {
                "width": "100px",
                "height": "50px",
            },
            "small": {
                "width": "80px",
                "height": "40px",
            },
        }
    }

    config = MkDocsConfig()
    config.load_dict(image_sizes)

    image_formatter_plugin(page, config)

    assert True
