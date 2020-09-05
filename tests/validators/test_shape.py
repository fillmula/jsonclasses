import unittest
from typing import Dict
from datetime import datetime, date
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException

class TestShapeValidator(unittest.TestCase):

  def test_shape_validator_validates_subfields(self):
    @jsonclass(graph='test_shape_1')
    class User(JSONObject):
      address: dict = types.nonnull.shape({
        'line1': types.str.required,
        'line2': types.str
      })
    user = User()
    self.assertRaisesRegex(ValidationException, '\'address\\.line1\' should not be None', user.validate)

  def test_shape_validator_do_not_throw_if_subfields_are_ok(self):
    @jsonclass(graph='test_shape_2')
    class User(JSONObject):
      address: dict = types.nonnull.shape({
        'line1': types.str.required,
        'line2': types.str
      }).required
    user = User(address={ 'line1': 'Shanghai' })
    try:
      user.validate()
    except:
      self.fail('shape validator should not throw if subfields are ok')

  def test_shape_validator_assigns_none_for_accessing(self):
    @jsonclass(graph='test_shape_3')
    class User(JSONObject):
      address: dict = types.shape({
        'line1': types.str,
        'line2': types.str,
        'line3': types.str
      }).required
    user = User(address={ 'line1': 'Sydney' })
    self.assertEqual(user.__dict__, {
      'address': { 'line1': 'Sydney', 'line2': None, 'line3': None }
    })

  def test_shape_validator_sanitizes_input(self):
    @jsonclass(graph='test_shape_4')
    class User(JSONObject):
      address: dict = types.shape({
        'line1': types.str,
        'line2': types.str,
        'line3': types.str
      }).required
    user = User(address={ 'line1': 'Sydney', 'haha': 'I\'m here' })
    self.assertEqual(user.__dict__, {
      'address': { 'line1': 'Sydney', 'line2': None, 'line3': None }
    })

  def test_shape_should_camelize_keys_when_serializing_if_its_the_class_setting(self):
    @jsonclass(graph='test_shape_5', camelize_json_keys=True)
    class Score(JSONObject):
      scores: dict = types.shape({
        'student_a': types.int,
        'student_b': types.int
      })
    score = Score(scores={ 'student_a': 2, 'student_b': 4 })
    self.assertEqual(score.tojson(), { 'scores': { 'studentA': 2, 'studentB': 4 }})

  def test_shape_should_not_camelize_keys_when_serializing_if_its_the_class_setting(self):
    @jsonclass(graph='test_shape_6', camelize_json_keys=False)
    class Score(JSONObject):
      scores: dict = types.shape({
        'student_a': types.int,
        'student_b': types.int
      })
    score = Score(scores={ 'student_a': 2, 'student_b': 4 })
    self.assertEqual(score.tojson(), { 'scores': { 'student_a': 2, 'student_b': 4 }})

  def test_shape_should_handle_camelized_keys_when_initializing_if_its_the_class_setting(self):
    @jsonclass(graph='test_shape_7', camelize_json_keys=True)
    class Score(JSONObject):
      scores: dict = types.shape({
        'student_a': types.int,
        'student_b': types.int
      })
    score = Score(scores={ 'studentA': 2, 'studentB': 4 })
    self.assertEqual(score.__dict__, { 'scores': { 'student_a': 2, 'student_b': 4 }})

  def test_shape_should_not_handle_camelized_keys_when_initializing_if_its_the_class_setting(self):
    @jsonclass(graph='test_shape_8', camelize_json_keys=False)
    class Score(JSONObject):
      scores: dict = types.shape({
        'student_a': types.int,
        'student_b': types.int
      })
    score = Score(scores={ 'student_a': 2, 'student_b': 4 })
    self.assertEqual(score.__dict__, { 'scores': { 'student_a': 2, 'student_b': 4 }})

  def test_dictof_produce_error_messages_for_all_items(self):
    @jsonclass(graph='test_shape_9')
    class Quiz(JSONObject):
      numbers: Dict[str, int] = types.shape({
      'a': types.int.min(140),
      'b': types.int.min(150)
      })
    quiz = Quiz(numbers={ 'a': 1, 'b': 2, })
    self.assertRaisesRegex(ValidationException, 'numbers\\.b', quiz.validate)
