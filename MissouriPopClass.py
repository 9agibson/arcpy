# Name: Aaron Gibson
# Created Date: 11/13
# Last Modified Date: 11/13
# Description: This script classifies the population of Missouri counties as High, Medium or Low, it also gets the
#               count of how many counties fall into each category

import arcpy
# gets the template feature class from the user as well as the new field to be added to the table
inputFC = arcpy.GetParameterAsText(0)
fieldNew = arcpy.GetParameterAsText(1)
# field list to be used by the cursor later
fieldList = ["NAME", "POP2000", fieldNew]
# variables that will be as temporary layers
lowLyr = "Low"
medLyr = "Medium"
highLyr = "High"
# establishes workspace from the shapefile given by the user
arcpy.env.workspace = arcpy.Describe(inputFC).path
feat_Class = arcpy.Describe(inputFC).file
# validates new field name
fieldNew = arcpy.ValidateFieldName(fieldNew)
# lists fields from the given feature
fields = arcpy.ListFields(feat_Class, fieldNew)
# if the new field name already exists in the table it is deleted and a new field is created
for fld in fields:
    arcpy.DeleteField_management(feat_Class, fieldNew)

arcpy.AddField_management(feat_Class, fieldNew, "text", "10")

# designates the update cursor, used with statement to avoid data lock
with arcpy.da.UpdateCursor(feat_Class, fieldList) as upCursor:
# iterates through the rows in the cursor designates list index as variables. if statement is used to give the new
# field a value based on the population
    for row in upCursor:

        cntyName = row[0]
        cntyPop = row[1]
        if row[1] < 10000:
            row[2] = "Low"
        elif row[1] <= 100000:
            row[2] = "Medium"
        else:
            row[2] = "High"
# updates the new field with the information from the conditional statements and prints out a statement with the
# County name, population and its new classification
        upCursor.updateRow(row)
        print("{0} has a population of {1} as {2}".format(cntyName, cntyPop, row[2]))
# deletes cursor
del upCursor
# Designates "entries" with the value of all counties
entries = arcpy.GetCount_management(feat_Class)
# deletes the lowlyr feature layer if it exists
if arcpy.Exists(lowLyr):
    arcpy.Delete_management(lowLyr)
# queries the counties that have a classification as "low", "medium" or "high"
# saves these to a temporary file to get the count of counties
# prints out the number of counties with each classification as well as the number of total counties
query = "\"{0}\" = \'Low\'".format(fieldNew)
arcpy.MakeFeatureLayer_management(feat_Class, lowLyr, query)
result = arcpy.GetCount_management(lowLyr)
print("There are {0} out of {1} with Low population".format(result, entries))

if arcpy.Exists(medLyr):
    arcpy.Delete_management(lowLyr)
query = "\"{0}\" = \'Medium\'".format(fieldNew)
arcpy.MakeFeatureLayer_management(feat_Class, medLyr, query)
result = arcpy.GetCount_management(medLyr)
print("There are {0} out of {1} with Medium population".format(result, entries))

if arcpy.Exists(highLyr):
    arcpy.Delete_management(highLyr)
query = "\"{0}\" = \'High\'".format(fieldNew)
arcpy.MakeFeatureLayer_management(feat_Class, highLyr, query)
result = arcpy.GetCount_management(highLyr)
print("There are {0} out of {1} with High population".format(result, entries))

# deletes temporary layers
arcpy.Delete_management(lowLyr)
arcpy.Delete_management(medLyr)
arcpy.Delete_management(highLyr)
