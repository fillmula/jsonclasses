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

print(Article(**json_input))
