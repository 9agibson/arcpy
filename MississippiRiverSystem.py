# Name: Aaron Gibson
# Created Date: 11/10
# Last Modified Date: 11/11
# Description: This script makes a nes shapefile of the states associated with the Mississippi river system. It also
# copies fields to a new table specific to those states and their population.

# imports arcpy modules
import arcpy
# establishes workspace and allows the program to overwrite
arcpy.env.workspace= r"C:\Geoprocessing with Python\Practice10\Data"
arcpy.env.overwriteOutput = True
# specifies the files that will be used by the program and assigns them to variables
states_feat = "States.shp"
rivers_feat = "rivers.shp"
# gives a value to the new files that will be created as the program runs
st_layer = "States"
riv_system = "Mississippi"
pop_layer = "Population"
out_feat = "Mississippi.shp"
out_table = "POPMiss.dbf"
# Deletes the file if they exist and makes the new st_layer feature layer
if arcpy.Exists(st_layer):
    arcpy.Delete_management(st_layer)
arcpy.MakeFeatureLayer_management(states_feat, st_layer,)
# deletes riv_system if it exists, runs a query to find the rivers in the Mississippi system, creates the riv_system feature class
if arcpy.Exists(riv_system):
    arcpy.Delete_management(riv_system)
query = '"SYSTEM" = \'Mississippi\''
arcpy.MakeFeatureLayer_management(rivers_feat, riv_system, query)
# selects features in the st_layer associated with the mississippi river system
# i tried several other selection types but this was the only one that I could get to work. if it seems like
# a strange way to select the states this is why
arcpy.SelectLayerByLocation_management(st_layer, "WITHIN_A_DISTANCE", riv_system, "1 MILES")
# copies the selected features to the out_feat shape file
arcpy.CopyFeatures_management(st_layer, out_feat)
# gets the count of states selected and sets that as the "result" variable
result = arcpy.GetCount_management(out_feat)
# prints the result and a message saying that the feature layer was copied.
print("There are {0} states associated with the {1} river system".format(result, riv_system))
print("Copy the feature layer {0} to the feature class {1}".format(st_layer, out_feat))
# deletes pop_layer if it exists and makes a new feature layer under that name
if arcpy.Exists(pop_layer):
    arcpy.Delete_management(pop_layer)
arcpy.MakeFeatureLayer_management(out_feat, pop_layer)
# queries fields that have a population more than 10000000
query = '"POP2008" > 10000000'
# selects the queried fields as a new selection
arcpy.SelectLayerByAttribute_management(pop_layer, "NEW_SELECTION", query)
# gets the count of the selected fields and assigns it as a value to the result variable
result = arcpy.GetCount_management(pop_layer)
# prints the number of selected states in the river system
print("There are {0} states in {1} River System with 2008 Population more than 10,000,000".format(result, riv_system))
# Copies the selected rows to the new "out_table" and prints a message saying that the attributes were copied.
arcpy.CopyRows_management(pop_layer, out_table)
print("Copy the attributes from the feature layer {0} to the table {1}".format(st_layer, out_table))
# deletes temporary files.
arcpy.Delete_management(st_layer)
arcpy.Delete_management(riv_system)
arcpy.Delete_management(pop_layer)



