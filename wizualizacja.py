import arcpy
def wizualizacja (tablica, drogi,result):
    arcpy.MakeFeatureLayer_management(drogi,tab_layer)
    SelectLayerByAttribute_management(tab_layer,"NEW_SELECTION","","","FID IN (tablica[:])")#FID znajduje się w tablicy "drogi" lista wartosci w formie SQL-a
    arcpy.CopyFeatures_management(tab_layer,result)
	
def heurystyka(wierzcholki,krawedzie)

