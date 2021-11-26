from __future__ import annotations
from typing import Any
from os import environ, getcwd
from pathlib import Path
from json import load
from re import match
from inflection import underscore
from .keypath import keypath_split
from .singleton import singleton


@singleton
class UserConf:
    """The user's configuration.
    """

    def __init__(self) -> None:
        self._conf: dict[str, Any] = {}
        self._loaded: bool = False

    def _load(self) -> None:
        conf_path = Path(getcwd()) / 'config.json'
        if conf_path.is_file():
            with open(conf_path) as conf_file:
                self._conf = load(conf_file)
                self._replace_envs()
                self._normalize_keys()
        self._loaded = True

    def _normalize_keys(self) -> None:
        self._conf = self._normalize_keys_dict(self._conf)

    def _normalize_keys_dict(self, subconf: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for k, v in subconf.items():
            if isinstance(v, dict):
                result[underscore(k)] = self._normalize_keys_dict(v)
            elif isinstance(v, list):
                result[underscore(k)] = self._normalize_keys_list(v)
            else:
                result[underscore(k)] = v
        return result

    def _normalize_keys_list(self, subconf: list[Any]) -> list[Any]:
        result: list[Any] = []
        for v in subconf:
            if isinstance(v, dict):
                result.append(self._normalize_keys_dict(v))
            elif isinstance(v, list):
                result.append(self._normalize_keys_list(v))
            else:
                result.append(v)
        return result

    def _replace_envs(self) -> None:
        self._conf = self._replace_envs_dict(self._conf)

    def _replace_envs_dict(self, subconf: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for k, v in subconf.items():
            if type(v) is str:
                result[k] = self._replace_envs_str(v)
            elif isinstance(v, dict):
                result[k] = self._replace_envs(v)
            elif isinstance(v, list):
                result[k] = self._replace_envs_list(v)
            else:
                result[k] = v
        return result

    def _replace_envs_list(self, subconf: list[Any]) -> list[Any]:
        result: list[Any] = []
        for v in subconf:
            if type(v) is str:
                result.append(self._replace_envs_str(v))
            elif isinstance(v, dict):
                result.append(self._replace_envs(v))
            elif isinstance(v, list):
                result.append(self._replace_envs_list(v))
            else:
                result.append(v)
        return result

    def _replace_envs_str(self, subconf: str) -> str:
        mresult = match('^environ\[[\'\"](.+)[\"\']\]$', subconf)
        if mresult is not None:
            name = mresult[1]
            retval = environ.get(name)
            if retval is None:
                raise KeyError(f"environment variable '{name}' is not defined.")
            return retval
        return subconf

    def get(self, keypath: str) -> Any | None:
        keypaths = keypath_split(keypath)
        return self._get(keypaths, self._conf)

    def _get(self, keypaths: list[str], val: Any | None) -> Any | None:
        if val is None:
            return None
        cur = keypaths[0]
        if isinstance(val, list):
            next = val[int(cur)]
        elif isinstance(val, dict):
            next = val[cur]
        else:
            return None
        rest = keypaths[1:]
        if len(rest) == 0:
            return next
        else:
            return self._get(rest, next)

    def __str__(self) -> str:
        return f'UserConf<{self._conf.__str__()}>'

    def __repr__(self) -> str:
        return self.__str__()


def uconf() -> UserConf:
    return UserConf()
