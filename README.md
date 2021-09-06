JSONClasses
===========
[![Pypi][pypi-image]][pypi-url]
[![Python Version][python-image]][python-url]
[![Build Status][travis-image]][travis-url]
[![License][license-image]][license-url]
[![PR Welcome][pr-image]][pr-url]

JSONClasses is a data flow pipeline and data graph framework written in Python.
It supports data sanitization, data validation, data transformation, data
presentation, data serialization, data graphing and data querying. It
eliminates the redundant coding of the process by an intuitive and innovative
declarative manner.

## How JSONClasses Works?

JSONClasses uses several Python features like type hinting and dataclasses.
With the great metaprogramming functionalities that Python offers, we can
easily extend it into a great DSL for declaring data structures, transforming
rules and validation rules.

## Why Not Create Another DSL?

GraphQL's Schema Definition Language cannot work well with programming
languages' syntax checking and type completion. To support more and more
functions, a DSL would become more and more like a programming language.

This is similar React.js, Jetpack Compose and SwiftUI. The structures of the
declaration is embedded in code, not in a special text file.

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

[Read the Documentation](https://docs.jsonclasses.com)

## Database & Web Framework Integrations

* [JSON Classes Pymongo](https://github.com/fillmula/jsonclasses-pymongo)
The mongodb integration through pymongo driver.

* [JSON Classes Sanic](https://github.com/fillmula/jsonclasses-sanic)
The sanic async web framework integration.

## Supported Python Versions

`jsonclasses` supports `Python >= 3.9.0`.

## License

MIT License

Copyright (c) 2021 Fillmula Inc.
Copyright (c) 2020 Reflection Co., Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


[pypi-image]: https://img.shields.io/pypi/v/jsonclasses.svg?style=flat-square
[pypi-url]: https://pypi.org/project/jsonclasses/
[python-image]: https://img.shields.io/pypi/pyversions/jsonclasses?style=flat-square
[python-url]: https://pypi.org/project/jsonclasses/
[travis-image]: https://img.shields.io/travis/fillmula/jsonclasses.svg?style=flat-square&color=blue&logo=travis
[travis-url]: https://travis-ci.com/fillmula/jsonclasses
[license-image]: https://img.shields.io/github/license/fillmula/jsonclasses.svg?style=flat-square
[license-url]: https://github.com/fillmula/jsonclasses/blob/master/LICENSE
[pr-image]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
[pr-url]: https://github.com/fillmula/jsonclasses
