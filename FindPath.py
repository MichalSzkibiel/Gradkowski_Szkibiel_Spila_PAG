from Graph import *
import arcpy
def wizualizacja (drogi, tab_layer,result):
    arcpy.MakeFeatureLayer_management(drogi,tab_layer)
    SelectLayerByAttribute_management(tab_layer,"NEW_SELECTION","FID IN (FID)")#FID znajduje się w tablicy "drogi"
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
#Okreslenie nazwy layera
tab_layer = "trasa_lyr"    
#Wywolanie we skrypcie find_path    
#Zamiana w Shapefile
result=wizualizacja(roads,tab_layer,file)
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
arcpy.AddMessage(str(begin) + " " + str(end))
#Wyznaczenie trasy
path = g.make_path(begin, end)
#Zapis do pliku
stream = open(file, 'w')
stream.write(str(path))
stream.close()
