"""
The name of this module, right now, is a lie.
It actually selects points as close as possible to
the cross section that you select using nearest neighbour, and it plots them.
"""


import xarray as xr
import nearest_neighbour as nn
import numpy as np
import matplotlib.pyplot as plt

def linear_equation_from_points(lat_init, lat_end, lon_init, lon_end):
    """
    Find the linear equation from two points.
    lat = m * lon + lat_init
    """

    if lon_init == lon_end:
        return "vertical line, no equation possible"
    if lat_init == lat_end:
        print("Horizontal line, is a constant.")
        return {"slope": 0, "intercept": lat_init}
    slope = (lat_end - lat_init)/(lon_end - lon_init)
    if lon_init == 0:
        intercept = lat_init
    elif lon_end == 0:
        intercept = lat_end
    else:
        intercept = lat_init / (slope * lon_init)
    return {"slope": slope, "intercept": intercept}

def cross_section_points(lat_init, lat_end, lon_init, lon_end, step):
    """
    Selects all points using nearest neighbour.
    step should be in degrees.
    If both lat and lon change from init to end,
    step should be the step in longitude. lat will adatp
    to that.
    """
    if lat_init == lat_end:
        lons = np.arange(lon_init, lon_end+step, step)
        lats = np.ones(len(lons)) * lat_init
    elif lon_init == lon_end:
        lats = np.arange(lat_init, lat_end+step, step)
        lons = np.ones(len(lats)) * lon_init
    else:
        return "The function isn't ready yet for a diagonal cross section.\nComing soon!"

    print("lats", lats)
    print("lons", lons)
    lonlat = np.stack((lons, lats), axis=1)
    return lonlat

def main():
    test = cross_section_points(-10, 10, -50, -50, 1)
    display(test)

#! =================================================
if __name__ == "__main__":
    main()
