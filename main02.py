# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 12:03:01 2021

@author: solis
"""

from time import time
from os.path import join
import traceback

import littleLogging as logging
import asc2xy as axy

dir_input = r'E:\layers\IGN\MDT'
filename = ('176.030.667 PNOA_MDT05_ETRS89_HU30_0934_LID.asc',
            '110.276.488 PNOA_MDT05_ETRS89_HU30_0935_LID.asc',
            '179.861.936 PNOA_MDT05_ETRS89_HU30_0954_LID.asc',
            '167.410.938 PNOA_MDT05_ETRS89_HU30_0955_LID.asc',
            '111.926.843 PNOA_MDT05_ETRS89_HU30_0956_LID.asc',
            '131.228.095 PNOA_MDT05_ETRS89_HU30_0977_LID.asc')
filepoints = r'E:\layers\IGN\MDT\PNOA_MDT200_ETRS89_HU30_Murcia.csv'

if __name__ == "__main__":

    try:
        startTime = time()

        vertex = axy.vertex_get(filename)
        print(vertex)


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
