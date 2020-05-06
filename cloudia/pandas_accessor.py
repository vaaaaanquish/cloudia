from typing import Any, List

from cloudia.main import CloudiaBase, Cloudia
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS
import pandas as pd


@pd.api.extensions.register_dataframe_accessor('wc')
class CloudiaDataFrame(CloudiaBase):
    def __init__(self, df):
        self.df = df

    def plot(self,
             single_words: List[str] = [],
             stop_words: List[str] = STOPWORDS,
             extract_postags: List[str] = ['名詞', '英単語', 'ローマ字文'],
             word_num: int = 100,
             parser: Any = None,
             parse_func: Any = None,
             sampling_rate: float = 1.0,
             dark_theme: bool = False,
             title_size: int = 12,
             row_num: int = 3,
             figsize_rate: int = 2):
        Cloudia(self.df, single_words, stop_words, extract_postags, word_num, parser, parse_func,
                sampling_rate).plot(dark_theme, title_size, row_num, figsize_rate)

    def save(self, fig_path: str, dark_theme: bool, **args: Any):
        self.plot(**args)
        plt.savefig(fig_path, facecolor=self._color(dark_theme), pad_inches=0.0, bbox_inches="tight")


@pd.api.extensions.register_series_accessor('wc')
class CloudiaSeries(CloudiaBase):
    def __init__(self, series):
        self.series = series

    def plot(self,
             single_words: List[str] = [],
             stop_words: List[str] = STOPWORDS,
             extract_postags: List[str] = ['名詞', '英単語', 'ローマ字文'],
             word_num: int = 100,
             parser: Any = None,
             parse_func: Any = None,
             sampling_rate: float = 1.0,
             dark_theme: bool = False,
             title_size: int = 12,
             row_num: int = 3,
             figsize_rate: int = 2):
        Cloudia(self.series, single_words, stop_words, extract_postags, word_num, parser, parse_func,
                sampling_rate).plot(dark_theme, title_size, row_num, figsize_rate)

    def save(self, fig_path: str, dark_theme: bool, **args: Any):
        self.plot(**args)
        plt.savefig(fig_path, facecolor=self._color(dark_theme), pad_inches=0.0, bbox_inches="tight")
