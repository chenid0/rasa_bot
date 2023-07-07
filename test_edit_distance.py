import unittest
from edit_distance import compare_to_string
class TestEditDistance(unittest.TestCase):

    def test_empty_string(self):
        words = ["molecuel", "mollecule"]
        output = compare_to_string(words, "molecule")
        self.assertEqual(output, {"molecuel": 2, "mollecule": 1})

    def test_exact_match(self):
        words = ["hello", "world"]
        output = compare_to_string(words, "hello")
        self.assertEqual(output, {"hello": 0, "world": 4})

    def test_single_edit(self):
        words = ["hello", "world"]
        output = compare_to_string(words, "helli")
        self.assertEqual(output, {"hello": 1, "world": 4})

    def test_multiple_words(self):
        words = ["hello", "world", "foo", "bar"]
        output = compare_to_string(words, "fooo")
        self.assertEqual(output, {"hello": 4, "world": 4, "foo": 1, "bar": 4})

    def test_empty_iterable(self):
        words = []
        output = compare_to_string(words, "hello")
        self.assertEqual(output, {})

if __name__ == '__main__':
    unittest.main()
