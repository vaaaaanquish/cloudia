# Cloudia
Tools to easily create a word cloud.

WordCloud from 
```
from cloudia import Cloudia

text = "text data"
Cloudia(text).plot()
```


from : [20 Newsgroups](http://qwone.com/~jason/20Newsgroups/)


```
df = pd.DataFrame({'wc1': ['sample1','sample2'], 'wc2': ['hoge hoge piyo piyo fuga', 'hoge']})

# plot from df
Cloudia(df).plot()

# add df method
df.wc.plot(dark_theme=True)
```

from pandas.DataFrame or pandas.Series.


```
text = "これはCloudiaのテストです。WordCloudをつくるには本来、形態素解析の導入が必要になります。Cloudiaはmecabのような形態素解析器の導入は必要はなくnagisaを利用した動的な生成を行う事ができます。nagisaとjapanize-matplotlibは、形態素解析を必要としてきたWordCloud生成に対して、Cloudiaに対して大きく貢献しました。ここに感謝の意を述べたいと思います。"

Cloudia(text).plot()
```
from japanese

# Require

I'm waiting for this [PR](https://github.com/uehara1414/japanize-matplotlib/pull/9).
```
pip install git+https://github.com/vaaaaanquish/japanize-matplotlib
```

# Install

```
pip install cloudia
```

# Thanks

- [japanize-matplotlib](https://github.com/uehara1414/japanize-matplotlib)
- [nagisa](https://github.com/taishi-i/nagisa)
