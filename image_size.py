"""
Main plugin file, contains logic for validating user-defined configuration and plugin events
"""

import mkdocs
import cssutils

WIDTH = "width"
HEIGHT = "height"


def validate_dimentions(dimentions: str) -> None:
    """Validates if dimentions are valid in CSS form"""
    try:
        cssutils.parseStyle(f"width: {dimentions};")
    except Exception as e:
        raise mkdocs.config.base.ValidationError(
            f"provided invalid dimentions: {dimentions}"
        )


class ImageSizeConfig(mkdocs.config.base.Config):
    image_size = mkdocs.config.config_options.Type(dict, default={})


class ImageSizePlugin(mkdocs.plugins.BasePlugin[ImageSizeConfig]):
    """Main plugin class, defines what shuld happen in each plugin event"""

    def on_config(self, config: dict) -> dict:
        """
        Verifies if tags are defined correctly. Each tag should specify width and height in vaild CSS form.
        """
        size_tags = config["image_size"]
        for tag, options in size_tags.items():
            if WIDTH not in options or HEIGHT not in options:
                raise mkdocs.config.base.ValidationError(
                    f"width or height is missing from {tag} tag configuration"
                )

            validate_dimentions(options[WIDTH])
            validate_dimentions(options[HEIGHT])

        return config

    def on_page_read_source() -> str | None:
        # todo: using lexer, parser and interpreter read user's docs and apply sizes specified in tags
        pass
