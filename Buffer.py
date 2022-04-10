import arcpy, os, sys

# gets variable values from the user for both geoprocessing functions
inFeature = arcpy.GetParameterAsText(0)
bufDistance = arcpy.GetParameterAsText(1)
eraseFeatures = arcpy.GetParameterAsText(2)
outWorkspace = arcpy.GetParameterAsText(3)
outName = arcpy.GetParameterAsText(4)

# allows the script to overwrite output results
arcpy.env.overwriteOutput = True

# Tells the script where to save the output file resulting from the script
Buffer_Output = outWorkspace + os.sep + outName + "buf"
Erase_Output = outWorkspace + os.sep + outName

# Runs the buffer and erase functions with the information given by the user and some variables that are hardcoded in.
arcpy.analysis.Buffer(inFeature, Buffer_Output, bufDistance, "Full", "ROUND", "All", "")
arcpy.analysis.Erase(eraseFeatures, Buffer_Output, Erase_Output)

# adds message to let the user know that the script is done running.
arcpy.AddMessage("All Done")