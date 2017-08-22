#-----------------------PyFix----------------------#
#----------------------Imports---------------------#
import arcpy, sys, os, time, getpass, time, traceback
from arcpy import env
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
arcpy.env.overwriteOutputs = True

#----------------------Setting Time----------------#
month = datetime.now().strftime('%B')
year = datetime.now().strftime('%Y')
lastmonth = datetime.now() - relativedelta(months=1)
lastmonth = format(lastmonth, '%B' + "_" + '%Y')
thismonth = month + "_" + year
time = datetime.now().strftime('%H:%M:%S')
time = str(time)


Kpath = ("K:/North West LLS/Travis/Biosecurity/BIOSECURITY_CORPORATE/Holdings/")

Current = Kpath + thismonth
month = thismonth
if not os.path.exists(Current):
    Current = (Kpath + lastmonth)
    month = lastmonth
    if not os.path.exists(Current):
        arcpy.AddMessage("NO HOLDINGS AVAILABLE FOR UPDATE")
name = "Holdings_NPSF_" + month
userid = getpass.getuser()

#--------------------Setting Folders--------------#
Path = "C:/Users/" + userid + "/Documents/"

Cpath = (Path + "UniversalBuffer_PDF")
if not os.path.exists(Cpath):
    os.makedirs(Cpath)
PyPath = (Path + "PyGIS/")
if not os.path.exists(PyPath):
    os.makedirs(PyPath)
PyData = PyPath + "Data/"
if not os.path.exists(PyData):
    os.makedirs(PyData)
                   
arcpy.env.workspace = PyData
layerx = arcpy.GetParameterAsText(0) #FeatureLayer

#------------------Update Holdings-----------------#

desc = arcpy.Describe(layerx)
layersource = desc.catalogPath
layerpath = (Kpath + month + "/" + name)

if layersource.endswith(month + ".shp"):
    arcpy.AddMessage("ALREADY HAVE RECENT HOLDING LAYER")
else:
    mxd = arcpy.mapping.MapDocument('current')
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    layer = (layerpath + ".shp")
    layerpath.replace("/", "\\")
    arcpy.CopyFeatures_management(layerpath +".shp", PyData + "Holdings_NPSF_August_2017.shp")
    newlayer = arcpy.mapping.Layer(PyData + "Holdings_NPSF_August_2017.shp")
    arcpy.mapping.AddLayer(df, newlayer)
    arcpy.ApplySymbologyFromLayer_management(name, layerx)

        # Move Layer in ToC
    for lyr in arcpy.mapping.ListLayers(mxd, "Hold*", df):
        if lyr.name == name:
            move = lyr
            arcpy.AddMessage(lyr.name)
        ref = lyr
        arcpy.AddMessage(ref)
    arcpy.mapping.MoveLayer(df, ref, move, "BEFORE")
    
    for lyr in arcpy.mapping.ListLayers(mxd, "Hold*", df):
        if lyr.name == name:
            print "Nothing"
        else:
            arcpy.mapping.RemoveLayer(df, lyr)  
    
    arcpy.RefreshTOC()
    mxd.save()
    arcpy.AddMessage("YOU WILL NEED TO MANUALLY TURN YOUR HOLDINGS LABELS ON")

#------------------Write To Log Catcher----------------#
                     
today = date.today()        
author = userid
if author == "williatr":
        author = "Moderator"
log = ("K:/North West LLS/Travis/Biosecurity/PythonDesk K/log.txt")
os.chmod(log, 0644)
with open(log, 'a') as file:
    file.write("\n")
    file.write(str(today) + " PyFix " + ", " + time + "  " + author)
os.chmod(log, 0444)





                
