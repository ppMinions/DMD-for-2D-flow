import numpy as np
import os
import tkinter as tk


def Read_Dat_File(path, file_name, line_start, line_end):
    # read the .dat file (Tecplot format), extract data information
    # and transform to the numpy array.
    """

    Parameters
    ----------
    path : str
        the location where the working directory
    file_name : str
        the file name
    line_start : int
        the line number where the data starts in the dat file
    line_end : int
        the line number where the data ends in the dat file

    Returns
    -------
    data_arr: 2D numpy.array
        the data from the .dat file
    header_list: 1D list
        the head information of the .dat file
    tail_list: 1D list
        the block information of the .dat file


    """

    os.chdir(path)
    header_list = []  # list for containing the header lines in the .dat file
    tail_list = []  # list for containing the block information in the .dat file
    data_list = []  # list for containing the data information in the .dat file
    with open(file_name, 'r') as of:
        lines = of.readlines()
        header_list = lines[:line_start]
        tail_list = lines[line_end:]
        lines = lines[line_start: line_end]
        for line in lines:
            # erase the space
            line = line.strip('\n').split()
            line_list = []
            for strings in line:
                line_list = line_list + (strings.strip(',').split(','))
                line_list = list(map(float, line_list))  # type transformation
            data_list.append(line_list)
    data_arr = np.array(data_list)
    return data_arr, header_list, tail_list

def Write_Dat_File(path, file_name, old_arr, header_list, tail_list):
    # transform the array to .dat file(Tecplot file) and save the .dat file to the specific location
    """
    Parameters
    path: str
        the location where the data will store
    file_name: str
        the file name specified by the users
    old_arr: 2D numpy.array
        the handled arrays
    header_list: str
        the head information of the .dat file, output by the Func Read_Dat_File
    tail_list: str
        the block information of the .dat file, output by the Func Read_Dat_File


    Note:
        the head_list and the tail_list are different for different .dat files, it is
        necessary to distinguish this two lists when handle a number of .dat files.

    """

    # transform numpy to list and generate the final lists
    data_list = old_arr.tolist()
    data_list = list(tk._flatten(data_list))
    data_list_ = []
    num_array = np.arange(0, len(data_list), 3)
    for i in num_array:
        temp = str(data_list[i]) + ' ' + str(data_list[i + 1]) + ' ' + str(data_list[i + 2]) + '\n'
        data_list_.append(temp)
    data_list_ultimate = header_list + data_list_ + tail_list

    # form the .dat file
    path = path + file_name
    dat_file = open(path, 'w', encoding="utf-8")
    for rows in data_list_ultimate:
        rows = str(rows)
        if rows[-1] != '\n':
            rows = rows + '\n'
        dat_file.write(rows)
    dat_file.close()



def Extract_Dat(arr, x_low, x_up, y_low, y_up):
    # extract the specific areas from the original data
    """

    Parameters
    ----------
    arr: 1D numpy array
        the arrays of the object data
    x_low: float
        the lower limit of the X coordinate
    x_up: float
        the upper limit of the X coordinate
    y_low: float
        the lower limit of the Y coordinate
    y_up: float
        the upper limit of the Y coordinate


    Returns
    -------
    object_arr: 1D numpy.array
        the object data
    id_arr: 1D numpy.array
        the index of the object data

    Note：
        the output of the functions contains two numpy arrays, the first one is our interested data and
        the second one is the index of the data, the index is for the data prolongation to the .dat files.
    -------

    """

    object = []
    index = []
    for i in range(arr.shape[0]):
        if (x_low < arr[i, 0] < x_up) and (y_low < arr[i, 1] < y_up):
            object.append(arr[i, 2])
            index.append(i)
    object_arr = np.array(object)
    id_arr = np.array(index)
    return object_arr, id_arr


def Replace_Dat(old_arr, object_arr, id_arr):
    # Replace the old array by the handled data
    """

    Parameters
    ----------
    old_arr: 2D numpy.array
        the original array of the data, output by the Funcs Read_Dat_File
    object_arr: 1D numpy.array
        the objected data
    id_arr: 1D numpy.array
        the index of the objected data, output by the Funcs Extract_Dat

    Returns
    -------
    old_arr: 2D numpy.array
        the processed numpy.array
    """
    new_arr = np.zeros((old_arr.shape[0], old_arr.shape[1]))
    new_arr[:, 0] = old_arr[:, 0]
    new_arr[:, 1] = old_arr[:, 1]
    for i in range(old_arr.shape[0]):
        for j in range(object_arr.shape[0]):
            if i == id_arr[j]:
                new_arr[i, 2] = object_arr[j]
        if new_arr[i, 2] == 0:
            new_arr[i, 2] = old_arr[i, 2]
    return new_arr






