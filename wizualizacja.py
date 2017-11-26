import arcpy
def wizualizacja (tablica, drogi,result):
    arcpy.MakeFeatureLayer_management(drogi,tab_layer)
    SelectLayerByAttribute_management(tab_layer,"NEW_SELECTION","","","FID IN (SELECT FID FROM tablica)")#FID znajduje się w tablicy "tablica"
    arcpy.CopyFeatures_management(tab_layer,result)

