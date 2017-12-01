import arcpy
import math
from Queue import Queue

def isClose(first, second, maxDiff):
    #Funkcja sprawdzajaca czy dwa elementy (first, second) roznia sie najwyzej o maxDiff
    return abs(first - second) < maxDiff

def isClose2(first, second, maxDiff):
    #Funkcja sprawdzajaca czy dwa dwumiarowe punkty (first, second) sa od siebie odlegle najwyzej o maxDiff
    el0 = first[0] - second[0]
    el1 = first[1] - second[1]
    sqrt = math.sqrt(el0**2 + el1**2)
    return sqrt < maxDiff

class Graph:
    #Klasa przechowujaca siec drog w formie grafu
	#Skladowe:
	#    pointCoords - tabela przechowujaca dane o skrzyzowaniach: id, wspolrzedna X, wspolrzedna Y
	#    edges - tabela przechowujaca dane o polaczeniach: id, poczatek, koniec

    def __init__(self):
	    #Konstruktor domyslny
        self.pointCoords = []
        self.edges = [[[]]]
    def insert_point(self, point):
	    #Funkcja wstawiajaca nowy punkt do tablicy
		#Punkty sa posegregowane wedlug sumy wspolrzednych X i Y
        X = point[0]
        Y = point[1]
        dist = X + Y;
        n = len(self.pointCoords)
        if n == 0:
		    #Jesli jest to pierwszy punkt, to po prostu go wstawiamy do tabeli
            self.pointCoords = [[0, X, Y]]
            return self
		#Szukanie wlasciwej pozycji do wstawienia poprzez wyszukiwanie binarne
        first = 0
        last = n - 1
        while first <= last:
            midpoint = (first + last)//2
            dist2 = self.pointCoords[midpoint][1] + self.pointCoords[midpoint][2]
            if (dist < dist2):
                if (midpoint == 0):
                    self.pointCoords = [[n, X, Y]] + self.pointCoords
                    return self
                last = midpoint - 1
            elif (dist >= dist2):
                if (midpoint == n-1):
                    self.pointCoords.append([n, X, Y])
                    return self
                dist3 = self.pointCoords[midpoint + 1][1] + self.pointCoords[midpoint + 1][2]
                if (dist < dist3):
                    self.pointCoords = self.pointCoords[:midpoint + 1] + [[n, X, Y]] + self.pointCoords[midpoint + 1:]
                    return self
                else:
                    first = midpoint + 1

    def binary_search(self, point, near = 3):
	    #Funkcja sluzy do sprawdzenia, czy dany punkt nie zostal juz wprowadzony do tej tabeli.
		#Punkty sa szukane poprzez zmodyfikowane wyszukiwanie binarne. Zgodnie ze struktura tabeli najpierw
		#szukane sa punkty o bliskiej sumie wspolrzednych, a potem blisko polozone, juz wyszukiwaniem liniowym.
		#Jesli punkt zostaje znaleziony, to zostaje zwrocony jego id. Jesli nie, to zostaje zwrocony rozmiar tabeli punktow
        dist = point[0] + point[1]
        n = len(self.pointCoords)
        first = 0
        last = n-1
        found = False
        while first<=last and not found:
            midpoint = (first + last)//2
            dist2 = self.pointCoords[midpoint][1] + self.pointCoords[midpoint][2]
            if midpoint < n and isClose(dist, dist2, near) :
                i = midpoint
                while i >= 0 and isClose(dist, self.pointCoords[i][1] + self.pointCoords[i][2], near):
                    if isClose2(point, self.pointCoords[i][1:], near):
                        return self.pointCoords[i][0]
                    i -= 1
                i = midpoint + 1
                while i < n and isClose(dist, self.pointCoords[i][1] + self.pointCoords[i][2], near):
                    if isClose2(point, self.pointCoords[i][1:], near):
                        return self.pointCoords[i][0]
                    i += 1
                found = True
            else:
                if dist < dist2:
                    last = midpoint-1
                else:
                    first = midpoint+1
        return n

    def insert_edge(self, id, begin, end, length, avg_Speed, direction):
	    #Funkcja sluzaca do wstawiania nowych polaczen
        n = len(self.pointCoords)
		#Sprawdzenie, czy poczatek zostal juz wprowadzony
        begIdx = self.binary_search(begin)
		#Jesli nie, to powinien byc wstawiony do tabeli punktow
        if (begIdx == n):
            self = self.insert_point(begin)
            n += 1
	    #Analogicznie dla konca
        endIdx = self.binary_search(end)
        if (endIdx == n):
            self = self.insert_point(end)
            n += 1
	    #Wstawienie do tabeli polaczen
	if begin >=len(self.edges):
            self.edges.append([[end,id,length, avg_Speed, direction]])
        else:
            self.edges[begin].append([end,id,length, avg_Speed, direction])
        if end >=len(self.edges):
            self.edges.append([[begin,id,length, avg_Speed, direction]])
        else:
            self.edges[end].append([begin,id,length, avg_Speed, direction])
        #self.edges.append([id, begIdx, endIdx, length, avg_Speed, direction])
        return self
		
    def export(self, file):
	    #Funkcja zapisujaca graf do wskazanego pliku tekstowego file
        stream = open(file, "w")
        stream.write(str(self.pointCoords) + "\n")
        stream.write(str(self.edges))
        stream.close()
    def __init__(self, lines, id, avg_Speed, direction):
	    #Konstruktor grafu, ktorego parametrem jest warstwa "OT_SKDR_L" z BDOTu ze wzbogaconymi atrybutami w formie FeatureClassy
        self.pointCoords = []
        self.edges = [[[]]]
        count = float(arcpy.GetCount_management(lines).getOutput(0))
        i = 0.0
		#Wybor argumentow istotnych dla problemu
        with arcpy.da.SearchCursor(lines, ["SHAPE@", id, "SHAPE@LENGTH", avg_Speed, direction]) as sc:
            for line in sc:
                i += 1.0
				#Pobor argumentow
                geom = line[0]
                id = line[1]
		length = line[2]
		avg_Speed = line[3]
		direction = line[4]
				
				#Inicjalizacja
                begin = [0,0]
                end = [1,1]	
				#Znalezienie pierwszego i ostatniego punktu geometrii
                for part in geom:
                    begin = [part[0].X, part[0].Y]
                    end = [part[len(part) - 1].X, part[len(part) - 1].Y]
					
				#Wstawienie nowego polaczenia
                self = self.insert_edge(id, begin, end, length, avg_Speed, direction)
                if i % 1000 == 0:
                    arcpy.AddMessage("Wpisano " + str(i/count*100) + "% drog")

    def make_path(self, begin, end):
        # Interfejs do znajdowania sciezki za pomoca algorytmu BFS
        #    begin - punkt poczatkowy sciezki
        #    end - punkt koncowy sciezki
        # Przeprowadzenie algorytmu BFS
        come_from = self.BFS(begin, end)
        # Wynikiem jest tablica trojek odleglosc, pochodzenie, krawedz
        # Jesli nie istnieje, to nie istnieje tez sciezka
        if not come_from:
            return False
        # Ulozenie sciezki
        path = [come_from[end][2]]
        current = end
        # Dodawanie kolejnych drog do sciezki dopoki nie natrafi na punkt poczatkowy
        while come_from[current][1] != begin:
            current = come_from[current][1]
            path.append(come_from[current][2])
        return path

    def BFS (self, begin, end):
        # Implementacja BFS
        # begin - punkt poczatkowy
        # end - punkt koncowy
        #Tablica odwiedzin i trojek odleglosc, pochodzenie i krawedz, inicjalizacja
        visited = []
        come_from = [[]]
        for el in self.pointCoords:
            visited.append(False)
            come_from.append([None, None, None])
        #Stworzenie kolejki wyszukiwania i operacje zwiazane z pierwszym punktem
        q = Queue()
        q.put(begin)
        visited[begin] = True
        #Ustawienie pochodzenia punktu poczatkowego na samego siebie
        come_from[begin] = [0, begin]
        #Dopoki kolejka nie pusta
        while not q.empty():
          #Pobierz pierwszy element
          current = q.get()
          for el in self.edges[current]:
            #Sprawdzenie krawedzi wychodzacych z danego punktu
            if not visited[el[0]]:
                #Dodanie do kolejki i aktualizacja tablic
                q.put(el[0])
                visited[el[0]] = True
                come_from[el[0]] = [come_from[current][0] + 1, current, el[1]]
                #Jesli napotkany koniec to zwracamy come_from
                if el[0] == end:
                    return come_from
        return False
