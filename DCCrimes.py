# Name: Aaron Gibson
# Created Date: 11/19/21
# Last Modified Date: 11/20/21
# Description: This program takes information from a CSV file and creates a point shapefile of the crimes committed in
# the Washington DC area.

# imports modules, allows program to overwrite
import arcpy, os
arcpy.overwriteOutput = True

# gets parameters from the script tool in ArcGIS, saves as variable value
outFC = arcpy.GetParameterAsText(0)
inFile = arcpy.GetParameterAsText(1)
coordsys = arcpy.GetParameterAsText(2)

# sets workspace and the variable featClass, deletes featClass if it exists
arcpy.env.workspace = os.path.dirname(outFC)
featClass = os.path.basename(outFC)

if arcpy.Exists(featClass):
    arcpy.Delete_management(featClass)

# creates feature class with the parameters listed
arcpy.CreateFeatureclass_management(arcpy.env.workspace, featClass, "POINT")
# defines the projection of the new feature class
arcpy.DefineProjection_management(featClass, coordsys)


# adds fields to the feature class attribute table
arcpy.AddField_management(featClass, "OFFENSE", "text", "50")
arcpy.AddField_management(featClass, "METHOD", "text", "50")
arcpy.AddField_management(featClass, "DISTRICT", "text", "50")

# opens txt file and reads the line, closes polygon and sets the split as |
txtFile = open(inFile, 'r')
# reads the first line in txtFile
headerLine = txtFile.readline()
# separates the fields in the headerline into a list
lstValue = headerLine.split(",")

# sets value of variables based on the the value in the table index, closes csv file
latIndex = lstValue.index("LATITUDE")
longIndex = lstValue.index("LONGITUDE")
distIndex = lstValue.index("DISTRICT")
offenseIndex = lstValue.index("OFFENSE")
methodIndex = lstValue.index("METHOD")
lines = txtFile.readlines()
txtFile.close()

# saves attribute fields as a list
fieldList = ["ID", "DISTRICT", "OFFENSE", "METHOD", "SHAPE@",]
# counting number to be used as ID
pid = 1

# insert cursor to add data into the table
with arcpy.da.InsertCursor(featClass, fieldList) as isCursor:
# checks if the points has a value for latitude and longitude, if not the row is skipped
    for line in lines:
        if latIndex == int(0):
            continue
        if longIndex == int(0):
            continue
# uses comma to split the line, saves field data as variables, adds one to the counting variable
        data = line.split(",")
        lat = float(data[latIndex])
        long = float(data[longIndex])
        district = data[distIndex]
        offense = data[offenseIndex]
        method = data[methodIndex]
        pid = pid + 1

# sets variable newPoint as a list of the fields and inserts the new row into the table, prints what records are written
        newPoint = [pid, district, offense, method, arcpy.Point(long, lat)]
        isCursor.insertRow(newPoint)
        # arcpy.AddMessage("Record Number {0} written to feature class".format(pid))
        # commented this message out because it produced a lot of messages, used it during testing to make sure all
        # the records were being written.


# prints message saying the process is complete, cleans up insert cursor.
arcpy.AddMessage("Process complete")
del isCursor