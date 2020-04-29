from cloudia.word_data import WordData
import unittest
import pandas as pd


class TestCloudia(unittest.TestCase):
    def setUp(self):
        self.cls = WordData('test', [], [], None, None, None, lambda x: [x])

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
        self.assertListEqual(words, ['test1 test2', 'test3'])
        self.assertListEqual(name, ['word cloud 1', 'word cloud 2'])

    def test_init_data_list_tuple_string(self):
        words, name = self.cls._init_data([('wc1', 'test1 test2'), ('wc2', 'test3')])
        self.assertListEqual(words, ['test1 test2', 'test3'])
        self.assertListEqual(name, ['wc1', 'wc2'])

    def test_init_data_list_tuple_series(self):
        test_1 = pd.Series(['test1 test2', 'test3'], name='wc1')
        test_2 = pd.Series(['test4', 'test5', 'test6'], name='wc2')
        words, name = self.cls._init_data([('name1', test_1), ('name2', test_2)])
        self.assertListEqual(words, ['test1 test2 test3', 'test4 test5 test6'])
        self.assertListEqual(name, ['name1', 'name2'])

    def test_init_data_dataframe(self):
        test = pd.DataFrame({'wc1': ['test1', 'test2'], 'wc2': ['test3', 'test4']})
        words, name = self.cls._init_data(test)
        self.assertListEqual(words, ['test1 test2', 'test3 test4'])
        self.assertListEqual(name, ['wc1', 'wc2'])

    def test_init_data_series(self):
        test = pd.Series(['test1', 'test2'], name='wc')
        words, name = self.cls._init_data(test)
        self.assertListEqual(words, ['test1 test2'])
        self.assertListEqual(name, ['wc'])

    def test_count(self):
        self.cls.word_num = 2
        self.cls.stop_words = 'test'
        words = ['hoge', 'hoge', 'hoge', 'test', 'test', 'piyo', 'piyo', 'fuga']
        output = self.cls.count(words)
        self.assertDictEqual(output, {'hoge': 1.0, 'piyo': 0.6666666666666666})

    def test_parse(self):
        class MockData:
            def __init__(self, d):
                self.words = d

        class MockParser:
            def extract(self, text, extract_postags):
                return MockData(text.split(' '))

        self.cls.parser = MockParser()
        output = self.cls.parse("It's a sample text; samples 1,2 face;) ")
        self.assertListEqual(output, ["it's", 'sample', 'text', 'samples', 'face'])
