from jsonclasses import jsonclass, types


@jsonclass
class DefaultDict:
    value: dict[str] = types.dictof(str).default({'a': '1', 'b': '2'})
