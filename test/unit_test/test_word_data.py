from cloudia.word_data import WordData
import unittest
from unittest.mock import patch
import pandas as pd
from collections import Counter


class TestWordData(unittest.TestCase):
    def setUp(self):
        self.cls = WordData('test', lambda x: [x], True, False)

    def assertSortTextEqual(self, data, target):
        """for random sample list."""
        data = [sorted(t.split(' ')) if isinstance(t, str) else sorted(t) for t in data]
        target = [sorted(t.split(' ')) if isinstance(t, str) else sorted(t) for t in target]
        for x, y in zip(data, target):
            self.assertListEqual(x, y)

    def test_init_data_string(self):
        words, name = self.cls._init_data('test')
        self.assertListEqual(words, ['test'])
        self.assertListEqual(name, ['word cloud'])

    def test_init_data_tuple(self):
        words, name = self.cls._init_data(('name', 'test'))
        self.assertListEqual(words, ['test'])
        self.assertListEqual(name, ['name'])

    def test_init_data_list_string(self):
        words, name = self.cls._init_data(['test1 test2', 'test3'])
        self.assertSortTextEqual(words, ['test1 test2', 'test3'])
        self.assertListEqual(name, ['word cloud 1', 'word cloud 2'])

    def test_init_data_list_tuple_string(self):
        words, name = self.cls._init_data([('wc1', 'test1 test2'), ('wc2', 'test3')])
        self.assertSortTextEqual(words, ['test1 test2', 'test3'])
        self.assertListEqual(name, ['wc1', 'wc2'])

    def test_init_data_list_tuple_series(self):
        test_1 = pd.Series(['test1 test2', 'test3'], name='wc1')
        test_2 = pd.Series(['test4', 'test5', 'test6'], name='wc2')
        words, name = self.cls._init_data([('name1', test_1), ('name2', test_2)])
        self.assertSortTextEqual(words, [['test1 test2', 'test3'], 'test4 test5 test6'])
        self.assertListEqual(name, ['name1', 'name2'])

    def test_init_data_dataframe(self):
        test = pd.DataFrame({'wc1': ['test1', 'test2'], 'wc2': ['test3', 'test4']})
        words, name = self.cls._init_data(test)
        self.assertSortTextEqual(words, ['test1 test2', 'test3 test4'])
        self.assertListEqual(name, ['wc1', 'wc2'])

    def test_init_data_series(self):
        test = pd.Series(['test1', 'test2'], name='wc')
        words, name = self.cls._init_data(test)
        self.assertSortTextEqual(words, ['test1 test2'])
        self.assertListEqual(name, ['wc'])

    def test_parse(self):
        def _parse(x, y, z, **args):
            return x

        with patch('cloudia.word_data.WordData._parse', side_effect=_parse):
            output = self.cls.parse(['hoge hoge', 'piyo'], None, None, False)
            self.assertListEqual(output, ['hoge hoge', 'piyo'])

    def test_parse_list_case(self):
        def _parse(x, y, z, **args):
            return [Counter(w.split(' ')) for w in x]

        with patch('cloudia.word_data.WordData._parse', side_effect=_parse):
            output = self.cls.parse([['hoge hoge', 'piyo'], ['fuga', 'fuga']], None, None, False)
            target = [Counter({'hoge': 2, 'piyo': 1}), Counter({'fuga': 2})]
            for o, t in zip(output, target):
                self.assertEqual(type(o), type(t))
                self.assertEqual(o.most_common(), t.most_common())

    def test_convert_weight(self):
        output = self.cls.convert_weight(Counter(['hoge', 'hoge', 'piyo']))
        self.assertDictEqual(output, {'hoge': 1, 'piyo': 0.5})

    def test_single_thread_parse(self):
        def f(x):
            return x.split(' ')

        output = self.cls._single_thread_parse(['hoge hoge', 'piyo'], f)
        target = [Counter(['hoge', 'hoge']), Counter(['piyo'])]
        for o, t in zip(output, target):
            self.assertEqual(type(o), type(t))
            self.assertEqual(o.most_common(), t.most_common())

    def test_parallel_parse(self):
        def f(x, _index):
            return Counter(x.split(' ')), _index

        output = self.cls._parallel_parse(['hoge hoge', 'piyo'], f, **{})
        target = [
            Counter(['hoge', 'hoge']),
            Counter(['piyo']),
        ]
        for o, t in zip(output, target):
            self.assertEqual(type(o), type(t))
            self.assertEqual(o.most_common(), t.most_common())
