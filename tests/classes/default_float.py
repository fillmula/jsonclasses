from jsonclasses import jsonclass, types


@jsonclass
class DefaultFloat:
    value: float = types.float.default(1.5)
