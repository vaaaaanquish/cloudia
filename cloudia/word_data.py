from typing import Any, List, Tuple, Dict
import re

from collections import Counter
import pandas as pd
from wurlitzer import pipes

with pipes() as (out, err):
    # https://github.com/clab/dynet/issues/1528
    import nagisa


def count(words: List[str], stop_words, word_num) -> Dict[str, float]:
    c = Counter(words).most_common()
    _max_count = c[0][1]
    weight = {k: v / _max_count for k, v in c if k not in stop_words}
    weight = {k: weight[k] for k in list(weight.keys())[:word_num]}
    return weight


def parse(text: str, single_words, extract_postags, num_regex) -> List[str]:
    parser = nagisa.Tagger(single_word_list=single_words)
    for x in ['"', ';', ',', '(', ')', '\u3000']:
        text = text.replace(x, ' ')
    text = text.lower()
    return [x for x in parser.extract(text, extract_postags=extract_postags).words if len(x) > 1 and not num_regex.match(x)]


def process(text, stop_words, word_num, single_words, extract_postags, num_regex):
    return count(parse(text, single_words, extract_postags, num_regex), stop_words, word_num)


class WordData:
    def __init__(self, data: Any, single_words: List[str], stop_words: List[str], extract_postags: List[str], word_num: int, parser: Any, parse_func: Any):
        words, self.names = self._init_data(data)
        self.word_num = word_num
        self.single_words = single_words
        self.extract_postags = extract_postags
        self.stop_words = stop_words
        # self.parser = nagisa.Tagger(single_word_list=self.single_words) if not parser else parser
        num_regex = re.compile('^[0-9]+$')
        self.num_regex = re.compile('^[0-9]+$')
        # if parse_func:
        #     self.words = [self.count(parse_func(x)) for x in words]
        # else:
        #     self.words = [self.count(self.parse(x)) for x in words]
        import time
        from joblib import Parallel, delayed
        from itertools import repeat
        a = time.time()
        print('joblib start', a)
        self.words = Parallel(n_jobs=-1)([
            delayed(process)(a, b, c, d, e, f)
            for a, b, c, d, e, f in zip(words, repeat(stop_words), repeat(word_num), repeat(single_words), repeat(extract_postags), repeat(num_regex))
        ])
        b = time.time()
        print('joblib end', b, b - a)

        a = time.time()
        print('start', a)
        self.parser = nagisa.Tagger(single_word_list=self.single_words) if not parser else parser
        self.words = [self.count(self.parse(x)) for x in words]
        b = time.time()
        print(' end', b, b - a)

    def count(self, words: List[str]) -> Dict[str, float]:
        c = Counter(words).most_common()
        _max_count = c[0][1]
        weight = {k: v / _max_count for k, v in c if k not in self.stop_words}
        weight = {k: weight[k] for k in list(weight.keys())[:self.word_num]}
        return weight

    def parse(self, text: str) -> List[str]:
        for x in ['"', ';', ',', '(', ')', '\u3000']:
            text = text.replace(x, ' ')
        text = text.lower()
        return [x for x in self.parser.extract(text, extract_postags=self.extract_postags).words if len(x) > 1 and not self.num_regex.match(x)]

    def _init_data(self, data: Any) -> Tuple[List[str], List[str]]:
        words, names = [], []
        if isinstance(data, list):
            if isinstance(data[0], tuple):
                if isinstance(data[0][1], pd.Series):
                    words = [' '.join(d.values.tolist()) for n, d in data]
                    names = [n for n, d in data]
                else:
                    words = [w for n, w in data]
                    names = [n for n, w in data]
            elif isinstance(data[0], str):
                words = data
                names = [f'word cloud {i+1}' for i in range(len(data))]
            elif isinstance(data[0], pd.Series):
                words = [' '.join(d.values.tolist()) for d in data]
                names = [d.name for d in data]
        elif isinstance(data, str):
            words = [data]
            names = ['word cloud']
        elif isinstance(data, tuple):
            words = [data[1]]
            names = [data[0]]
        elif isinstance(data, pd.DataFrame):
            names = data.columns.tolist()
            words = [' '.join(data[x].values.tolist()) for x in names]
        elif isinstance(data, pd.Series):
            words = [' '.join(data.values.tolist())]
            names = [data.name]

        return words, names

    def __iter__(self):
        for n, w in zip(self.names, self.words):
            yield n, w
