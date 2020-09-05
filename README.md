jsonclasses
===========
[![Pypi][pypi-image]][pypi-url]
[![Python Version][python-image]][python-url]
[![Build Status][travis-image]][travis-url]
[![License][license-image]][license-url]
[![PR Welcome][pr-image]][pr-url]

Python dataclasses <=> JSON declarable, interchangeable, validatable, sanitizable.

## Motivation

Python lacks a great solution of handling JSON web inputs, JSON objects
manipulation and serialization. By declaring field specifications with extended
feature set of @dataclass, we can solve this issue elegantly.

## Installation

Install jsonclasses with pip.

```sh
pip install jsonclasses
```

## Examples

### Converting from json dict

To create a jsonclass object from json dict, just use its initialization
method. Type transforming, input sanitization, and JSON key case convension are
taken into consideration during this process.

```python
from jsonclasses import jsonclass, JSONObject, types

@jsonclass
class Article(JSONObject):
  title: str = types.str.maxlength(100).required
  content: str = types.str.required
  read_count: int = types.int.default(0).required

json_input = {
  'title': 'Declarative Web API Development with jsonclasses',
  'content': 'With jsonclasses, you can easily implement your web API with declaration style rather than procedural style.'
}

article = Article(**json_input)
# =>
# Article(
#   title='Declarative Web API Development with jsonclasses',
#   content='With jsonclasses, you can easily implement your web API with declaration style rather than procedural style.',
#   read_count=0
# )
```

### Coverting to json dict

To convert a jsonclass to json dict, use instance method `tojson`. During this
process, Python data types are converted to JSON acceptable types.

```python
from jsonclasses import jsonclass, JSONObject, types

@jsonclass
class MobilePhone(JSONObject):
  name: str = types.str.maxlength(50).required,
  model: str = types.str.oneof(['iphone', 'galaxy', 'pixel']).required,
  year: int = types.int.range(2010, 2020).required

mobile_phone = MobilePhone(name='iPhone 12', model='iphone', year=2020)

mobile_phone.tojson()
# =>
# {'name': 'iPhone 12', 'model': 'iphone', 'year': 2020}
```

### Sanitization

Jsonclass sanitizes inputs on initialization and `set`. Values of extra fields
are just ignored. Fields marked with `readonly` won't accept value inputs.

```python
from jsonclasses import jsonclass, JSONObject, types

@jsonclass
class Coupon(JSONObject):
  type: str = types.str.oneof(['spring', 'flash', 'limited']).required
  discount_rate: float = types.float.range(0, 1).required
  used: bool = types.bool.readonly.default(False).required
  user_id: str = types.str.length(24).required

json_input = {
  'type': 'flash',
  'discount_rate': 0.3,
  'used': True,
  'user_id': '12345678901234567890abcd',
  'haha': 'I want to hack into this system!'
}

Coupon(**json_input)
# =>
# Coupon(type='flash', discount_rate=0.3, used=False, user_id='12345678901234567890abcd')
# * value of field 'haha' is ignored.
# * value of 'used' is not affected by the fraud input.
```

### Validation

```python
from jsonclasses import jsonclass, JSONObject, types

@jsonclass
class UserProfile(JSONObject):
  name: str = types.str.required
  gender: str = types.str.oneof(['male', 'female'])

user_profile = UserProfile(name='John', gender='mlae')

user_profile.validate()
# =>
# jsonclasses.exceptions.ValidationException: Json classes validation failed:
#   'gender': Value 'mlae' at 'gender' should be one of ['male', 'female'].
```

### Integration with web frameworks

Using `jsonclasses` with `sanic` web framework.

```python

```

Using `jsonclasses` with `flask` web framework.

```python

```

## Supported Python versions

`jsonclasses` supports `Python >= 3.7`.

## License

[MIT License](https://github.com/WiosoftCrafts/jsonclasses/blob/master/LICENSE)

[pypi-image]: https://img.shields.io/pypi/v/jsonclasses.svg?style=flat-square
[pypi-url]: https://pypi.org/project/jsonclasses/
[python-image]: https://img.shields.io/pypi/pyversions/jsonclasses?style=flat-square
[python-url]: https://pypi.org/project/jsonclasses/
[travis-image]: https://img.shields.io/travis/WiosoftCrafts/jsonclasses.svg?style=flat-square&color=blue&logo=travis
[travis-url]: https://travis-ci.org/WiosoftCrafts/jsonclasses
[license-image]: https://img.shields.io/github/license/WiosoftCrafts/jsonclasses.svg?style=flat-square
[license-url]: https://github.com/WiosoftCrafts/jsonclasses/blob/master/LICENSE
[pr-image]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
[pr-url]: https://github.com/WiosoftCrafts/jsonclasses
