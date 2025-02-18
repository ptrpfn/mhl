"""
__author__ = "Patrick Renner"
__copyright__ = "Copyright 2020, Pomfort GmbH"

__license__ = "MIT"
__maintainer__ = "Patrick Renner, Alexander Sahm"
__email__ = "opensource@pomfort.com"
"""

import os
from click.testing import CliRunner
from freezegun import freeze_time
from .conftest import abspath_conversion_tests

import ascmhl.commands


@freeze_time("2020-01-16 09:15:00")
def test_simple(fs, simple_mhl_history):
    runner = CliRunner()
    result = runner.invoke(
        ascmhl.commands.flatten, [abspath_conversion_tests("/root"), abspath_conversion_tests("/out")]
    )
    assert result.exit_code == 0


@freeze_time("2020-01-16 09:15:00")
def test_add_one_file_same_hashformat(fs, simple_mhl_history):
    runner = CliRunner()

    # add a sidecar
    fs.create_file("/root/sidecar.txt", contents="sidecar\n")
    runner = CliRunner()
    runner.invoke(ascmhl.commands.create, [abspath_conversion_tests("/root"), "-h", "xxh64"])

    result = runner.invoke(
        ascmhl.commands.flatten, [abspath_conversion_tests("/root"), abspath_conversion_tests("/out")]
    )
    assert result.exit_code == 0


@freeze_time("2020-01-16 09:15:00")
def test_simple_two_hashformats(fs, simple_mhl_history):
    runner = CliRunner()

    # add a sidecar
    runner = CliRunner()
    runner.invoke(ascmhl.commands.create, [abspath_conversion_tests("/root"), "-h", "md5"])

    result = runner.invoke(
        ascmhl.commands.flatten, [abspath_conversion_tests("/root"), abspath_conversion_tests("/out")]
    )
    assert result.exit_code == 0


@freeze_time("2020-01-16 09:15:00")
def test_nested(fs, nested_mhl_histories):
    runner = CliRunner()

    result = runner.invoke(
        ascmhl.commands.flatten, ["-v", abspath_conversion_tests("/root"), abspath_conversion_tests("/out")]
    )
    assert result.exit_code == 0

    # check for files in root and sub histories
    assert (
        result.output == f"Flattening folder at path: /root ...\n"
        "  created original hash for     Stuff.txt  xxh64: 94c399c2a9a21f9a\n"
        "\n"
        "Child History at A/AA:\n"
        "  created original hash for     A/AA/AA1.txt  xxh64: ab6bec9ec04704f6\n"
        "\n"
        "Child History at B:\n"
        "  created original hash for     B/B1.txt  xxh64: 51fb8fb099e92821\n"
        "\n"
        "Child History at B/BB:\n"
        "  created original hash for     B/BB/BB1.txt  xxh64: 5c14eac4f4ad7501\n"
        "Created new generation collection_2020-01-16/packinglist_root_2020-01-16_091500Z.mhl\n"
    )
    