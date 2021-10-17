from __future__ import annotations
from importlib import import_module
from subprocess import check_call
from sys import executable


def check_package(module_name: str, info: tuple[str, str]) -> None:
    try:
        import_module(module_name)
    except:
        raise ModuleNotFoundError(f'module {module_name} is not found. please install {info[0]}{info[1]}')


def install_package(info: tuple[str, str]) -> None:
    param = f'{info[0]}{info[1]}'
    check_call([executable, "-m", "pip", "install", param])
    with open('requirements.txt', 'r') as file:
        content = file.read()
        lines = content.split('\n')
        has = False
        for line in lines:
            if info[0] in line:
                has = True
        if not has:
            with open('requirements.txt', 'a') as afile:
                afile.write(param + '\n')


def check_and_install_packages(packages: dict[str, (str, str)] | None) -> None:
    for module_name, info in packages.items():
        try:
            check_package(module_name, info)
        except:
            install_package(info)
