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
#Pobranie trybu
algorithm = arcpy.GetParameterAsText(5)
ignore_direct = arcpy.GetParameterAsText(6)
time_or_dist = arcpy.GetParameterAsText(7)
#Plik z wyjsciem
file = arcpy.GetParameterAsText(8)  
#Utworzenie grafu
g = Graph(roads, id, avg_Speed, direction)
#Wyciagniecie punktow z klasy targets
points = []
with arcpy.da.SearchCursor(targets, ["SHAPE@X", "SHAPE@Y"]) as sc:
    for row in sc:
        points.append([row[0], row[1]])
#Znalezienie punktow
begin = g.search(points[0])
end = g.search(points[1])
arcpy.AddMessage(str(begin) + " " + str(end))
#Wyznaczenie trasy
path = g.make_path(begin, end, [algorithm, ignore_direct, time_or_dist])
#Zamiana w Shapefile
wizualizacja(roads,path,file, id)
