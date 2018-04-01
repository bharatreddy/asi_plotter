import numpy
import os
import datetime
import matplotlib.pyplot as plt
import aacgmv2
from davitpy import utils
import matplotlib.pyplot as plt
import seaborn as sns

class UtilsASI(object):
    """
    A class to Download SSUSI data
    given a date and datatype!
    """
    def __init__(self, inpDir, inpGlatFile=None, inpGlonFile=None):
        """
        Given a input dir read data from and setup base parameters
        if inpGlatFile and inpGlonFile are None then we expect to
        read glat and glon file data from the input directory.
        """
        # Have a dict store the file data
        self.asiDict = {}
        # Get glat, glon file data if they are provided externally
        if inpGlatFile is not None:
            self.glats = numpy.loadtxt(inpGlatFile)
        if inpGlonFile is not None:
            self.glons = numpy.loadtxt(inpGlonFile)
        # Loop through the directory and parse dates
        # from the files!
        for pFn in os.listdir(inpDir):
            if os.path.isfile(inpDir + pFn):
                # check if the file is a pixel file
                # or a glat/glon file or some random
                # file which we don't need
                if "glat" in pFn:
                    if inpGlatFile is None:
                        self.glats = numpy.loadtxt(inpDir + pFn)
                elif "glon" in pFn:
                    if inpGlonFile is None:
                        self.glons = numpy.loadtxt(inpDir + pFn)
                else:
                    fNameList = pFn.split("_")
                    # Now check if the first element
                    # is a digit (date)!
                    if fNameList[0].isdigit():
                        # Now get the date of the image
                        fDate = datetime.datetime.strptime(\
                                    fNameList[0], "%Y%m%d%H%M%S" )
                        self.asiDict[fDate] = numpy.loadtxt(inpDir + pFn)

        if self.glats.shape != self.glons.shape:
            print "glats and glons are not the same size!!".upper()

    def convert_geo_to_aacgm(self, glat, glon, inpTime):
        """
        Get MLAT, MLON, MLT from GLAT, GLON
        and time!
        """
        mlat, mlon = aacgmv2.convert(glat,\
                            glon, 300., inpTime)
        mlt = aacgmv2.convert_mlt(\
                mlon, inpTime, m2a=False)
        return mlat, mlon, mlt

    def overlay_asi_data(self, mapHandle, ax, inpTime=None, coords="mlt", overlayTime=True,\
                        timeColor="black", timeFontSize=8., zorder=5., timeZorder=7.,\
                         plotCBar=True, logScale=True, autoScale=True, vmin=0., vmax=10.,\
                         plotTitle=True, titleString=None, alpha=0.7, ssusiCmap="Oranges"):
        """
        Overlay ASI data on map
        """
        # Select the closest time based on the input time
        if coords == "mlt":
            if inpTime is None:
                print "need to enter inpTime for mlt coords"
        # get closest time
        delTimes = numpy.array( [ abs( (dd - inpTime).total_seconds() ) for\
                     dd in self.asiDict.keys() ] )
        selTimeIndex = numpy.argmin( delTimes )
        mapTime = self.asiDict.keys()[selTimeIndex]
        if mapTime != inpTime:
            print "closest map time --->", mapTime
        # get pixel data
        if logScale:
            pixData = numpy.log( self.asiDict[ mapTime ] )
        else:
            pixData = self.asiDict[ mapTime ]

        if autoScale:
            vmin = 0.
            vmax = numpy.round( numpy.max( pixData )/5. )*5.
        # get appropriate lat/lon data
        if coords != "geo":
            mlats = numpy.zeros(shape=self.glats.shape)
            mlons = numpy.zeros(shape=self.glats.shape)
            mlts = numpy.zeros(shape=self.glats.shape)
            for x in xrange(self.glats.shape[0]):
                for y in xrange(self.glats.shape[1]):
                    mlats[x,y], mlons[x,y], mlts[x,y] =\
                            self.convert_geo_to_aacgm(\
                                self.glats[x,y], self.glons[x,y], inpTime )
        if coords == "geo":
            asiLats = self.glats
            asiLons = self.glons
        else:
            asiLats = mlats
            if coords == "mag":
                asiLons = mlons
            else:
                asiLons = mlts*15.
        # Remove nan's and inf values
        asiLats = numpy.ma.masked_where(\
                numpy.isnan(asiLats),asiLats)
        asiLons = numpy.ma.masked_where(\
                        numpy.isnan(asiLons),asiLons)
        xVecs, yVecs = mapHandle(asiLons, asiLats,\
                                 coords=coords)        
        asiPix = numpy.ma.masked_where(numpy.isinf(pixData),pixData)
        asiPlot = mapHandle.pcolor(xVecs, yVecs,\
                            asiPix, zorder=8,
                            vmin=vmin, vmax=vmax,
                            ax=ax, alpha=alpha, cmap=ssusiCmap)




