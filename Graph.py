import arcpy
import math
from Queue import *

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
	#    pointCoords - slownik, klucz: wspolrzedne, wartosc: id
	#    edges - lista sasiedztwa. Rekord: end, id, avg_speed, direction

    def __init__(self):
	    #Konstruktor domyslny
        self.pointCoords = {}
        self.edges = [[[]]]
    def insert_point(self, point):
	    #Funkcja wstawiajaca nowy punkt do slownika
		#Klucz jest przyblizeniem do jednostek
        X = int(round(point[0]))
        Y = int(round(point[1]))
        self.pointCoords[str(X) + " " + str(Y)] = len(self.pointCoords)
        return self

    def search(self, point):
        #Funkcja szukajaca punktu w slowniku.
        #Sprawdza wszystkie skrajne punkty oczka metrowego
        #Jesli nie znajdzie, zwraca rozmiar slownika
        X = int(point[0])
        Y = int(point[1])
        keys = [str(X) + " " + str(Y),
                str(X) + " " + str(Y + 1),
                str(X + 1) + " " + str(Y),
                str(X + 1) + " " + str(Y + 1)]
        for key in keys:
            if self.pointCoords.has_key(key):
                return self.pointCoords[key]
        return len(self.pointCoords)

    def insert_edge(self, id, begin, end, length, avg_Speed, direction):
	    #Funkcja sluzaca do wstawiania nowych polaczen
        n = len(self.pointCoords)
		#Sprawdzenie, czy poczatek zostal juz wprowadzony
        begIdx = self.search(begin)
		#Jesli nie, to powinien byc wstawiony do tabeli punktow
        if (begIdx == n):
            self = self.insert_point(begin)
            n += 1
	    #Analogicznie dla konca
        endIdx = self.search(end)
        if (endIdx == n):
            self = self.insert_point(end)
            n += 1
	    #Wstawienie do tabeli polaczen
	if begIdx >=len(self.edges):
            self.edges.append([[endIdx,id,length, avg_Speed, direction//2]])
        else:
            self.edges[begIdx].append([endIdx,id,length, avg_Speed, direction//2])
        if endIdx >=len(self.edges):
            self.edges.append([[begIdx,id,length, avg_Speed, direction%2]])
        else:
            self.edges[endIdx].append([begIdx,id,length, avg_Speed, direction%2])
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
        self.pointCoords = {}
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

    def make_path(self, begin, end, mode = ["A*", "samochod", "najszybsza"]):
        # Interfejs do znajdowania sciezki za pomoca algorytmu BFS
        #    begin - punkt poczatkowy sciezki
        #    end - punkt koncowy sciezki
        #    mode - parametry wyznaczania, pozycja 0: algorytm, 1: pieszy, czy samochod, 2: czas, czy odleglosc
        come_from = []
        if mode[0] == "BFS":
            # Przeprowadzenie algorytmu BFS
            come_from = self.BFS(begin, end, mode)
        elif mode[0] == "A*":
            # Przeprowadzenie algorytmu A*
            come_from = self.aDot(begin, end, mode)
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

    def BFS (self, begin, end, mode):
        # Implementacja BFS
        # begin - punkt poczatkowy
        # end - punkt koncowy
        #Sprawdzenie stosunku do kierunkowosci
        ignore_direct = False
        if mode[1] == "pieszy":
            ignore_direct = True
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
            #Przeszukiwanie krawedzi wychodzacych z danego punktu
            if not visited[el[0]] and (ignore_direct or el[4] == 0):
                #Dodanie do kolejki i aktualizacja tablic
                q.put(el[0])
                visited[el[0]] = True
                come_from[el[0]] = [come_from[current][0] + 1, current, el[1]]
                #Jesli napotkany koniec to zwracamy come_from
                if el[0] == end:
                    return come_from
        return False

    def h(self, end, mode):
        #Docelowo funkcja obliczajaca heurystyke dla kazdego wierzcholka.
        #Teraz dla kazdego wierzcholka daje 0
        H = []
        endCoords=[]
        for el in self.pointCoords:
            H.append(0)
            if (self.pointCoords[el]==end):
                endCoords=el.split()
                endCoords=[int(endCoords[0]),int(endCoords[1])]
        for el2 in self.pointCoords:
            #{wspolrzedne:id}
            coords=el2.split()#wyciagamy wspolrzedne z klucza
            coords=[int(coords[0]),int(coords[1])]
            id=self.pointCoords[el2]# wyciagamy identyfikator z wartosci
            if mode[2]=="najkrotsza":
                H[id]=math.sqrt((coords[0]-endCoords[0])**2+(coords[1]-endCoords[1])**2)#odleglosc liniowa dla opcji "najkrotsza droga"
            else:
                H[id]=(math.sqrt((coords[0]-endCoords[0])**2+(coords[1]-endCoords[1])**2))/140
                """odleglosc liniowa dla opcji "najszybsza"- najbardziej optymistyczny wariant z maksymalna predkoscia na autostradzie"""
        return H

    def aDot(self, begin, end, mode):
        #Implementacja A*
        #visited - tablica odwiedzonych wierzcholkow
        #come_from - tablica trojek odleglosc, pochodzenie wierzcholka, pochodzenie krawedzi
        #Sprawdzenie stosunku do kierunkowosci
        ignore_direct = False
        if mode[1] == "pieszy":
            ignore_direct = True
        #Sprawdzenie, czy liczy sie czas, czy odleglosc
        time = 1
        if mode[2] == "najkrotsza":
            time = 0
        #Inicjalizacja
        visited = []
        come_from = [[]]
        for el in self.pointCoords:
            visited.append(False)
            if len(come_from[0]) == 0:
                come_from[0] = [999999999, None, None]
                continue
            come_from.append([999999999, None, None])
        #Pobranie heurystyki
        H = self.h(end, mode)
        #Inicjalizacja kolejki priorytetowej
        q = PriorityQueue()
        #Uwzglednienie pierwszego punktu
        q.put([H[begin], begin])
        come_from[begin] = [0, begin]
        #Dopoki kolejka nie opustoszala
        while not q.empty():
          #Pobierz pierwszy element
          current = q.get()[1]
          #Sprawdz, czy tu nie bylismy
          if visited[current]:
              continue
          #Odwiedzilismy wierzcholek
          visited[current] = True
          #Jak trafilismy na koniec, to zwracamy come_from
          if current == end:
              return come_from
          for el in self.edges[current]:
            #Przeszukiwanie krawedzi wychodzacych z danego punktu
            if len(el) == 0:
                continue
            dist = come_from[current][0] + el[2]/ (el[3]*time)
            #Jesli sasiad nie odwiedzony i nowa odleglosc bedzie mniejsza i nie przeczy kierunkowi
            if not visited[el[0]] and come_from[el[0]][0] > dist and (ignore_direct or el[4] == 0) :
                #Dodanie do kolejki i aktualizacja tablic
                q.put([dist + H[el[0]], el[0]])
                come_from[el[0]] = [dist, current, el[1]]
        return False
