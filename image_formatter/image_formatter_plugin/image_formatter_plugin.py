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

WIDTH = "width"
HEIGHT = "height"

logger = logging.getLogger("mkdocs.plugins")


def validate_dimentions(dimentions: str) -> None:
    """Validates if dimentions are valid in CSS form"""
    style = cssutils.parseStyle(f"width: {dimentions};")
    if not style.valid or len(dimentions) == 0:
        err_msg = f"provided invalid dimensions: {dimentions}"
        logger.error(err_msg)
        raise mkdocs.config.base.ValidationError(err_msg)


class ImageFormatterConfig(mkdocs.config.base.Config):
    image_size = mkdocs.config.config_options.Type(dict, default={})


class ImageFormatterPlugin(mkdocs.plugins.BasePlugin[ImageFormatterConfig]):
    """Main plugin class, defines what shuld happen in each plugin event"""

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        """
        Verifies if tags are defined correctly. Each tag should specify width and height in vaild CSS form.
        """
        size_tags = config["image_size"]
        for tag, options in size_tags.items():
            if WIDTH not in options or HEIGHT not in options:
                raise mkdocs.config.base.ValidationError(f"width or height is missing from {tag} tag configuration")

            validate_dimentions(options[WIDTH])
            validate_dimentions(options[HEIGHT])

        logger.info("configuration validation finished successfully")
        return config

    def on_page_read_source(self, page: Page, config: MkDocsConfig) -> str | None:
        # todo: using lexer, parser and interpreter read user's docs and apply sizes specified in tags

        pass
