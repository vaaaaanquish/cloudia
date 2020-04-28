from collections import Counter
import pandas as pd
import re
from wurlitzer import pipes

with pipes() as (out, err):
    # https://github.com/clab/dynet/issues/1528
    import nagisa


class WordData:
    def __init__(self, data, single_words, stop_words, extract_postags, word_num, parser, parse_func):
        self.words, self.names = self._init_data(data)
        self.word_num = word_num
        self.single_words = single_words
        self.extract_postags = extract_postags
        self.stop_words = stop_words
        self.parser = nagisa.Tagger(single_word_list=self.single_words) if not parser else parser
        self.num_regex = re.compile('^[0-9]+$')
        if parse_func:
            self.words = [self.count(parse_func(x)) for x in self.words]
        else:
            self.words = [self.count(self.parse(x)) for x in self.words]

    def _init_data(self, data):
        words, names = [], []
        if isinstance(data, list):
            if isinstance(data[0], tuple):
                if isinstance(data[0][1], pd.Series):
                    words = [' '.join(d.tolist()) for n, d in data]
                    names = [n for n, d in data]
                else:
                    words = [w for n, w in data]
                    names = [n for n, w in data]
            elif isinstance(data[0], str):
                words = data
                names = [f'word cloud {i+1}' for i in range(len(data))]
            elif isinstance(data[0], pd.Series):
                words = [' '.join(d.tolist()) for d in data]
                names = [d.name for d in data]
        elif isinstance(data, str):
            words = [data]
            names = ['word cloud']
        elif isinstance(data, tuple):
            words = [data[1]]
            names = [data[0]]
        elif isinstance(data, pd.DataFrame):
            names = data.columns.tolist()
            words = [' '.join(data[n].tolist()) for n in names]
        elif isinstance(data, pd.Series):
            words = [' '.join(data.tolist())]
            names = [data.name]

        return words, names

    def count(self, words):
        c = Counter(words).most_common()
        _max_count = c[0][1]
        weight = {k: v / _max_count for k, v in c if k not in self.stop_words}
        weight = {k: weight[k] for k in list(weight.keys())[:self.word_num]}
        return weight

    def parse(self, text):
        for x in ['"', ';', ',', '(', ')', '\u3000']:
            text = text.replace(x, ' ')
        text = text.lower()
        return [x for x in self.parser.extract(text, extract_postags=self.extract_postags).words if len(x) > 1 and not self.num_regex.match(x)]

    def __iter__(self):
        for n, w in zip(self.names, self.words):
            yield n, w
