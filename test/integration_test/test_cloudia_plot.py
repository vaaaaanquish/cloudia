import sys
import pathlib
import pandas as pd

if __name__ == '__main__':
    current_dir = pathlib.Path(__file__).resolve().parent
    sys.path.append(str(current_dir.parents[1]))
    from cloudia.main import Cloudia

    try:
        Cloudia([('test', pd.Series(['hoge']))]).plot()
        Cloudia([('test', 'hoge')]).plot()
        Cloudia(['hoge']).plot()
        Cloudia([pd.Series(['hoge'])]).plot()
        Cloudia('hoge').plot()
        Cloudia(('test', 'hoge')).plot()
        Cloudia(pd.DataFrame({'test': ['hoge']})).plot()
        Cloudia(pd.Series(['hoge'])).plot()
    except Exception:
        sys.exit(1)
    sys.exit(0)
