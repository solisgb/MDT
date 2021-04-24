# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 13:08:17 2021

@author: solis
"""
import numpy as np
from os.path import join, splitext
import pandas as pd
import littleLogging as logging


class MDT_asc():
    """
    This module does 2 operations:
    1) Assign z values to a set of points fiven a set of asc files
    2) Changes the format of a set of asc files to a csv format:
        "x","y","z"
        x1,y1,z1
        ...
        xn,yn,zn
    """

    keys = {'ncols': 0, 'nrows': 0, 'xllcenter': 0, 'yllcenter': 0,
            'cellsize': 0, 'nodata_value': 0}


    def __init__(self, dir_input, filename):
        """
        Parameters
        ----------
        dir_input : str
            path to filename
        filename : str
            name of the asc file (input)
        Returns
        -------
        mdt_asc object
        """
        print(filename)
        self.dir_input = dir_input
        self.filename = join(dir_input, filename)
        with open(self.filename, 'r') as fi:
            for i, line in enumerate(fi):
                if i<len(self.keys):
                    a, n = line.split(' ')
                    self.keys[a.lower()] = int(n)
                    continue
                if i == len(self.keys):
                    self.Z = np.empty((self.keys['nrows'],
                                       self.keys['ncols']), dtype=object)
                    self.xmin = self.keys['xllcenter']
                    self.ymax = ((self.keys['nrows'] -1) * \
                            self.keys['cellsize']) + self.keys['yllcenter']
                    self.xmax = ((self.keys['ncols'] -1) * \
                            self.keys['cellsize']) + self.keys['xllcenter']
                    self.ymin = self.keys['yllcenter']
                    j = -1
                words = line.strip().split(' ')
                j += 1
                self.Z[j, :] = words
                if j == self.keys['nrows'] - 1:
                    break


    def point_in_grid(self, x1, y1):
        """
        tests if the point x1, y1 is into th grid
        Parameters
        ----------
        x1 : float
            x coordinate
        y1 : float
            y coordinate
        Returns
        -------
        bool : if point is into the grid returns True, else False
        """
        delta = self.keys['cellsize'] / 2
        xmin = self.xmin - delta
        xmax = self.xmax + delta
        ymin = self.ymin - delta
        ymax = self.ymax + delta
        if xmin <= x1 and x1 <= xmax and ymin <= y1 and y1 <= ymax:
            return True
        else:
            return False


    def z_get(self, xy):
        """
        returns the z value given a list of x, y coordinates
        Parameters
        ----------
        xy : List([float, float)
            list of coordinates as [x1, y1], [x2, y2]...
        Returns
        z : List(List)), each element: ii, x1, y1, z1
        """
        z = []
        tiny = 0.1
        for ii, xy1 in enumerate(xy):
            if not self.point_in_grid(xy1[0], xy1[1]):
                msg = f'{ii} {xy1[0]} {xy1[1]} NO está en {self.filename}'
                logging.append(msg, False)
                continue

            x1 = xy1[0]
            y1 = xy1[1]

            if x1 >= self.xmax:
                x1 = self.xmax - tiny
            if y1 >= self.ymax:
                y1 = self.ymax - tiny
            if x1 <= self.xmin:
                x1 = self.xmin
            if y1 <= self.ymin:
                y1 = self.ymin

            xi = ((y1 - self.ymin) * self.keys['nrows']) / (self.ymax -
                                                            self.ymin)
            xj = ((x1 - self.xmin) * self.keys['ncols']) / (self.xmax -
                                                            self.xmin)

            i = self.keys['nrows'] - int(xi) - 1
            j = int(xj)

            z.append([ii, self.Z[i, j]])
        return z


    @staticmethod
    def asc2xys_many_files(filenames):
        """
        Calls asc2xy for a list of instances MDT_asc
        Parameters
        ----------
        filenames : List(MDT_asc)
            list of instances MDT_asc to be written as csv format
        Returns
        -------
        None.
        """
        for i, filen1 in enumerate(filenames):
            print(i)
            filen1.asc2xy()


    def asc2csv(self) -> None:
        """
        writes self as new csv file -fileout- with format:
            "x","y","z"
            x1,y1,z1
            ...
            xn,yn,zn
        """
        name, ext = splitext(self.filename)
        fileout = name + '.csv'
        with open(fileout, 'w') as fo:
            fo.write('"x","y","z"\n')
            x = self.xmin
            y = self.ymax
            for i in range(self.Z.shape[0]):
                for j in range(self.Z.shape[1]):
                    if self.Z[i, j].strip() != self.keys['nodata_value']:
                        fo.write(f'{x},{y},{self.Z[i, j]}\n')
                    x += self.keys['cellsize']
                x = self.xmin
                y -= self.keys['cellsize']


def get_z_drv(filepoints, dir_asc_files, filenames, dtypes):
    """
    driver to assign its z value to a set of points in filepoints
    Parameters
    ----------
    filepoints : str
        csv file with the following structure
        "gid","x","y"
        gid1 (int), x1 (float), y1 (float)
        ...
        gidn, xn, yn
    dir_asc_files : str
        directory where filenames are found
    filenames : List(str)
        list in wich each element is the name of a standar asc file
    dtypes : Dictionary with 3 elements,
        {'gid': type, 'x': type, 'y': type}, examples:
        dtypes = {'gid': 'int32', 'x': 'float32', 'y': 'float32'}
        dtypes = {'gid': 'str', 'x': 'float32', 'y': 'float32'}
        dtypes = {'gid': 'int32', 'x': 'float64', 'y': 'float64'}
    Returns
    -------
    None.
    """
    dfp = pd.read_csv(filepoints, dtype=dtypes)
    dfp['z'] = np.nan
    dfp['file'] = ''
    xys = [[row.x, row.y] for index, row in dfp.iterrows()]

    for fn in filenames:
        grd = MDT_asc(dir_asc_files, fn)
        zs = grd.z_get(xys)
        for z1 in zs:
            dfp.at[z1[0], 'z'] = z1[-1]
            dfp.at[z1[0], 'file'] = fn
        dfp2 = dfp.loc[dfp['z'] == np.NaN]
        xys = [[row.x, row.y] for index, row in dfp2.iterrows()]
    if len(dfp2.index) > 0:
        msg = f'there are {len(dfp2.index)} points without assigned z'
        logging.append(msg)
        msg = dfp2.to_string()
        print(msg)


