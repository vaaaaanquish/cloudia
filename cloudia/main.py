from typing import Any, List, Tuple

import matplotlib.pyplot as plt
import japanize_matplotlib
from wordcloud import WordCloud, STOPWORDS
from cloudia.word_data import WordData


class CloudiaBase:
    def __init__(self,
                 data: Any,
                 single_words: List[str] = [],
                 stop_words: List[str] = STOPWORDS,
                 extract_postags: List[str] = ['名詞', '英単語', 'ローマ字文'],
                 word_num: int = 100,
                 parser: Any = None,
                 parse_func: Any = None,
                 sampling_rate: float = 1.0):
        self.wd = WordData(data=data,
                           single_words=single_words,
                           stop_words=stop_words,
                           extract_postags=extract_postags,
                           word_num=word_num,
                           parser=parser,
                           parse_func=parse_func,
                           sampling_rate=sampling_rate)

    def make_wordcloud(self, dark_theme: bool, rate: int) -> List[Tuple[str, WordCloud]]:
        wordcloud_list = []
        wcsize = self._calc_wc_size(rate)
        for name, words in self.wd:
            wordcloud = WordCloud(font_path=japanize_matplotlib.get_font_ttf_path(),
                                  background_color=self._color(dark_theme),
                                  width=wcsize[0],
                                  height=wcsize[1])
            wordcloud.fit_words(words)
            wordcloud_list.append((name, wordcloud))
        return wordcloud_list

    def make_fig(self, wordcloud_list: List[Tuple[str, WordCloud]], dark_theme: bool, title_size: int, row_num: int, rate: int):
        fig = plt.figure(facecolor=self._color(dark_theme), figsize=self._calc_fig_size(row_num, len(wordcloud_list), rate))
        w, h = self._calc_sub_plot_dimensions(len(wordcloud_list), row_num)
        for i, (title, wc) in enumerate(wordcloud_list):
            ax = fig.add_subplot(w, h, i + 1)
            ax.imshow(wc)
            ax.set_title(title, color=self._color(dark_theme, True), fontsize=title_size)
            ax.axis('off')

    @staticmethod
    def _calc_fig_size(row_num: int, item_num: int, rate: int) -> Tuple[int, int]:
        if row_num == 1 and item_num == 1:
            return rate * 5 * 2, rate * 3 * 2
        if item_num <= row_num:
            return rate * 5 * item_num, rate * 3 * item_num
        elif item_num // row_num + 1 < row_num:
            return rate * 5 * row_num, rate * 3 * ((item_num // row_num + 1) % row_num)
        return rate * 5 * row_num, rate * 3 * (row_num + ((item_num // row_num + 1) - row_num))

    @staticmethod
    def _calc_wc_size(rate: int) -> Tuple[int, int]:
        return rate * 5 * 100, rate * 3 * 100

    @staticmethod
    def _calc_sub_plot_dimensions(l: int, row_num: int) -> Tuple[int, int]:
        return (l // row_num) + 1, row_num if l > row_num else l

    @staticmethod
    def _color(dark_theme: bool, text: bool = False) -> str:
        if text:
            return 'white' if dark_theme else 'black'
        return 'black' if dark_theme else 'white'


class Cloudia(CloudiaBase):
    def plot(self, dark_theme: bool = False, title_size: int = 12, row_num: int = 3, figsize_rate: int = 2):
        wc = self.make_wordcloud(dark_theme, figsize_rate)
        self.make_fig(wc, dark_theme, title_size, row_num, figsize_rate)

    def save(self, fig_path: str, dark_theme: bool = False, title_size: int = 12, row_num: int = 3, figsize_rate: int = 2):
        wc = self.make_wordcloud(dark_theme, figsize_rate)
        self.make_fig(wc, dark_theme, title_size, row_num, figsize_rate)
        plt.savefig(fig_path, facecolor=self._color(dark_theme), pad_inches=0.0, bbox_inches="tight")
