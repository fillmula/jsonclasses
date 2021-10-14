from __future__ import annotations
from typing import Any, Optional
from os import environ, getcwd
from pathlib import Path
from json import load
from re import match


_conf: dict[str, Any] = {}
_conf_loaded: bool = False


def _replace_envs_str(conf: str) -> Optional[str]:
    mresult = match('^environ\[[\'\"](.+)[\"\']\]$', conf)
    if mresult is not None:
        name = mresult[1]
        retval = environ.get(name)
        if retval is None:
            raise KeyError(f"environment variable '{name}' is not defined.")
        return retval
    return conf


def _replace_envs_list(conf: list[Any]) -> list[Any]:
    result: list[Any] = []
    for v in conf:
        if type(v) is str:
            result.append(_replace_envs_str(v))
        elif isinstance(v, dict):
            result.append(_replace_envs(v))
        elif isinstance(v, list):
            result.append(_replace_envs_list(v))
        else:
            result.append(v)
    return result


def _replace_envs(conf: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for k, v in conf.items():
        if type(v) is str:
            result[k] = _replace_envs_str(v)
        elif isinstance(v, dict):
            result[k] = _replace_envs(v)
        elif isinstance(v, list):
            result[k] = _replace_envs_list(v)
        else:
            result[k] = v
    return result


def _load_user_conf() -> None:
    global _conf
    global _conf_loaded
    conf_path = Path(getcwd()) / 'config.json'
    if conf_path.is_file():
        with open(conf_path) as conf_file:
            conf = load(conf_file)
            _conf = _replace_envs(conf)
    _conf_loaded = True


def user_conf() -> dict[str, Any]:
    if not _conf_loaded:
        _load_user_conf()
    return _conf
