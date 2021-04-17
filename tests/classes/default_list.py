from jsonclasses import jsonclass, types


@jsonclass
class DefaultList:
    value: list[str] = types.listof(str).default(['1', '2', '3'])
