from jsonclasses import jsonclass, types


@jsonclass
class UserSOS:
    name: str = types.str.required
    age: int = types.int.setonsave(lambda x: x + 300).required


@jsonclass
class UserSOSZ:
    name: str = types.str.required
    age: int = types.int.setonsave(lambda: 500).required
