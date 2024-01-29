import xarray as xr
import matplotlib.pyplot as plt
import cmcrameri.cm as cm
from vertical_crossection import ncol_crossection, cross_section_points
import glob


def main() -> None:
    abc = "abcdefghijklmnopqrstuvwxyz"
    lonlat = cross_section_points(
        lat_init=-56, lat_end=19, lon_init=-31, lon_end=-31, step=0.25
    )
    months = sorted(glob.glob("f.e23.FCHIST.ne0np4SAMne30x4.MERRA2.firecorrect.tstep450.cam.h0.2019-*.nc"))
    fig, axs = plt.subplots(figsize=(8,7.5), nrows=4, ncols=3, sharex=True, sharey=True)
    axs = axs.flatten()
    for i,f in enumerate(months):
        ds = xr.open_dataset(f)
        list_ncol = ncol_crossection(lonlat, ds_model=ds)
        co = ds["CO"][0,:,:].sel(ncol=list_ncol) * 1e9
        lat = ds["lat"].sel(ncol=list_ncol)
        lon = ds["lon"].sel(ncol=list_ncol)
        print(lat.values)
        print(lon.values)
        pressure = ds["lev"]
        cmesh = axs[i].pcolormesh(lat, pressure, co, vmax=250, cmap=cm.hawaii_r)
        axs[i].set_ylim(bottom=200, top=1000)
        axs[i].invert_yaxis()
        axs[i].text(
            0.99, 0.99, "lon=-31°", ha='right', va="top", transform=axs[i].transAxes
                )
        axs[i].set_title(f"2019-{i:02d}", fontsize=10)
        axs[i].set_title(abc[i]+")", loc="left", fontsize=10)
    axs[-2].set_xlabel("Latitude (degrees north)")
    fig.subplots_adjust(bottom=0.18, top=0.95, left=0.1, right=0.95,
                        wspace=0.3, hspace=0.2)

    cbar_ax = fig.add_axes([0.2, 0.08, 0.6, 0.02])
    cbar = fig.colorbar(
    cmesh,
    cax = cbar_ax,
    orientation = "horizontal",
    label = "ppbv",
    #ticks = np.linspace(cmin, cmax, nlev + 1, dtype=ltype),
    extend = "max",
)
    fig.savefig("cross_section_atlantic_monthly.png")



#====================================
if __name__ == "__main__":
    main()
