import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import nearest_neighbour as nn


MOLMOL2PPB = 1e9
PA2HPA = 0.01

def vertical_levels_meters(ds_model):
    """
    Calculate all vertical levels of the model in meters.
    This assumes that the model is hydrostatic.
    See https://www.pdas.com/hydro.pdf
    """
    R_EARTH = 6375000

    height = ds_model["Z3"] * R_EARTH / (R_EARTH - ds_model["Z3"])
    height.attrs["long_name"] = "Height over sea level at mid-layer"
    height.attrs["history"] = "calcualted from Geopotential height as GPH * R / (GPH - R) with and R of 6375000"
    height.attrs["units"] = "m"
    return height

def main():
    with xr.open_dataset(
        "f.e23.FCHIST.ne0np4SAMne30x4.MERRA2.firecorrect.tstep450.cam.h0.2019-01.nc"
    ) as ds:
        lat_ZF2_monitoring = -2.64
        lon_ZF2_monitoring = -60.15
        ncol = nn.nearest_neighbour_index(
            lon_target=lon_ZF2_monitoring,
            lat_target=lat_ZF2_monitoring,
            ds_model=ds
        )
        CO = ds["CO"].sel(ncol=ncol)  * MOLMOL2PPB
        
        geometric_height = vertical_levels_meters(ds)
        geometric_height = geometric_height.sel(ncol=ncol)
        pressure = ds["PMID"].sel(ncol=ncol) * PA2HPA

        fig, axs = plt.subplots(figsize=(8, 3), ncols=2)
        axs[0].plot(CO[0,:].values, pressure[0,:].values, 'o-')
        axs[0].invert_yaxis()
        axs[0].set_xlabel("CO (ppbv)")
        axs[0].set_ylabel("pressure (hPa)")

        axs[1].plot(CO[0,:].values, geometric_height[0,:], 'o-')
        axs[1].set_xlabel("CO (ppbv)")
        axs[1].set_ylabel("height (m)")
        
        fig.tight_layout()
        fig.savefig("vertical_profile_ZF2.png")

#! ===================================================================
if __name__ == "__main__":
    main()
