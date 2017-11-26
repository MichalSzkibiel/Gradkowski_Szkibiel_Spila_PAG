# Gradkowski_Szkibiel_Spila_PAG
Implementacja algorytmu A*

  Autorzy: Adam Gradkowski, Michał Szkibiel, Karol Śpila
  
  Bieżące zadania:
  
       1. Utworzenie struktury grafu z Feature Classy przedstawiającej drogi / Michał Szkibiel - wykonano
       
       2. Uzupełnienie parametrów i uzupełnienie ich w widoku grafu / Karol Śpila- zrobione
       
       3. Zamiana składowej pointCoords klasy Graph z uporządkowanej tablicy na tablicę asocjacyjną celem optymalizacji działania / Adam Gradkowski
       
  Pliki:
  
      BDOTtoGraph.py - plik konwertujacy Feature Classę z drogami na graf, a następnie zapisujący strukturę grafu do pliku tekstowego
      
      Skrzynka.zip - skompresowana skrzynka ArcGISa z narzędziem "roads to graph" uruchamiającym skrypt BDOTtoGraph.py. Do poprawnego                           działania potrzebne jest ustalenie ścieżki do położenia pliku
      
      Jezdnie_WokolTorunia.zip- skompresowany Plik z Shapefile z gotowymi atrybutami o średniej prędkości w zależności od klasy dróg i materiału jej nawierzchni w przedostatniej kolumnie o nazwie sred_pred, oraz o kierunkowości zawartej w wartosciach 0-3, gdzie: 0- dwukierunkowość; 1- jednokierunkowość zgodna z orientacją; 2-jednokierunkowość przeciwna do orientacji; 3-ulice wyłączone z ruchu w ostatniej kolumnie "kierunk".
       
      wizualizacja.py- plik zawierający funkcję umożliwiającą wyświetlenie określonej trasy w ArcMapie. Zapytanie SQL będzie jeszcze poprawione.
