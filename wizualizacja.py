import arcpy
def wizualizacja (drogi, tab_layer,result):
    arcpy.MakeFeatureLayer_management(drogi,tab_layer)
    SelectLayerByAttribute_management(tab_layer,"NEW_SELECTION","FID IN (FID)")#FID znajduje się w tablicy "drogi"
    arcpy.CopyFeatures_management(tab_layer,result)

#Okreslenie nazwy layera
tab_layer = "trasa_lyr"    
#Wywolanie we skrypcie find_path    
#Zamiana w Shapefile
result=wizualizacja(roads,tab_layer,file)
