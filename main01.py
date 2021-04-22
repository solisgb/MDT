# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 13:08:40 2020

@author: solis
"""

from time import time
import traceback

import littleLogging as logging
import mdt_asc as mdt

dir_input = r'E:\layers\IGN\MDT'
filenames = ('PNOA_MDT05_ETRS89_HU30_0934_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0935_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0954_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0955_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0956_LID.asc',
             'PNOA_MDT05_ETRS89_HU30_0977_LID.asc')

points = [[659078, 4188818], [659078, 4188822], [659082, 4188818], [659082, 4188822]]


if __name__ == "__main__":

    try:
        startTime = time()

        grd = mdt.MDT_asc(dir_input, filenames[0])
        # z = grd.z_get(points)
        # for z1 in z:
        #     print(z1)

        grd.asc2csv()

        #axy.asc2xy(filename, fileout)


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
