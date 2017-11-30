# Szkibiel_Spila_PAG
Implementacja algorytmu A*

  Autorzy: Michał Szkibiel, Karol Śpila
  
  Bieżące zadania:
  
       1. Utworzenie struktury grafu z Feature Classy przedstawiającej drogi / Michał Szkibiel - wykonano
       
       2. Uzupełnienie parametrów i uzupełnienie ich w widoku grafu / Karol Śpila- zrobione
       
       3. Zamiana składowej pointCoords klasy Graph z uporządkowanej tablicy na tablicę asocjacyjną celem optymalizacji działania / Michał Szkibiel
       
       4. Implementacja algorytmu BFS z uwzględnieniem tego, że ma służyć do wyznaczania trasy pomiędzy dwoma punktami / Michał Szkibiel - zrobione
       
       5. Stworzenie funkcji tworzącej shapefile z podanej tablicy identyfikatorów dróg celem uzyskania shapefile'a z trasą / Karol Śpila
       
       6. Zamiana składowej edges na listę połączeń dla danego wierzchołka celem optymalizacji działania / Karol Śpila
       
  Pliki:
  
      BDOTtoGraph.py - plik konwertujacy Feature Classę z drogami na graf, a następnie zapisujący strukturę grafu do pliku tekstowego
      
      Skrzynka.zip - skompresowana skrzynka ArcGISa z narzędziami:
      
          "roads to graph" - uruchamia skrypt BDOTtoGraph.py. 
      
          "make path" - uruchamia skrypt FindPath.py
      
          Do poprawnego działania potrzebne jest ustalenie ścieżki do położenia pliku
      
      Jezdnie_WokolTorunia.zip- skompresowany Plik z Shapefile z gotowymi atrybutami o średniej prędkości w zależności od klasy dróg i materiału jej nawierzchni w przedostatniej kolumnie o nazwie sred_pred, oraz o kierunkowości zawartej w wartosciach 0-3, gdzie: 0- dwukierunkowość; 1- jednokierunkowość zgodna z orientacją; 2-jednokierunkowość przeciwna do orientacji; 3-ulice wyłączone z ruchu w ostatniej kolumnie "kierunk".
       
      wizualizacja.py- plik zawierający funkcję umożliwiającą wyświetlenie określonej trasy w ArcMapie. Funkcja została dodana także do skryptu FindPath.py
      
      Graph.py - moduł zawierający implemenrtację klasy Graph, z której będą korzystały wszystkie moduły wykonywalne zawarte w projekcie. Żeby możliwe było uruchomienie modułów wykonywalnych z poziomu narzędzia skryptowego w ArcGISie. Ten plik powinien się znaleźć w folderze C:\Python27\ArcGIS10.5\Lib (Ewentualnie, jak python nie jest zainstalowany bezpośrednio na dysku C, to ...\Python27\ArcGIS10.5\Lib)
      
      FindPath.py - Skrypt, który przyjmuje sieć drogową w formie .shp i dwa punkty w formie .shp, po czym tworzy trasę pomiędzy tymi dwoma punktami wytyczoną za pomocą algorytmu BFS. Docelowo wynikiem ma być shapefile reprezentujący trasę.
