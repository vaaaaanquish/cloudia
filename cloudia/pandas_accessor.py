from typing import Any, List

import matplotlib.pyplot as plt
from wordcloud import STOPWORDS
import pandas as pd

from cloudia.main import CloudiaBase, Cloudia
from cloudia.utils import default_parse_func


@pd.api.extensions.register_dataframe_accessor('wc')
class CloudiaDataFrame(CloudiaBase):
    def __init__(self, df):
        self.df = df

    def plot(self,
             single_words: List[str] = [],
             stop_words: List[str] = STOPWORDS,
             extract_postags: List[str] = ['名詞', '英単語', 'ローマ字文'],
             parse_func: Any = default_parse_func,
             dark_theme: bool = False,
             title_size: int = 12,
             row_num: int = 3,
             figsize_rate: int = 2,
             multiprocess: bool = True):
        Cloudia(self.df, single_words, stop_words, extract_postags, parse_func, multiprocess).plot(dark_theme, title_size, row_num, figsize_rate)

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
             parse_func: Any = default_parse_func,
             dark_theme: bool = False,
             title_size: int = 12,
             row_num: int = 3,
             figsize_rate: int = 2,
             multiprocess: bool = True):
        Cloudia(self.series, single_words, stop_words, extract_postags, parse_func, multiprocess).plot(dark_theme, title_size, row_num, figsize_rate)

    def save(self, fig_path: str, dark_theme: bool, **args: Any):
        self.plot(**args)
        plt.savefig(fig_path, facecolor=self._color(dark_theme), pad_inches=0.0, bbox_inches="tight")
