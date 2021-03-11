from jsonclasses import jsonclass, types


@jsonclass
class GenderUser:
    nickname: str = types.str.required
    gender: str = types.str.writeonce.oneof(['male', 'female']).required
