import numpy as np
import xarray as xr
import nearest_neighbour as nn

ds = xr.open_dataset("f.e23.FCHIST.ne0np4SAMne30x4.MERRA2.firecorrect.tstep450.cam.h0.2019-08.nc")

CO = nn.nearest_neighbour_val(ds["CO"], lat_target=-34, lon_target=-58, ds_model=ds)

print(CO)
