import unittest

from examples.json_parser import *

class TestParser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def parse(self, string):
        parser = JSONParser(string)
        parser.parse()
        tree = parser.tree
        tokens = parser.tokens
        #parser.pretty_print()
        #print(f"Tree: {tree}")
        #print(f"Tokens: {tokens}")
        return tree, tokens

    def test_null(self):
        json = '[null]'
        tree, tokens = self.parse(json)
        tokens_assert = "['[', 'null', ']']"
        assert str(tokens) == tokens_assert
        tree_str = "root: [value: [array: [value: [null]]]]"
        assert str(tree) == tree_str

    def test_false(self):
        json = '[false]'
        tree, tokens = self.parse(json)
        tokens_assert = "['[', 'false', ']']"
        assert str(tokens) == tokens_assert
        tree_str = "root: [value: [array: [value: [false]]]]"
        assert str(tree) == tree_str

    def test_true(self):
        json = '[true]'
        tree, tokens = self.parse(json)
        tokens_assert = "['[', 'true', ']']"
        assert str(tokens) == tokens_assert
        tree_str = "root: [value: [array: [value: [true]]]]"
        assert str(tree) == tree_str

    def test_number(self):
        json = '[1]'
        tree, tokens = self.parse(json)
        tokens_assert = "['[', '1', ']']"
        assert str(tokens) == tokens_assert
        tree_str = "root: [value: [array: [value: [number: [1]]]]]"
        assert str(tree) == tree_str

    def test_array(self):
        json = '["test", "test2"]'
        tree, tokens = self.parse(json)
        tokens_assert = "['[', '\"', 'test', '\"', ',', '\"', 'test2', '\"', ']']"
        assert str(tokens) == tokens_assert
        tree_str = "root: [value: [array: [value: [string: [test]],value: [string: [test2]]]]]"
        assert str(tree) == tree_str

    def test_object(self):
        json = '{"test":"test", "test2":"test"}'
        tree, tokens = self.parse(json)
        tokens_assert = "['{', '\"', 'test', '\"', ':', '\"', 'test', '\"', ',', '\"', 'test2', '\"', ':', '\"', 'test', '\"', '}']"
        assert str(tokens) == tokens_assert
        tree_str = "root: [value: [object: [member: [string: [test],value: [string: [test]]],member: [string: [test2],value: [string: [test]]]]]]"
        assert str(tree) == tree_str
