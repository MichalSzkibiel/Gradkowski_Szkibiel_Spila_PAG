from Graph import *
import arcpy
def wizualizacja (drogi, tablica, result, id):
    tab_layer="tab_layer"#definicja pomocniczej wartstwy
    strtablica=str(tablica)#konwersja do stringa
    strtablica = "(" + strtablica[1:len(strtablica)-1]+")"
    arcpy.MakeFeatureLayer_management(drogi,tab_layer)
    arcpy.SelectLayerByAttribute_management(tab_layer,"NEW_SELECTION", id + " IN " + strtablica)#FID znajduje się w tablicy "drogi" lista wartosci w formie SQL-a
    arcpy.CopyFeatures_management(tab_layer,result)


#FeatureClass z drogami			
roads = arcpy.GetParameterAsText(0)
#Kolumna atrybutow z identyfikatorem
id = arcpy.GetParameterAsText(1)
#Kolumna atrybutow ze srednia predkoscia
avg_Speed = arcpy.GetParameterAsText(2)
#Kolumna atrybutow z kierunkami jezdni
direction = arcpy.GetParameterAsText(3)
#Punkty z poczatkiem i koncem
targets = arcpy.GetParameterAsText(4)
#Plik z wyjsciem
file = arcpy.GetParameterAsText(5)  
#Utworzenie grafu
g = Graph(roads, id, avg_Speed, direction)
#Wyciagniecie punktow z klasy targets
points = []
with arcpy.da.SearchCursor(targets, ["SHAPE@X", "SHAPE@Y"]) as sc:
    for row in sc:
        points.append([row[0], row[1]])
#Znalezienie punktow
begin = g.binary_search(points[0], 100)
end = g.binary_search(points[1], 100)
#Wyznaczenie trasy
path = g.make_path(begin, end)
#Zamiana w Shapefile
wizualizacja(roads,path,file, id)
