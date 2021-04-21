# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 13:08:17 2021

@author: solis
"""
from math import modf
import numpy as np
import os
from os.path import join, splitext
# import littleLogging as logging


class MDT_asc():
    """
    Operation between an mdt with asc format an points
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
        self.dir_input = dir_input
        self.filename = join(dir_input, filename)
        with open(self.filename, 'r') as fi:
            for i, line in enumerate(fi):
                print(i)
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
        if xmin <= x1 and x1 < xmax and ymin <= y1 and y1 < ymax:
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
        z : list of z values; len(z) = len(x, y)
        """
        for xy1 in xy:
            if not self.point_in_grid(xy1[0], xy1[1]):
                return self.keys['nodata_value']
            x1 = xy1[0]
            y1 = xy1[1]
            jcell = x1/self.keys['cellsize']
            icell = y1/self.keys['cellsize']

            d_jcell, n_jcell = modf(jcell)
            d_icell, n_icell = modf(icell)

            if d_jcell <= 0.5:
                nj = round(n_jcell)
            else:
                nj = round(n_jcell + 1)

            if d_icell <= 0.5:
                ni = round(n_icell)
            else:
                ni = round(n_icell + 1)

            i = self.keys['nrows'] - ni
            j = nj - 1
            if i < 0:
                i = 0
            elif i > self.keys['nrows'] - 1:
                i = self.keys['nrows'] - 1
            if j < 0:
                j = 0
            elif j > self.keys['ncols'] - 1:
                j = self.keys['ncols'] - 1
            return self.Z[i, j]


def asc2xys_many_files(filenames, dir_input):
    """
    Calls asc2xy for a list of filenames
    Parameters
    ----------
    filenames : List(str)
        list of names of files in asc forst to be transformed to csv format
    dir_input : directory of filenames
    Returns
    -------
    None.
    """
    for i, filen1 in enumerate(filenames):
        print(i)
        fname, fext = os.path.splitext(filen1)
        fileout = f'{fname}.csv'
        asc2xy(join(dir_input, filen1), join(dir_input, fileout))


    def asc2xy(self) -> None:
        """
        changes the format of the file filename from standar asc
        to a new csv file fileout with format:
            "x","y","z"
            x1,y1,z1
            ...
            xn,yn,zn
        """
        name, ext = splitext(self.filename)
        fileout = name + '.csv'
        with open(fileout, 'w') as fo:
            fo.write('"x","y","z"\n')
            for i in self.Z.shape[0]:
                for j in self.Z.shape[1]:
                    if w1.strip() != keys['nodata_value']:
                        fo.write(f'{x},{y},{w1}\n')
                    x += keys['cellsize']
                x = xmin
                y -= keys['cellsize']


# def vertex_get(filename):
#     """
#     Gets the vertex of standar asz file
#     Parameters
#     ----------
#     filename : str
#         name of the asc file (input)
#     Returns
#     -------
#         tuple with 2 elements (xmin, ymin), (xmax, ymax) of the asc
#         filename
#     """
#     keys = {'ncols': 0, 'nrows': 0, 'xllcenter': 0, 'yllcenter': 0,
#             'cellsize': 0, 'nodata_value': 0}
#     with open(filename, 'r') as fi:
#         for i, line in enumerate(fi):
#             if i<len(keys):
#                 a, n = line.split(' ')
#                 keys[a.lower()] = int(n)
#                 continue
#             if i == len(keys):
#                 xmin = keys['xllcenter']
#                 ymax = ((keys['nrows'] -1) * keys['cellsize']) + \
#                 keys['yllcenter']
#                 xmax = ((keys['ncols'] -1) * keys['cellsize']) + \
#                 keys['xllcenter']
#                 ymin = keys['yllcenter']
#             break
#     return ((xmin, ymin), (xmax, ymax))


