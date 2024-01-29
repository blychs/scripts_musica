"""
The name of this module, right now, is a lie.
It actually selects points as close as possible to
the cross section that you select using nearest neighbour.
"""

import xarray as xr
import nearest_neighbour as nn
import numpy as np
import numpy.typing as npt


def linear_equation_from_points(lat_init, lat_end, lon_init, lon_end) -> tuple:
    """
    Find the linear equation from two points.
    lat = m * lon + lat_init
    returns slope, intercept
    """

    if (lon_init == lon_end) and (lat_init == lat_end):
        raise Exception("Initial and final coordinates are the same. No line is possible.")
    if lon_init == lon_end:
        raise Exception("vertical line, no equation possible")
    if lat_init == lat_end:
        print("Horizontal line, is a constant.")
        slope, intercept = 0, lat_init
        return slope, intercept
    slope = (lat_end - lat_init)/(lon_end - lon_init)
    if lon_init == 0:
        intercept = lat_init
    elif lon_end == 0:
        intercept = lat_end
    else:
        intercept = lat_init - (slope * lon_init)
    return slope, intercept
def cross_section_points(lat_init, lat_end, lon_init, lon_end, step) -> npt.NDArray:
    """
    Selects all points using nearest neighbour.
    step should be in degrees.
    If both lat and lon change from init to end,
    step should be the step in longitude. lat will adatp
    to that.
    """
    if lon_init > lon_end:
        raise Exception("Initial longitude should be less or equal than final longitude.")
    if lat_init > lat_end:
        raise Exception("Initial latitude should be less or equal than final latitude.")
    if lat_init == lat_end:
        lons = np.arange(lon_init, lon_end+step, step)
        lats = np.ones(len(lons)) * lat_init
    elif lon_init == lon_end:
        lats = np.arange(lat_init, lat_end+step, step)
        lons = np.ones(len(lats)) * lon_init
    else:
        slope, intercept = linear_equation_from_points(
            lat_init=lat_init, lon_init=lon_init,
            lat_end=lat_end, lon_end=lon_end
        )
        lons = np.arange(lon_init, lon_end+step, step)
        lats = slope * lons + intercept

    lonlat = np.stack((lons, lats), axis=1)
    return lonlat


def ncol_crossection(lonlat, ds_model) -> list:
    """
    Creates an array with all the crossection points 
    in the model using nearest neighbour
    It returns a list of ncol
    """
    ncol_list = []
    for coordinate in  lonlat:
        ncol_list.append(
            nn.nearest_neighbour_index(
            lon_target = coordinate[0],
            lat_target = coordinate[1],
            ds_model=ds_model
            )
        )
    return ncol_list
    
