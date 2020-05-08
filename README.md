# Cloudia
Tools to easily create a word cloud.

  
### from string

from str or List[str]
```
from cloudia import Cloudia

text1 = "text data..."
text2 = "text data..."

# from str
Cloudia(text1).plot()

# from list
Cloudia([text1, text2]).plot()
```
 
example from : [20 Newsgroups](http://qwone.com/~jason/20Newsgroups/)

![sample_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/sample_img.png?raw=true, "sample_img")
  

We can also make it from Tuple.
```
from cloudia import Cloudia

text1 = "text data..."
text2 = "text data..."
Cloudia([ ("cloudia 1", text1), ("cloudia 2", text2) ]).plot()
```
Tuple is ("IMAGE TITLE", "TEXT").  
  
  
### from pandas

We can use pandas.

```
df = pd.DataFrame({'wc1': ['sample1','sample2'], 'wc2': ['hoge hoge piyo piyo fuga', 'hoge']})

# plot from df
Cloudia(df).plot()

# add df method
df.wc.plot(dark_theme=True)
```

from pandas.DataFrame or pandas.Series.

![pandas_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/pandas_img.png?raw=true, "pandas_img")
![dark_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/dark_img.png?raw=true, "dark_img")
  
We can use Tuple too.
```
Cloudia( ("IMAGE TITLE", pd.Series(['hoge'])) ).plot()
```
  
  
### from japanese

We can process Japanese too.
```
text = "これはCloudiaのテストです。WordCloudをつくるには本来、形態素解析の導入が必要になります。Cloudiaはmecabのような形態素解析器の導入は必要はなくnagisaを利用した動的な生成を行う事ができます。nagisaとjapanize-matplotlibは、形態素解析を必要としてきたWordCloud生成に対して、Cloudiaに対して大きく貢献しました。ここに感謝の意を述べたいと思います。"

Cloudia(text).plot()
```

from japanese without morphological analysis module.  
  
![japanese_img](https://github.com/vaaaaanquish/cloudia/blob/021a6d151fb6a3b579dc96b7086356fc0c225852/examples/img/japanese_img.png?raw=true, "jap_img")  
  
No need to introduce morphological analysis.
  
  
# Install

```
pip install cloudia
```
  
  
# Args

Cloudia args.
```
Cloudia(
  data,    # text data
  single_words=[],    # It's not split word list, example: ["neural network"]
  stop_words=STOPWORDS,    # not count words, default is wordcloud.STOPWORDS
  extract_postags=['名詞', '英単語', 'ローマ字文'],    # part of speech for japanese
  parse_func=None,    # split text function, example: lambda x: x.split(',')
  multiprocess=True    # Flag for using multiprocessing
)
```
  
  
plot method args.
```
Cloudia().plot(
    dark_theme=False,    # color theme
    title_size=12,     # title text size
    row_num=3,    # for example, 12 wordcloud, row_num=3 -> 4*3image
    figsize_rate=2    # figure size rate
)
```

save method args.
```
Cloudia().save(
    file_path,    # save figure image path
    dark_theme=False,
    title_size=12, 
    row_num=3,
    figsize_rate=2
)
```

pandas.DataFrame, pandas.Series wc.plot method args.
```
DataFrame.wc.plot(
  single_words=[],    # It's not split word list, example: ["neural network"]
  stop_words=STOPWORDS,    # not count words, default is wordcloud.STOPWORDS
  extract_postags=['名詞', '英単語', 'ローマ字文'],    # part of speech for japanese
  parse_func=None,    # split text function, example: lambda x: x.split(',')
  multiprocess=True,    # Flag for using multiprocessing
  dark_theme=False,    # color theme
  title_size=12,     # title text size
  row_num=3,    # for example, 12 wordcloud, row_num=3 -> 4*3image
  figsize_rate=2    # figure size rate
)
```
If we use wc.save, setting file_path args.
  
  
# Thanks

- [japanize-matplotlib](https://github.com/uehara1414/japanize-matplotlib)
- [nagisa](https://github.com/taishi-i/nagisa)
