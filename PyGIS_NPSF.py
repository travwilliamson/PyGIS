#-------------PyGIS NPSF & HOLDINGS----------------#
#------------------Imports-------------------------#
import arcpy, sys, os, time, getpass, time, traceback, shutil
from arcpy import env
from datetime import date
from datetime import datetime
time = datetime.now().strftime('%H:%M:%S')
time = str(time)

arcpy.env.overwriteOutputs = True
userid = getpass.getuser()

Cpath = ("C:\Users\\" + userid + "\Documents\UniversalBuffer_PDF")
if not os.path.exists(Cpath):
    os.makedirs(Cpath)
PyPath = ("C:\Users\\" + userid + "\Documents\PyGIS")
if not os.path.exists(PyPath):
    os.makedirs(PyPath)
PyData = PyPath + "/Data"
if not os.path.exists(PyData):
    os.makedirs(PyData)

holding = arcpy.GetParameterAsText(0) #FeatureLayer
reference = arcpy.GetParameterAsText(1) #String
l = int(reference)
l = len(reference)
if len(reference) == 9 or len(reference) <= 4:
    
#------------------Geoprocessing-------------------#
    try:
        arcpy.AddMessage("CREATING ARCPY ENVIRONMENT...")
        
        if len(reference) == 9:
            arcpy.AddMessage("SEARCHING FOR HOLDING REFERENCE NUMBER...")
        if len(reference) <= 4:
            arcpy.AddMessage("SEARCHING FOR NATIONAL PARK / STATE FOREST...")

        try:    
            arcpy.SelectLayerByAttribute_management(holding, "NEW_SELECTION", "Holding_Re" + '=' + reference)
        except:
            arcpy.AddMessage("FAILED TO SELECT ATTRIBUTE WITH NUMBER PROVIDED")
            
        arcpy.Buffer_analysis(holding, "output", "1 Kilometer", "FULL")
        mxd = arcpy.mapping.MapDocument('current')
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        newlayer = arcpy.mapping.Layer("output")
        arcpy.mapping.AddLayer(df, newlayer)
        mxd.save()
        arcpy.ApplySymbologyFromLayer_management("output", "Boundary_NWLLS")
        lyr = arcpy.mapping.ListLayers(mxd, "output", df)[0]
        ext = lyr.getExtent()
        df.extent = ext
        lyr.visible = True 
        table = lyr.name
        field = "Holding_Na"
        holdingname = str({row[0] for row in arcpy.da.SearchCursor(table, field)})
        name = holdingname.replace("set([u'", " ")
        newname = name.replace("'])", "")
        TextElement = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "TitleText")[0]
        TextElement.text = (newname + ' - ' + reference + '\n' + '1km Buffer')
        newname = newname.replace("/","-")
        newname = (newname + " - " + reference)
        Kpath = ("K:/North West LLS/Travis/Biosecurity/BIOSECURITY_CORPORATE/PDF/")

        dataframe = "PAGE_LAYOUT"
        arcpy.mapping.ExportToPDF(mxd, Cpath + "\\" + newname, dataframe)
        arcpy.mapping.ExportToJPEG(mxd, Kpath + newname, dataframe)
        arcpy.AddMessage("Completed for " + newname)
        today = date.today()

#------------------Write To Log Catcher----------------#
        
        author = userid
        if author == "williatr":
             author = "Moderator"
        log = ("K:/North West LLS/Travis/Biosecurity/PythonDesk K/log.txt")
        os.chmod(log, 0644)
        with open(log, 'a') as file:
            file.write("\n")
            file.write(str(today) + " PyGIS_NPSF " + ", " + time + "  " + author + "  " + newname)
        os.chmod(log, 0444)

        PyUpdates  = "K:/North West LLS/Travis/Biosecurity/PythonDesk K/PyUpdates.txt"
        shutil.copy(PyUpdates, PyPath + "/")
        
        
#------------------Error Catching----------------------#       
    except:
        tb= sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        err1 = str(tb)
        err2 = str(tbinfo)
        today = date.today()
        author = userid
        if author == "williatr":
             author = "Moderator"
        log = ("K:/North West LLS/Travis/Biosecurity/PythonDesk K/log.txt")
        os.chmod(log, 0644)
        arcpy.AddMessage(err1 + "  " + err2)
        with open(log, 'a') as file:
            file.write("\n")
            file.write(str(today) + " PyGIS_NPSF" + ", " + time + "  " + author + "  " + reference + err1  + ", " + "\n" + err2)

        os.chmod(log, 0444)

else:
    arcpy.AddMessage("\n" + "\n"+ "\n"+ "\n"+ "\n"+ "INVALID LENGTH ENTERED FOR REFERENCE NUMBER, EXPECTED: 9, RECEIVED [" + str(l) + "]" +"\n"+ "\n"+ "\n"+ "\n"+ "\n"+ "\n")


