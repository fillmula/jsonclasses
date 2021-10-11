from jsonclasses import jsonclass, types


@jsonclass
class UserSOS:
    name: str = types.str.required
    age: int = types.int.setonsave(lambda x: x + 300).required


@jsonclass
class UserSOSZ:
    name: str = types.str.required
    age: int = types.int.setonsave(lambda: 500).required


@jsonclass
class UserFSOS:
    name: str = types.str.required
    age: int = types.int.fsetonsave(lambda x: (x or 0) + 100).required


@jsonclass
class UserTFSOS:
    name: str = types.str.required
    code: str = types.str.fsetonsave(types.randomdigits(4)).required
