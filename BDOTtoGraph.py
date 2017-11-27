import Graph
import arcpy

#FeatureClass z drogami			
roads = arcpy.GetParameterAsText(0)
#Kolumna atrybutow z identyfikatorem
id = arcpy.GetParameterAsText(1)
#Kolumna atrybutow ze srednia predkoscia
avg_Speed = arcpy.GetParameterAsText(2)
#Kolumna atrybutow z kierunkami jezdni
direction = arcpy.GetParameterAsText(3)
#Plik tekstowy do zapisu struktury grafu
file = arcpy.GetParameterAsText(4)
#Stworzenie grafu
g = Graph(roads, id, avg_Speed, direction)
#Zapisanie grafu do pliku tekstowego
g.export(file)
