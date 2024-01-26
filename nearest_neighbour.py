import numpy as np
import xarray as xr

def spherical_distance(lat_target, lon_target, ds_model):
    """
    Calculate distance to model output.
    Nice thing about the cos function: wrapping around
    360 is not really necessary.
    """
    R = 6_371_000 # mean earth radius

    lat_target = np.deg2rad(lat_target)
    lon_target = np.deg2rad(lon_target)
    lat_model = np.deg2rad(ds_model["lat"])
    lon_model = np.deg2rad(ds_model["lon"])
    delta_lon = lon_target - lon_model
    angular_distance = np.arccos(
        np.sin(lat_target) * np.sin(lat_model) +
        np.cos(lat_target) * np.cos(lat_model) * np.cos(delta_lon)
    )

    distance = R * angular_distance
    distance = distance.assign_coords(ncol=ds_model["ncol"].values)
    return distance


def nearest_neighbour_index(lat_target, lon_target, ds_model):
    """
    Calculate the index of the nearest neighbour
    """
    distance = spherical_distance(lat_target, lon_target, ds_model)
    return int(distance.idxmin(dim="ncol"))


def nearest_neighbour_val(variable, lat_target, lon_target, ds_model):
    """
    Return values at nearest neighbour
    """
    ncol = nearest_neighbour_index(lat_target, lon_target, ds_model)
    print(ncol)
    data = ds_model[variable].sel(ncol=ncol)
    return data
