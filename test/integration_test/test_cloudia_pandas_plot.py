import sys
import pathlib
import pandas as pd

if __name__ == '__main__':
    current_dir = pathlib.Path(__file__).resolve().parent
    sys.path.append(str(current_dir.parents[1]))
    import cloudia  # noqa

    try:
        pd.DataFrame({'test': ['hoge']}).wc.plot()
        pd.DataFrame({'test': ['hoge']})['test'].wc.plot()
        pd.Series(['hoge']).wc.plot()
        raise
    except Exception:
        sys.exit(1)
    sys.exit(0)
