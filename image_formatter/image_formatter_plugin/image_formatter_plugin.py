"""
Main plugin file, contains logic for validating user-defined configuration and plugin events
"""

import mkdocs
import mkdocs.config.base
import mkdocs.config.config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
import mkdocs.plugins
import cssutils
import logging
from typing import Tuple
from image_formatter.lexer.lexer import Lexer
from image_formatter.image_properties_tag_replacer.image_properties_tag_replacer import ImagePropertiesTagReplacer

WIDTH = "width"
HEIGHT = "height"

logger = logging.getLogger("mkdocs.plugins")


def log_and_raise_validation_error(error_message: str) -> None:
    logger.error(error_message)
    raise mkdocs.config.base.ValidationError(error_message)


def validate_dimensions(dimensions: Tuple[str, str]) -> None:
    """Validates if dimensions are valid in CSS form"""
    if len(dimensions) != 2:
        log_and_raise_validation_error(f"Expected 2 elements in tuple but {len(dimensions)} provided")
    dimension, units = dimensions
    style = cssutils.parseStyle(f"{dimension}: {units};")
    if not style.valid:
        log_and_raise_validation_error(f"provided invalid dimensions: {dimensions}")


class ImageFormatterConfig(mkdocs.config.base.Config):
    image_size = mkdocs.config.config_options.Type(dict, default={})


class ImageFormatterPlugin(mkdocs.plugins.BasePlugin[ImageFormatterConfig]):
    """Main plugin class, defines what should happen in each plugin event"""

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig or None:
        """
        Verifies if tags are defined correctly. Each tag should specify width and height in valid CSS form.
        """
        size_tags = self.config["image_size"]
        for tag, options in size_tags.items():
            if WIDTH not in options or HEIGHT not in options:
                raise mkdocs.config.base.ValidationError(f"width or height is missing from {tag} tag configuration")

            validate_dimensions((WIDTH, options[WIDTH]))
            validate_dimensions((HEIGHT, options[HEIGHT]))

        logger.info("configuration validation finished successfully")
        return config

    def on_page_read_source(self, page: Page, config: MkDocsConfig) -> str or None:
        # todo: using lexer, image_properties_tag_replacer and interpreter read user's docs and apply sizes specified in tags
        src_path = page.file.abs_src_path
        # with open(src_path) as fp:
        #     with open("test.txt", "w+") as t:
        #         lexer = Lexer(fp)
        #         lexer.next_char()
        #         tags_replacer = ImagePropertiesTagReplacer(lexer, self.config["image_size"])
        #         for link in tags_replacer.get_token():
        #             t.write(link.string)
