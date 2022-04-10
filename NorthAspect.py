# Name: Aaron Gibson
# Created Date: 11/21/21
# Last Modified Date: 11/21/21
# Description: This program generates a north facing aspect raster based on input data.

# imports modules and specific classes, allows program to overwrite.
import arcpy, os
from arcpy import env
from arcpy.sa import *
env.overwriteOutput = True

# gets the elevation raster and output file name from the user
elevation = arcpy.GetParameterAsText(0)
outRaster = arcpy.GetParameterAsText(1)

# sets the workspace as the path of the elevation raster as well as saves the basename of the elevation raster and the
# output name
env.workspace = os.path.dirname(elevation)
inputElev = os.path.basename(elevation)
saveReclass = os.path.basename(outRaster)


# gets the aspect from the elevation dataset
outAspect = Aspect(inputElev)


# sets the range for north facing aspect
northRangeone = 22.5
northRangetwo = 337.5
negative = -1
# retrieves spatial extension
arcpy.CheckOutExtension("Spatial")
# north one gets the desired aspect value in the range of 0 - 22.5, northtwo gets aspect higher than 337.5
northone = (Raster(outAspect) < northRangeone) & (Raster(outAspect) > negative)
northtwo = Raster(outAspect) > northRangetwo
# saves the desired aspect values to a variable
newAspect = northone | northtwo

# remaps the data to save only the cells that returned true, reclassifies the newAspect raster and saves it as the
# output name
remap = arcpy.sa.RemapValue([[0, "NODATA"], [1, 1]])
outReclassify = Reclassify(newAspect, "Value", remap, "NODATA")
outReclassify.save(saveReclass)
# returns spatial extension
arcpy.CheckInExtension("Spatial")

# cleans up temp files
del outAspect, newAspect
