from jsonclasses import jsonclass, types


@jsonclass
class DefaultStr:
    value: str = types.str.default('abc')
