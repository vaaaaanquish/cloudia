from cloudia.main import Cloudia
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS
import pandas as pd


@pd.api.extensions.register_dataframe_accessor('wc')
class CloudiaDataFrame(Cloudia):
    def __init__(self, df):
        self.df = df

    def plot(self,
             single_words=[],
             stop_words=STOPWORDS,
             extract_postags=['名詞', '英単語', 'ローマ字文'],
             word_num=100,
             parser=None,
             parse_func=None,
             dark_theme=False,
             figsize=(7.2, 4.8),
             wcsize=(720, 480),
             title_size=12,
             row_num=3):
        Cloudia(self.df, single_words, stop_words, extract_postags, word_num, parser, parse_func).plot(dark_theme, figsize, wcsize, title_size, row_num)

    def save(self, fig_path, dark_theme, **args):
        self.plot(args)
        plt.savefig(fig_path, facecolor=self._color(dark_theme), pad_inches=0.0, bbox_inches="tight")


@pd.api.extensions.register_series_accessor('wc')
class CloudiaSeries(Cloudia):
    def __init__(self, series):
        self.series = series

    def plot(self,
             single_words=[],
             stop_words=STOPWORDS,
             extract_postags=['名詞', '英単語', 'ローマ字文'],
             word_num=100,
             parser=None,
             parse_func=None,
             dark_theme=False,
             figsize=(7.2, 4.8),
             wcsize=(720, 480),
             title_size=12,
             row_num=3):
        Cloudia(self.series, single_words, stop_words, extract_postags, word_num, parser, parse_func).plot(dark_theme, figsize, wcsize, title_size, row_num)

    def save(self, fig_path, dark_theme, **args):
        self.plot(args)
        plt.savefig(fig_path, facecolor=self._color(dark_theme), pad_inches=0.0, bbox_inches="tight")
