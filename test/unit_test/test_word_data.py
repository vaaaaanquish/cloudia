from cloudia.word_data import WordData
import unittest


class TestCloudia(unittest.TestCase):
    def setUp(self):
        self.cls = WordData('test', [], [], None, None, None, lambda x: [x])

    def test_init_data(self):
        words, name = self.cls._init_data('test')
        self.assertListEqual(words, ['test'])
        self.assertListEqual(name, ['word cloud'])

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
