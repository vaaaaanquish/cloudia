# Cloudia
Tools to easily create a word cloud.

### from string
```
from cloudia import Cloudia

text = "text data"
Cloudia(text).plot()
```

![sample_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/sample_img.png?raw=true, "sample_img")
  
from : [20 Newsgroups](http://qwone.com/~jason/20Newsgroups/)


### from pandas
```
df = pd.DataFrame({'wc1': ['sample1','sample2'], 'wc2': ['hoge hoge piyo piyo fuga', 'hoge']})

# plot from df
Cloudia(df).plot()

# add df method
df.wc.plot(dark_theme=True)
```

![pandas_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/pandas_img.png?raw=true, "pandas_img")
![dark_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/dark_img.png?raw=true, "dark_img")
  
from pandas.DataFrame or pandas.Series.


### from japanese
```
text = "これはCloudiaのテストです。WordCloudをつくるには本来、形態素解析の導入が必要になります。Cloudiaはmecabのような形態素解析器の導入は必要はなくnagisaを利用した動的な生成を行う事ができます。nagisaとjapanize-matplotlibは、形態素解析を必要としてきたWordCloud生成に対して、Cloudiaに対して大きく貢献しました。ここに感謝の意を述べたいと思います。"

Cloudia(text).plot()
```

![japanese_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/japanese_img.png?raw=true, "jap_img")
  
from japanese without morphological analysis module


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
