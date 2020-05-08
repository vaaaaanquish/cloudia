import sys
import pathlib
import traceback
import pandas as pd

if __name__ == '__main__':
    current_dir = pathlib.Path(__file__).resolve().parent
    sys.path.append(str(current_dir.parents[1]))
    import cloudia  # noqa

    try:
        for multiprocess in [True, False]:
            pd.DataFrame({'test': ['hoge']}).wc.plot(multiprocess=multiprocess)
            pd.DataFrame({'test': ['hoge']})['test'].wc.plot(multiprocess=multiprocess)
            pd.Series(['hoge']).wc.plot(multiprocess=multiprocess)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
