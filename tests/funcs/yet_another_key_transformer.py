from jsonclasses.fdef import FStore, FType
from jsonclasses.jfield import JField


def yet_another_key_transformer(field: JField) -> str:
    if field.fdef.fstore not in \
            [FStore.FOREIGN_KEY, FStore.LOCAL_KEY]:
        raise ValueError(f"field named {field.name} is not a reference field")
    if field.fdef.ftype == FType.LIST:
        return field.name + '_ids'
    elif field.fdef.ftype == FType.INSTANCE:
        return field.name + '_id'
    else:
        raise ValueError(f"field type {field.fdef.ftype} is not a "
                         "supported reference field type")
