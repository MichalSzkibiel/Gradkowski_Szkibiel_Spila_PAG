from Graph import *
import arcpy
arcpy.env.overwriteOutput = True
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
#Geometria konca
target = arcpy.GetParameterAsText(5)
if target == "":
    target = targets
#Pobranie trybu
algorithm = arcpy.GetParameterAsText(6)
ignore_direct = arcpy.GetParameterAsText(7)
time_or_dist = arcpy.GetParameterAsText(8)
#FeatureDataset z wyjsciem
dat = arcpy.GetParameterAsText(9)
i = len(dat)
while i > 0:
   i -= 1
   if dat[i] == "\\" or dat[i] == "/":
       break
arcpy.CreateFeatureDataset_management(dat[:i], dat[i+1:])
file_path = dat + "\\path"
file_target = dat + "\\target"
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
wizualizacja(roads,path,file_path, id)
#Jezeli inna niz punkt koncowy, to zamien na linie
if target != targets:
    temp = "toLine"
    arcpy.FeatureToLine_management([target], temp)
    target = temp
#Ustalenie celu na granicy poligonu
arcpy.Intersect_analysis([file_path, target], file_target, "ONLY_FID", None, "POINT")

if target == "toLine":
   arcpy.Delete_management(target)