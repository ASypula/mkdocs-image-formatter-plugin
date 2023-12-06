from setuptools import setup, find_packages

setup(
    name="mkdocs-image-formatter-plugin",
    description="MkDocs plugin for managing image sizes",
    packages=find_packages(),
    install_requires=["mkdocs>=1.0"],
    version="1.0.0",
    entry_points={
        "mkdocs.plugins": [
            "image-formatter = image_formatter.image_formatter_plugin.image_formatter_plugin:ImageFormatterPlugin",
        ]
    },
)
