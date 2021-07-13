<img src="https://github.com/fillmula/jsonclasses/blob/master/resources/logo.png" alt="Logo" width="auto" height="88">

JSONClasses
===========
[![Pypi][pypi-image]][pypi-url]
[![Python Version][python-image]][python-url]
[![Build Status][travis-image]][travis-url]
[![License][license-image]][license-url]
[![PR Welcome][pr-image]][pr-url]

The modern declarative data flow and data graph framework for the AI empowered
generation.

JSONClasses eliminates the separated and redundant coding of data sanitization,
data validation, data format converting and data serialization.

JSONClasses transforms all the redundant procedures into declarative
annotations and markers defined right on the dataclasses.

Just like how React.js changed the paradigms of frontend development,
JSONClasses aims leading the transforming of the insdustry backend development
standards.

## How JSONClasses Works?

JSONClasses is built on top of Python dataclasses. With the great
metaprogramming functionalities that Python dataclasses offers, we can easily
extend it into a great DSL for declaring data structures, transforming rules
and validation rules.

## Why Not Create Another SDL?

GraphQL's Schema Definition Language cannot work well with programming
languages' syntax checking and type completion. To support more and more
functions, a DSL would become more and more like a programming language.

This is similar to why React.js embedded HTML into JavaScript/TypeScript and
Apple built new Swift language features for SwiftUI.

## Why Python Is Chosen?

Python is the programming language which is nearest to AI areas. The era we are
living is an era and a generation empowered by AI. AI algorithms empower
products with unimaginable stunning features. A great product should adapt to
some level of AI to continue providing great functions for it's targeting
audience.

## Business Logic Examples

### Example 1: Dating App Users

Let's say, you are building the base user functionality for a cross-platform
dating app.

The product requirements are:

1. Unique phone number is required
2. Password should be secure, encrypted, hidden from response
3. Gender cannot be changed after set
4. This product is adult only
5. User intro should be brief

Let's transform the requirements into code.

```python
from jsonclasses import jsonclass, types

@jsonclass
class User:
  phone_no: str = types.str.unique.index.match(local_phone_no_regex).required #1
  email: str = types.str.match(email_regex)
  password: str = types.str.writeonly.length(8, 16).match(secure_password_regex).transform(salt).required #2
  nickname: str = types.str.required
  gender: str = types.str.writeonce.oneof(['male', 'female']) #3
  age: int = types.int.min(18).max(100) #4
  intro: str = types.str.truncate(500) #5
```

Look how brief it is to describe our business requirements. JSON Classes has
official support for some databases to store data permanently. If you are
building a RESTful API, you can integrate JSON Classes with flask or any
other web frameworks.

```python
from flask import Blueprint, request, jsonify
from models.article import Article

bp = Blueprint('articles', __name__, url_prefix='/articles')

@bp.get('/')
async def articles(request: Request):
  return jsonify(await User.find())

@bp.get('/<id:string>')
async def user(request, id):
  return jsonify(await User.id(id))

@bp.post('/')
async def create_user(request):
  return jsonify(User(**request.json).save())

@bp.patch('/<id:string>')
async def update_user(request, id):
  return jsonify((await User.id(id)).set(**request.json).save())

@bp.delete('/<id:string>')
async def delete_user(request, id):
  return jsonify((await User.id(id)).delete())
```

## Documentation

Read our documentation on bla bla bla.

## Database & Web Framework Integrations

* [JSON Classes Pymongo](https://github.com/fillmula/jsonclasses-pymongo)
The mongodb integration through pymongo driver.

* [JSON Classes Sanic](https://github.com/fillmula/jsonclasses-sanic)
The sanic async web framework integration.

## Supported Python Versions

`jsonclasses` supports `Python >= 3.9.0`.

## License

[MIT License](https://github.com/fillmula/jsonclasses/blob/master/LICENSE)

JSON Classes logo is designed by Albert Leung.

[pypi-image]: https://img.shields.io/pypi/v/jsonclasses.svg?style=flat-square
[pypi-url]: https://pypi.org/project/jsonclasses/
[python-image]: https://img.shields.io/pypi/pyversions/jsonclasses?style=flat-square
[python-url]: https://pypi.org/project/jsonclasses/
[travis-image]: https://img.shields.io/travis/fillmula/jsonclasses.svg?style=flat-square&color=blue&logo=travis
[travis-url]: https://travis-ci.org/fillmula/jsonclasses
[license-image]: https://img.shields.io/github/license/fillmula/jsonclasses.svg?style=flat-square
[license-url]: https://github.com/fillmula/jsonclasses/blob/master/LICENSE
[pr-image]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
[pr-url]: https://github.com/fillmula/jsonclasses
