import asi_utils
import datetime
import matplotlib.pyplot as plt
from davitpy import utils

# plotting variables
inpDir = "../data/"
inpTime = datetime.datetime(2014,12,14,22)
coords = "mlt"
# setup the asi object
asiObj = asi_utils.UtilsASI(inpDir)
# A sample map
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1,1,1)
mh = utils.plotUtils.mapObj(boundinglat=40., coords=coords,\
             lat_0=90., lon_0=0, datetime=inpTime)
# DIFFERENT PLOTTING OPTIONS
### 1) Create multipage pdf with all files in folder ###
asiObj.plot_all_asi()
### Create multipage pdf with all files in folder ###

### 2) Overlay sample data for a given timeinstance ###
asiObj.overlay_asi_data(mh, ax, inpTime=inpTime)
fig.savefig("../sample_figs/sampleASI-" +\
             inpTime.strftime("%Y%d%m-%H%M") + ".pdf",\
            bbox_inches='tight')
### Overlay sample data for a given timeinstance ###

