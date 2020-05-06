from typing import Any, List, Tuple, Dict
import re

from collections import Counter
import pandas as pd
from wurlitzer import pipes

with pipes() as (out, err):
    # https://github.com/clab/dynet/issues/1528
    import nagisa


class WordData:
    def __init__(self, data: Any, single_words: List[str], stop_words: List[str], extract_postags: List[str], word_num: int, parser: Any, parse_func: Any,
                 sampling_rate: float):
        words, self.names = self._init_data(data, sampling_rate)
        self.word_num = word_num
        self.single_words = single_words
        self.extract_postags = extract_postags
        self.stop_words = stop_words
        self.parser = nagisa.Tagger(single_word_list=self.single_words) if not parser else parser
        self.num_regex = re.compile('^[0-9]+$')
        if parse_func:
            self.words = [self.count(parse_func(x)) for x in words]
        else:
            self.words = [self.count(self.parse(x)) for x in words]

    def _init_data(self, data: Any, sampling_rate: float) -> Tuple[List[str], List[str]]:
        words, names = [], []
        if isinstance(data, list):
            if isinstance(data[0], tuple):
                if isinstance(data[0][1], pd.Series):
                    words = [' '.join(d.sample(frac=sampling_rate).tolist()) for n, d in data]
                    names = [n for n, d in data]
                else:
                    words = [w for n, w in data]
                    names = [n for n, w in data]
            elif isinstance(data[0], str):
                words = data
                names = [f'word cloud {i+1}' for i in range(len(data))]
            elif isinstance(data[0], pd.Series):
                words = [' '.join(d.sample(frac=sampling_rate).tolist()) for d in data]
                names = [d.name for d in data]
        elif isinstance(data, str):
            words = [data]
            names = ['word cloud']
        elif isinstance(data, tuple):
            words = [data[1]]
            names = [data[0]]
        elif isinstance(data, pd.DataFrame):
            names = data.columns.tolist()
            words = [' '.join(data[n].sample(frac=sampling_rate).tolist()) for n in names]
        elif isinstance(data, pd.Series):
            words = [' '.join(data.sample(frac=sampling_rate).tolist())]
            names = [data.name]

        return words, names

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

    def __iter__(self):
        for n, w in zip(self.names, self.words):
            yield n, w
