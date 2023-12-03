import shutil
import os
from mkdocs.tests.base import load_config
import pytest
import re

"""
Note that pytest offers a `tmp_path`.
You can reproduce locally with

```python
%load_ext autoreload
%autoreload 2
import os
import tempfile
import shutil
from pathlib import Path
tmp_path = Path(tempfile.gettempdir()) / 'pytest-table-builder'
if os.path.exists(tmp_path):
    shutil.rmtree(tmp_path)
os.mkdir(tmp_path)
```
"""

import re
import os
import shutil
import logging
from click.testing import CliRunner
from mkdocs.__main__ import build_command


# Adapted from https://github.com/timvink/mkdocs-table-reader-plugin/blame/master/tests/test_build.py
def setup_clean_mkdocs_folder(mkdocs_yml_path, output_path):
    """
    Sets up a clean mkdocs directory

    outputpath/testproject
    ├── docs/
    └── mkdocs.yml

    Args:
        mkdocs_yml_path (Path): Path of mkdocs.yml file to use
        output_path (Path): Path of folder in which to create mkdocs project

    Returns:
        testproject_path (Path): Path to test project

    Original code by timvink
    """

    testproject_path = output_path / "testproject"

    # Create empty 'testproject' folder
    if os.path.exists(testproject_path):
        logging.warning(
            """This command does not work on windows.
        Refactor your test to use setup_clean_mkdocs_folder() only once"""
        )
        shutil.rmtree(testproject_path)

    # Copy correct mkdocs.yml file and our test 'docs/'
    shutil.copytree(
        os.path.join(os.path.dirname(mkdocs_yml_path), "docs"),
        testproject_path / "docs",
    )
    if os.path.exists(os.path.join(os.path.dirname(mkdocs_yml_path), "assets")):
        shutil.copytree(
            os.path.join(os.path.dirname(mkdocs_yml_path), "assets"),
            testproject_path / "assets",
        )
    shutil.copyfile(mkdocs_yml_path, testproject_path / "mkdocs.yml")

    return testproject_path


def build_docs_setup(testproject_path):
    """
    Runs the `mkdocs build` command

    Args:
        testproject_path (Path): Path to test project

    Returns:
        command: Object with results of command

    Original code by timvink
    """

    cwd = os.getcwd()
    os.chdir(testproject_path)

    try:
        run = CliRunner().invoke(build_command)
        os.chdir(cwd)
        return run
    except:
        os.chdir(cwd)
        raise


def test_given_tags_in_config_then_changes_image_styling(tmp_path):
    tmp_proj = setup_clean_mkdocs_folder("./resources/e2e_test_files/test_project/mkdocs.yml", tmp_path)

    build_docs_setup(tmp_proj)

    page_path = tmp_proj / "site/index.html"
    contents = page_path.read_text()
    assert re.search(r'<img alt="Persian Cat" src="img/Persialainen.jpg" style="height:100px;width:100px" />', contents)
    assert re.search(
        r'<img alt="Siamese Cat" src="img/Siam_lilacpoint.jpg" style="height:200px;width:200px" />', contents
    )
    assert re.search(r'<img alt="Maine Coon" src="img/Maine_coon.jpg" style="height:100px;width:100px" />', contents)


def test_given_unknown_tags_in_config_then_no_styling_applied(tmp_path):
    tmp_proj = setup_clean_mkdocs_folder("./resources/e2e_test_files/test_project_unknown_tags/mkdocs.yml", tmp_path)

    build_docs_setup(tmp_proj)

    page_path = tmp_proj / "site/index.html"
    contents = page_path.read_text()
    assert re.search(r'<img alt="Persian Cat" src="img/Persialainen.jpg" />', contents)
    assert re.search(
        r'<img alt="Siamese Cat" src="img/Siam_lilacpoint.jpg" style="height:200px;width:200px" />', contents
    )
    assert re.search(r'<img alt="Maine Coon" src="img/Maine_coon.jpg" />', contents)
