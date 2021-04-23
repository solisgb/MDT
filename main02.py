# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 12:03:01 2021

@author: solis
"""

from time import time
import traceback

import pandas as pd
import numpy as np

import littleLogging as logging
import mdt_asc as mdt

dir_input = r'E:\layers\IGN\MDT'
filenames = ('PNOA_MDT05_ETRS89_HU30_0934_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0935_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0954_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0955_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0956_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0977_LID.asc')

filepoints = r'E:\IGME20\20201215_aquifer\_data\JLGA_20210217\CRCC\Pozos_eia2017.csv'
dtypes = {'gid': 'int32', 'x': 'float32', 'y': 'float32'}
dtypes2 = (np.int32, np.float32, np.float32)


if __name__ == "__main__":

    try:
        startTime = time()

        points = pd.read_csv(filepoints, index_col=0, dtype=dtypes)

        points = np.genfromtxt(filepoints, skip_header=1, delimiter=',',
                               dtype=dtypes2)

        for fn in filenames:
            grd = mdt.MDT_asc(dir_input, fn)







    except ValueError:
        msg = traceback.format_exc()
        logging.append(msg)
    except ImportError:
        msg = traceback.format_exc()
        logging.append(msg)
    except Exception:
        msg = traceback.format_exc()
        logging.append(msg)
    finally:
        logging.dump()
        xtime = time() - startTime
        print(f'El script tardó {xtime:0.1f} s')
