# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 13:08:17 2021

@author: solis
"""
import os
from os.path import join
# import littleLogging as logging


def vertex_get(filename):
    """
    Gets the vertex of standar asz file
    Parameters
    ----------
    filename : TYPE
        name of the asc file (input)
    Returns
    -------
    None.
    """
    keys = {'ncols': 0, 'nrows': 0, 'xllcenter': 0, 'yllcenter': 0,
            'cellsize': 0, 'nodata_value': 0}
    with open(filename, 'r') as fi:
        for i, line in enumerate(fi):
            if i<len(keys):
                a, n = line.split(' ')
                keys[a.lower()] = int(n)
                continue
            if i == len(keys):
                xmin = keys['xllcenter']
                ymax = ((keys['nrows'] -1) * keys['cellsize']) + \
                keys['yllcenter']
                xmax = ((keys['ncols'] -1) * keys['cellsize']) + \
                keys['xllcenter']
                ymin = keys['yllcenter']
            break
    return (xmin, xmax, ymin, ymax)


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


def asc2xy(filename, fileout) -> None:
    """
    changes the format of the file filename from standar asc to a new csv file
        fileout with format:
        "x","y","z"
        x1,y1,z1
        ...
        xn,yn,zn
    Parameters
    filename : Lit(str)
        name of the asc file (input)
    fileout : str
        name of the csv file (output)

    """
    keys = {'ncols': 0, 'nrows': 0, 'xllcenter': 0, 'yllcenter': 0,
            'cellsize': 0, 'nodata_value': 0}
    with open(filename, 'r') as fi, open(fileout, 'w') as fo:
        fo.write('"x","y","z"\n')
        for i, line in enumerate(fi):
            if i<len(keys):
                a, n = line.split(' ')
                keys[a.lower()] = int(n)
                continue
            if i == len(keys):
                xmin = keys['xllcenter']
                ymax = ((keys['nrows'] -1) * keys['cellsize']) + \
                keys['yllcenter']
                x = xmin
                y = ymax
            words = line.strip().split(' ')
            for w1 in words:
                if w1.strip() != keys['nodata_value']:
                    fo.write(f'{x},{y},{w1}\n')
                x += keys['cellsize']
            x = xmin
            y -= keys['cellsize']
