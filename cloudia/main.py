import matplotlib.pyplot as plt
import japanize_matplotlib
from wordcloud import WordCloud, STOPWORDS
from cloudia.word_data import WordData


class Cloudia:
    def __init__(self, data, single_words=[], stop_words=STOPWORDS, extract_postags=['名詞', '英単語', 'ローマ字文'], word_num=100, parser=None, parse_func=None):
        self.wd = WordData(data=data,
                           single_words=single_words,
                           stop_words=stop_words,
                           extract_postags=extract_postags,
                           word_num=word_num,
                           parser=parser,
                           parse_func=parse_func)

    def plot(self, dark_theme=False, figsize=(7.2, 4.8), wcsize=(720, 480), title_size=12, row_num=3):
        wc = self.make_wordcloud(dark_theme, wcsize)
        self.make_fig(wc, dark_theme, figsize, title_size, row_num)

    def save(self, fig_path, dark_theme=False, figsize=(7.2, 4.8), wcsize=(720, 480), title_size=12, row_num=3):
        wc = self.make_wordcloud(dark_theme, wcsize)
        self.make_fig(wc, dark_theme, figsize, title_size, row_num)
        plt.savefig(fig_path, facecolor=self._color(dark_theme), pad_inches=0.0, bbox_inches="tight")

    def make_wordcloud(self, dark_theme, wcsize):
        wordcloud_list = []
        for name, words in self.wd:
            wordcloud = WordCloud(font_path=japanize_matplotlib.get_font_ttf_path(),
                                  background_color=self._color(dark_theme),
                                  width=wcsize[0],
                                  height=wcsize[1])
            wordcloud.fit_words(words)
            wordcloud_list.append((name, wordcloud))
        return wordcloud_list

    def make_fig(self, wordcloud_list, dark_theme, figsize, title_size, row_num):
        fig = plt.figure(facecolor=self._color(dark_theme), figsize=figsize)
        w, h = self._calc_sub_plot_dimensions(len(wordcloud_list), row_num)
        for i, (title, wc) in enumerate(wordcloud_list):
            ax = fig.add_subplot(w, h, i + 1)
            ax.imshow(wc)
            ax.set_title(title, color=self._color(dark_theme, True), fontsize=title_size)
            ax.axis('off')

    @staticmethod
    def _calc_sub_plot_dimensions(l, row_num):
        return (l // row_num) + 1, row_num if l > row_num else l

    @staticmethod
    def _color(dark_theme, text=False):
        if text:
            return 'white' if dark_theme else 'black'
        return 'black' if dark_theme else 'white'
