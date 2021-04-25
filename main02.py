# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 12:03:01 2021

@author: solis

set z values in a set of filepoints; zs are extracted from a asc file
by running the funtion get_z_drv in module get_z_drv
"""

from time import time
import traceback

import littleLogging as logging
import mdt_asc as mdt

filepoints = r'E:\IGME20\20201215_aquifer\_data\JLGA_20210217\CRCC\Pozos_eia2017.csv'
dtypes = {'gid': 'int32', 'x': 'float32', 'y': 'float32'}
dir_asc_files = r'E:\layers\IGN\MDT'
filenames = ('PNOA_MDT05_ETRS89_HU30_0934_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0935_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0954_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0955_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0956_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0977_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0978_LID.asc')
output_file = 'zpoints.csv'

if __name__ == "__main__":

    try:
        startTime = time()

        df = mdt.get_z_drv(filepoints, dtypes, dir_asc_files, filenames,
                           output_file)

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
