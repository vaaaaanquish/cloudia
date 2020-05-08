import sys
import pathlib
import traceback
import pandas as pd

if __name__ == '__main__':
    current_dir = pathlib.Path(__file__).resolve().parent
    sys.path.append(str(current_dir.parents[1]))
    from cloudia.main import Cloudia

    try:
        for multiprocess in [True, False]:
            Cloudia([('test', pd.Series(['hoge']))], multiprocess=multiprocess).plot()
            Cloudia([('test', 'hoge')], multiprocess=multiprocess).plot()
            Cloudia(['hoge'], multiprocess=multiprocess).plot()
            Cloudia([pd.Series(['hoge'])], multiprocess=multiprocess).plot()
            Cloudia('hoge', multiprocess=multiprocess).plot()
            Cloudia(('test', 'hoge'), multiprocess=multiprocess).plot()
            Cloudia(pd.DataFrame({'test': ['hoge']}), multiprocess=multiprocess).plot()
            Cloudia(pd.Series(['hoge']), multiprocess=multiprocess).plot()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)
