import arcpy
<<<<<<< HEAD
def wizualizacja (drogi, tab_layer,result):
    tab_layer="tab_layer"#definicja pomocniczej wartstwy
    strtablica=str(tablica)#konwersja do stringa
    strtablica = "(" + strtablica[1:len(strtablica)-2]+")"#usuniecie ze stringa cudzyslowow
    arcpy.MakeFeatureLayer_management(drogi,tab_layer)
    arcpy.SelectLayerByAttribute_management(tab_layer,"NEW_SELECTION","FID IN " + strtablica)#FID znajduje się w tablicy "drogi"
    arcpy.CopyFeatures_management(tab_layer,result)
  
#Zamiana w Shapefile
result=wizualizacja(roads,path,file)
=======
def wizualizacja (tablica, drogi,result):
    arcpy.MakeFeatureLayer_management(drogi,tab_layer)
    SelectLayerByAttribute_management(tab_layer,"NEW_SELECTION","","","FID IN (tablica[:])")#FID znajduje się w tablicy "drogi" lista wartosci w formie SQL-a
    arcpy.CopyFeatures_management(tab_layer,result)
	
def heurystyka(wierzcholki,krawedzie)

>>>>>>> Work_CharliesSp
