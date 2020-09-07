JSON Classes
===========
[![Pypi][pypi-image]][pypi-url]
[![Python Version][python-image]][python-url]
[![Build Status][travis-image]][travis-url]
[![License][license-image]][license-url]
[![PR Welcome][pr-image]][pr-url]

The Modern Declarative Data Flow Framework for the AI Empowered Generation.

JSON Classes eliminates the separation and redundant coding of data
sanitization, data validation, data format converting, data serialization and
data persistent storage.

JSON Classes transforms all the redundant procedures into declarative
annotations and markers defined right on the data classes.

Just like how React.js changed the paradigms of frontend development, JSON
Classes aims leading the transforming of the insdustry backend development
standards.

## How JSON Classes Works?

JSON Classes is built on top of Python Data Classes. With the great
metaprogramming functionalities that Python Data Classes offers, we can easily
extend it into a great DSL for declaring data structures, transforming rules
and validation rules.

## Why Not Create Another SDL?

GraphQL's Schema Definition Language cannot work well with programming
languages' syntax checking and type completion. To support more and more
functions, a DSL would become more and more like a programming language.

This is why React.js embedded HTML into JavaScript/TypeScript and Apple built
new Swift language features for SwiftUI.

## Why Python Is Chosen?

Python is the programming language which is nearest to AI areas. This is an era
and a generation empowered by AI. AI algorithms empower products with
unimaginable stunning features. A great product should adapt to some level of AI
to continue providing great functions for it's targeting audience.

## Business Examples

### Example 1: Dating App Users

Let's say, you are building the base user functionality for a cross-platform
dating app.

The product requirements are:

1. Unique phone number is required
2. Password should be secure and encrypted
3. Gender cannot be changed after set
4. This product is adult only
5. User intro should be brief

Let's transform the requirements into code.

```python
from jsonclasses import jsonclass, JSONObject, types

@jsonclass
class User(JSONObject):
  phone_no: str = types.str.unique.index.match(local_phone_no_regex).required #1
  email: str = types.str.match(email_regex)
  password: str = types.str.length(8, 16).match(secure_password_regex).transform(salt).required #2
  nickname: str = types.str.required
  gender: str = types.str.writeonce.oneof(['male', 'female']) #3
  age: int = types.int.min(18).max(100) #4
  intro: str = types.str.truncate(500) #5
```

Look how brief it is to describe our business requirements. JSON Classes has
official support for some databases to store data permanently. If you are
building a RESTful API, you can integrate JSON Classes with flask, sanic or any
other web frameworks.

```python
from sanic import Blueprint
from sanic.request import Request
from jsonclasses_sanic import response
from jsonclasses_sanic.middlewares import only_handle_json_middleware
from models import User

bp = Blueprint('users')

bp.middleware('request')(only_handle_json_middleware)

@bp.get('/')
async def users(request: Request):
  return response.data(User.find())

@bp.get('/<id:string>')
async def user(request, id):
  return response.data(User.find_by_id(id))

@bp.post('/')
async def create_user(request):
  return response.data(User(**request.json).save())

@bp.patch('/<id:string>')
async def update_user(request, id):
  return response.data(User.find_by_id(id).set(**request.json).save())

@bp.delete('/<id:string>')
async def delete_user(request, id):
  return response.empty(User.delete_by_id(id))
```

## Documentation

Read our documentation on bla bla bla.

## Database & Web Framework Integrations

* [JSON Classes Pymongo](https://github.com/WiosoftCrafts/jsonclasses-pymongo)
The mongodb integration through pymongo driver.

* [JSON Classes Sanic](https://github.com/WiosoftCrafts/jsonclasses-sanic)
The sanic async web framework integration.

## Supported Python Versions

`jsonclasses` supports `Python >= 3.8`.

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
