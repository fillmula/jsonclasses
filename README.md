🌎 JSONClasses [![Pypi][pypi-image]][pypi-url] [![Python Version][python-image]][python-url] [![License][license-image]][license-url] [![PR Welcome][pr-image]][pr-url]
===========

JSONClasses is a declarative data flow pipeline and data graph framework.

Official Website: https://www.jsonclasses.com

Official Documentation: https://docs.jsonclasses.com

## 🚗 Features

|     | **Features**|
| --- | ----------------------------------------------------------------------------------|
| 🛠  | **Data Modeling** Declarative data model with Python type hints |
| 🍸  | **Data Sanitization** Two strictness modes |
| 🩺  | **Data Validation** Descriptive data validation rules without even a line of code |
| 🧬  | **Data Transformation** Intuitive with modifier pipelines |
| 🦖  | **Data Presentation** Custom key encoding & decoding strategies |
| 🌍  | **Data Graphing** Models are linked with each other on the same graph |
| 🏄‍♂️  | **Data Querying** Well-designed protocols and implementations for databases |
| 🚀  | **Synthesized CRUD** Only with a line of code |
| 👮‍♀️  | **Session & Authorization** Builtin support for session and authorization |
| 🔐  | **Permission System** Supports both object level and field level |
| 📁  | **File Uploading** A configuration is enough for file uploading |
| 📦  | **Data Seeder** Declarative named graph relationship |

## 🍎 Getting Started

### Prerequisites

[Python >= 3.10](https://www.python.org) is required. You can download it [here](https://www.python.org/downloads/).

### Install JSONClasses

Install JSONClasses is simple with `pip`.

```sh
pip install jsonclasses
```

### Install Components

Depends on your need, you can install ORM integration and HTTP library integration with the following commands.

```sh
pip install jsonclasses-pymongo jsonclasses-server
```

## 🎹 Examples

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
from jsonclasses_pymongo import pymongo
from jsonclasses_server import api


@api
@pymongo
@jsonclass
class User:
    id: str = types.readonly.str.primary.mongoid.required
    phone_no: str = types.str.unique.index.match(local_phone_no_regex).required #1
    email: str = types.str.match(email_regex)
    password: str = types.str.writeonly.length(8, 16).match(secure_password_regex).transform(salt).required #2
    nickname: str = types.str.required
    gender: str = types.str.writeonce.oneof(['male', 'female']) #3
    age: int = types.int.min(18).max(100) #4
    intro: str = types.str.truncate(500) #5
    created_at: datetime = types.readonly.datetime.tscreated.required
    updated_at: datetime = types.readonly.datetime.tsupdated.required
```

## ⚽️ Database & HTTP Library Integrations

* [JSON Classes Pymongo](https://github.com/fillmula/jsonclasses-pymongo)
The mongodb integration through pymongo driver.

* [JSON Classes Server](https://github.com/fillmula/jsonclasses-server)
The server integration.

## 🦸 Contributing

* File a [bug report](https://github.com/fillmula/jsonclasses/issues/new). Be sure to include information like what version of YoMo you are using, what your operating system is, and steps to recreate the bug.
* Suggest a new feature.

## 🤹🏻‍♀️ Feedback

Any questions or good ideas, please feel free to come to our Discussion. Any feedback would be greatly appreciated!

## License

[MIT License](https://github.com/fillmula/jsonclasses/blob/master/LICENSE)

[pypi-image]: https://img.shields.io/pypi/v/jsonclasses.svg?style=flat-square
[pypi-url]: https://pypi.org/project/jsonclasses/
[python-image]: https://img.shields.io/pypi/pyversions/jsonclasses?style=flat-square
[python-url]: https://pypi.org/project/jsonclasses/
[license-image]: https://img.shields.io/github/license/fillmula/jsonclasses.svg?style=flat-square
[license-url]: https://github.com/fillmula/jsonclasses/blob/master/LICENSE
[pr-image]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
[pr-url]: https://github.com/fillmula/jsonclasses
