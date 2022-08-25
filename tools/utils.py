from __future__ import annotations

import re
import sys
import copy
import json
import shutil
import os.path
import argparse
import importlib.util
import urllib.request

from pathlib import Path
from typing import TYPE_CHECKING, Callable, Any, Iterable

import note_files

from json_minify import json_minify


if TYPE_CHECKING:
    import types

EXAMPLE_CONFIG_PATH = "config/example_config.py"
DEFAULT_CONFIG_PATH = "config/config.py"

rx_GET_VERSION = re.compile(r"JP Mining Note: Version (\d+\.\d+\.\d+\.\d+)")


cached_config = None


def add_args(parser):
    group = parser.add_argument_group(title="common")
    group.add_argument("-c", "--config-file", type=str, default=None)
    # group.add_argument(
    #    "--override-config",
    #    action="store_true",
    #    help="overrides the current config file with the example config, "
    #    "if no specific config file was specified.",
    # )
    group.add_argument(
        "-r",
        "--release",
        action="store_true",
        default=False,
        help="uses the default options for when building for release",
    )
    group.add_argument(
        "-f",
        "--build-folder",
        type=str,
        default="build",
        help="output folder for the build process, and input folder for installation",
    )


def get_args(*args: Callable[[argparse.ArgumentParser], None]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    for add_args_func in args:
        add_args_func(parser)
    return parser.parse_args()


class Config:
    # def __init__(self, config_data: dict, description: str = ""):
    def __init__(self, data, path: list[int | str] = []):
        self.data = data
        # assert isinstance(self.data, dict)
        # self.desc = description
        self.path = copy.deepcopy(path)

    # def get_opt(self, *args):
    #    current_dict = self.data
    #    for key in args:
    #        if not isinstance(self.data, dict):
    #            raise RuntimeError(f"Argument {key} (from {args}) is not a dictionary")
    #        if key not in self.data:
    #            raise RuntimeError(f"Argument {key} (from {args}) not in config")
    #        current_dict = current_dict[key]

    #    if isinstance(current_dict, dict):
    #        return Config(current_dict)
    #    return current_dict

    def container(self) -> dict | list:
        assert isinstance(self.data, dict) or isinstance(self.data, list)
        return self.data

    def list(self) -> list:
        assert isinstance(self.data, list)
        return self.data

    def dict(self) -> dict:
        assert isinstance(self.data, dict)
        return self.data

    def item(self, javascript=False) -> Any:
        # assert not (isinstance(self.data, dict) or isinstance(self.data, list))
        if not javascript:
            return self.data
        var = self.data
        if var == True:
            return "true"
        elif var == False:
            return "false"
        elif isinstance(var, str):
            return f"'{var}'"
        return var

    def key(self) -> int | str:
        # assert not (isinstance(self.data, dict) or isinstance(self.data, list))
        return self.path[-1]

    def dict_values(self) -> Iterable[Config]:
        assert isinstance(self.data, dict)
        for key in self.data.keys():
            yield Config(self.data[key], self.path + [key])

    def dict_items(self) -> Iterable[tuple["str", Config]]:
        assert isinstance(self.data, dict)
        for key in self.data.keys():
            yield key, Config(self.data[key], self.path + [key])

    def list_items(self) -> Iterable[Config]:
        assert isinstance(self.data, list)
        for i, item in enumerate(self.data):
            yield Config(item, self.path + [i])

    def __call__(self, *keys: str | int) -> Config:
        """
        - returns a config object if dictionary
        - otherwise returns the expected object (list, str, int, etc.)
        - automatically detects errors with unknown keys

        can be called either way:
        >>> config("note_opts")("keybinds")("toggle-hybrid-sentence")
        >>> config("note_opts", "keybinds", "toggle-hybrid-sentence")
        """
        result = self  # returns itself if no keys

        current_config = self
        for i, key in enumerate(keys):
            if not (isinstance(self.data, dict) or isinstance(self.data, list)):
                raise RuntimeError(
                    f"Key '{key}' is not in the data value {current_config}. "
                    "Ensure your config matches the example config!"
                )

            if not (
                (isinstance(current_config.item(), dict) and key in current_config.data)
                or (
                    isinstance(current_config.item(), list)
                    and isinstance(key, int)
                    and key < len(current_config.data)
                )
            ):
                raise RuntimeError(f"Key '{key}' is not in {repr(current_config)}")
            result = current_config.data[key]

            # if isinstance(result, dict):
            #    current_config = Config(
            #        #result, description=f"{current_config.desc}.{key}"
            #        result, path=self.path + [key]
            #    )
            current_config = Config(
                # result, description=f"{current_config.desc}.{key}"
                result,
                path=current_config.path + [key],
            )

            # elif i < len(keys) - 1:
            #    # ensures that current_config is always a config object
            #    raise RuntimeError(
            #        f"Key '{keys[i+1]}' is not in the data value "
            #        f"Config({current_config.path}.{key}). "
            #        "Ensure your config matches the example config!"
            #    )

        # if isinstance(result, dict) and not get_dict:
        #    return current_config
        # return result
        return current_config

    def __repr__(self):
        return f"Config({'.'.join([str(x) for x in self.path])})"


# TODO upgrade python to 3.10 so I can do str | Path
# https://stackoverflow.com/a/41595552
def import_source_file(fname: str, modname: str) -> "types.ModuleType":
    """
    Import a Python source file and return the loaded module.

    Args:
        fname: The full path to the source file.  It may container characters like `.`
            or `-`.
        modname: The name for the loaded module.  It may contain `.` and even characters
            that would normally not be allowed (e.g., `-`).
    Return:
        The imported module

    Raises:
        ImportError: If the file cannot be imported (e.g, if it's not a `.py` file or if
            it does not exist).
        Exception: Any exception that is raised while executing the module (e.g.,
            :exc:`SyntaxError).  These are errors made by the author of the module!
    """
    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    spec = importlib.util.spec_from_file_location(modname, fname)
    if spec is None:
        raise ImportError(f"Could not load spec for module '{modname}' at: {fname}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    try:
        assert spec.loader is not None
        spec.loader.exec_module(module)
    except FileNotFoundError as e:
        raise ImportError(f"{e.strerror}: {fname}") from e
    return module


# taken from https://github.com/FooSoft/anki-connect#python
def request(action, **params):
    return {"action": action, "params": params, "version": 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode("utf-8")
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request("http://localhost:8765", requestJson)
        )
    )
    if len(response) != 2:
        raise Exception("response has an unexpected number of fields")
    if "error" not in response:
        raise Exception("response is missing required error field")
    if "result" not in response:
        raise Exception("response is missing required result field")
    if response["error"] is not None:
        raise Exception(response["error"])
    return response["result"]


def get_config_from_str(file_path: str):
    module = import_source_file(file_path, "config")
    if module is None:
        raise Exception("Module is None and cannot be imported")
    # config = getattr(module, "CONFIG", None)
    # if config is None:
    if not hasattr(module, "CONFIG"):
        raise Exception("CONFIG variable is not defined in the config file")

    return module.CONFIG


def get_note_opts(config, as_config=False):
    opts_file = config("jp-mining-note", "opts-path").item()
    root_folder = get_root_folder()
    opts_path = os.path.join(root_folder, "config", opts_file)

    with open(opts_path) as f:
        contents = f.read()

    if as_config:
        return Config(json.loads(json_minify(contents)))

    return contents


def get_version() -> str:
    """
    gets version of the jp mining note within the repo
    """

    root_folder = get_root_folder()
    with open(os.path.join(root_folder, "version.txt")) as f:
        version = f.read().strip()

    return version


def note_is_installed(note_name) -> bool:
    result = invoke("modelNames")
    return note_name in result


def get_version_from_anki(config: Config) -> str:
    """
    gets version of the jp mining note from the installed note in anki
    """
    result = invoke(
        "modelTemplates",
        modelName=config("notes", "jp-mining-note", "model-name").item(),
    )

    assert result.keys()

    # doesn't matter which card it is
    what = list(result.values())[0]["Front"]
    match = rx_GET_VERSION.search(what)

    assert match is not None
    return match.group(1)


def get_config(args) -> Config:
    """
    creates the config file from the example config if it doesn't exist
    """
    global cached_config  # lazy fix

    if cached_config is not None:
        return cached_config

    file_path = args.config_file

    tools_folder = os.path.dirname(os.path.abspath(__file__))
    root_folder = os.path.join(tools_folder, "..")

    example_config_path = os.path.join(root_folder, EXAMPLE_CONFIG_PATH)
    default_config_path = os.path.join(root_folder, DEFAULT_CONFIG_PATH)

    if file_path is None:
        file_path = default_config_path

        if args.release:
            file_path = example_config_path
            print(f"Building release: using the example config...")

        elif not os.path.isfile(default_config_path):  # or args.override_config:
            print(f"Creating the config file under '{file_path}'...")
            if not os.path.isfile(EXAMPLE_CONFIG_PATH):
                raise Exception("Example config file does not exist")
            shutil.copy(example_config_path, default_config_path)

    config_data = get_config_from_str(file_path)

    config = Config(config_data, path=["root"])
    cached_config = config
    return config


def get_note_files_config():
    return Config(note_files.NOTE_DATA)


def gen_dirs(file_path):
    """
    generates all directories for a file path if the directories don't exist
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)


def get_root_folder():
    """
    grabs the repository root folder
    """

    tools_folder = os.path.dirname(os.path.abspath(__file__))
    root_folder = os.path.join(tools_folder, "..")

    return root_folder


if __name__ == "__main__":
    # x = import_source_file(EXAMPLE_CONFIG_PATH, "config")
    # print(x)
    # print(getattr(x, "CONFIG", None))
    # print(getattr(x, "not_a_variable", None))

    args = get_args(add_args)
    config = get_config(args)
    # print(config("build_opts"))

    # print(config("build-opts", "optimize-opts", "always-filled"))
    # print(config("build-opts")("optimize-opts")("never-filled"))
    # print(config("note-opts")("keybinds")("toggle-hybrid-sentence"))
    # print(config("note-opts", "keybinds", "toggle-hybrid-sentence"))
    # print(config("note-opts", "keybinds", "toggle-hybrid-sentence"))
    # print(config("notes", "jp-mining-note", "media-build", 0))
    # print(config("note_opts", "keybinds", "toggle-hybrid-sentence", "a", "b"))
    # print(config("note_opts", "keybinds", "a"))

    print(get_version_from_anki(config))

    # print(x.CONFIG)
