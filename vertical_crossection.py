"""
The name of this module, right now, is a lie.
It actually selects points as close as possible to the cross section that you select using nearest neighbour, and it plots them.
"""


import xarray as xr
import nearest_neighbour as nn
import numpy as np
import matplotlib.pyplot as plt

def cross_section_points(lat_init, lat_end, lon_init, lon_end, resolution):
    """
    Selects all points using nearest neighbour.
    Resolution should be in degrees
    """
    if lat_init == lat_end:
        lons = np.arange(lon_init, lon_end+resolution, resolution)
        lats = np.ones(len(lons)) * lat_init
    elif lon_init == lon_end:
        lats = np.arange(lat_init, lat_end+resolution, resolution)
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
