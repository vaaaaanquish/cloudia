from cloudia.utils import default_parse_func, function_wrapper
import unittest
from collections import Counter


class TestUtils(unittest.TestCase):
    def test_default_parse_func(self):
        output = default_parse_func('This is a simple test.', ['simple test'], ['英単語'], ['is'], 'default')
        self.assertListEqual(output, ['this', 'simple\u3000test'])

    def test_function_wrapper(self):
        def test(x):
            return [x + '_']

        wf = function_wrapper(test)
        output = [wf(x, _index=i) for i, x in enumerate(['hoge', 'piyo'])]
        target = [(Counter({'hoge_': 1}), 0), (Counter({'piyo_': 1}), 1)]
        for o, t in zip(output, target):
            self.assertEqual(type(o), type(t))
            self.assertEqual(o[1], t[1])
            self.assertEqual(o[0].most_common(), t[0].most_common())
