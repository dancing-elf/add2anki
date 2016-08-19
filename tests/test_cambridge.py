import unittest
import add2anki.cambridge as cambridge


class TestCambridge(unittest.TestCase):

    def test_join(self):
        self.assertEqual(cambridge._join(['foo']), 'foo')
        self.assertEqual(cambridge._join(['foo', 'bar']), 'foo, bar')

    def test_is_dictionary_form(self):
        self.assertTrue(cambridge._is_dictionary_form('group'))
        self.assertFalse(cambridge._is_dictionary_form('group secret'))
        self.assertFalse(cambridge._is_dictionary_form('“group”'))
        

if __name__ == '__main__':
    unittest.main()