from collections import Counter
from typing import List
import re

from wurlitzer import pipes

with pipes() as (out, err):
    # https://github.com/clab/dynet/issues/1528
    import nagisa

NUM_REGEX = re.compile('^[0-9]+$')


def make_nagisa_tagger(single_words: List[str]):
    return nagisa.Tagger(single_word_list=single_words)


def default_parse_func(text: str, single_words: List[str], extract_postags: List[str], stop_words: List[str], parser) -> List[str]:
    if parser == 'default':
        parser = make_nagisa_tagger(single_words)
    for x in ['"', ';', ',', '(', ')', '\u3000']:
        text = text.replace(x, ' ')
    text = text.lower()
    return [x for x in parser.extract(text, extract_postags=extract_postags).words if len(x) > 1 and not NUM_REGEX.match(x) and x not in stop_words]


def function_wrapper(func):
    def _f(t, **kwargs):
        i = kwargs.pop('_index')
        d = Counter(func(t, **kwargs))
        return d, i

    return _f
