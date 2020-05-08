from typing import Any, List, Tuple, Dict
from itertools import repeat, chain, zip_longest
from collections import Counter

from joblib import Parallel, delayed
import pandas as pd

from cloudia.utils import function_wrapper


class WordData:
    def __init__(self, data: Any, parse_func: Any, multiprocess: bool, **args):
        words, self.names = self._init_data(data)
        self.counter_list = self.parse(words, parse_func, multiprocess, **args)
        self.words = [self.convert_weight(x) for x in self.counter_list]

    def parse(self, words, parse_func: Any, multiprocess: bool, **args) -> List[List[str]]:
        if isinstance(words[0], list):
            word_list_length = len(words[0])
            words = list(chain.from_iterable(words))
            words = self._parse(words, parse_func, multiprocess, **args)
            words = list(zip_longest(*[iter(words)] * word_list_length))
            words = [sum(w, Counter()) for w in words]
        else:
            words = self._parse(words, parse_func, multiprocess, **args)
        return words

    def convert_weight(self, c: Counter) -> Dict[str, float]:
        c = c.most_common()
        _max_count = c[0][1]
        weight = {k: v / _max_count for k, v in c}
        weight = {k: weight[k] for k in list(weight.keys())}
        return weight

    def _parse(self, words: List[str], parse_func: Any, multiprocess: bool, **args) -> List[str]:
        if multiprocess:
            return self._parallel_parse(words, function_wrapper(parse_func), **args)
        return self._single_thread_parse(words, parse_func, **args)

    def _single_thread_parse(self, words: List[str], parse_func: Any, **args) -> List[str]:
        return [Counter(parse_func(x, **args)) for x in words]

    def _parallel_parse(self, words: List[str], parse_func: Any, **args) -> List[str]:
        words = Parallel(n_jobs=-1)([delayed(parse_func)(w, **dict(**a, **{'_index': i})) for i, (w, a) in enumerate(zip(words, repeat(args)))])
        words.sort(key=lambda x: x[1])
        words = [t[0] for t in words]
        return words

    def _init_data(self, data: Any) -> Tuple[List[str], List[str]]:
        # TODO: set assert
        words, names = [], []
        if isinstance(data, list):
            if isinstance(data[0], tuple):
                if isinstance(data[0][1], pd.Series):
                    words = [d.values.tolist() for n, d in data]
                    names = [n for n, d in data]
                else:
                    words = [w for n, w in data]
                    names = [n for n, w in data]
            elif isinstance(data[0], str):
                words = data
                names = [f'word cloud {i+1}' for i in range(len(data))]
            elif isinstance(data[0], pd.Series):
                words = [d.values.tolist() for d in data]
                names = [d.name for d in data]
        elif isinstance(data, str):
            words = [data]
            names = ['word cloud']
        elif isinstance(data, tuple):
            words = [data[1]]
            names = [data[0]]
        elif isinstance(data, pd.DataFrame):
            names = data.columns.tolist()
            words = [data[x].values.tolist() for x in names]
        elif isinstance(data, pd.Series):
            words = [data.values.tolist()]
            names = [data.name]
        return words, names

    def __iter__(self):
        for n, w in zip(self.names, self.words):
            yield n, w
