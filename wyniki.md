# Raport ze scenariuszy i analiza algorytmów

## Scenariusze

### Tabelka porównań scenariuszy

| Scenariusz            | Samoloty   | Dziennikarz | Porównywanie Parami |
|-----------------------|------------|-------------|---------------------|
| Algorytm              | King       | PBFT        | Lamport             |
| 'N' wierzchołków      | 9 (4;5)    | 5           | 7                   |
| W tym 't' wadliwych   | 2          | 1           | 2                   |
| Procent tolerancji    | 22%        | 20%         | 28.5%               |
| Rodzaj grafu          | Dwudzielny | Pełny       | Pełny               |
| Parametr algorytmu    | 3 rundy (k)| 3 rundy (k) | głębokość 2 (d)     |
| czas trwania          | 14s        | 48s         | 116s                |
| liczba kroków         | 3          | 15          | 37                  |
| 'l' wysłanych opinii  | 60         | 42          | 156                 |
| Potrzebnych wierzchołków | 4t+1     | 4t + klient | 3t+1               |
| Złożoność algorytmu   | O(t^3)     | O(t^3*5k)   | O(t^4)              |
| Gwarancja konsensusu? | Tak        | Tak         | Tak                 |
 

 ### Samoloty

  Scenariusz zrealizowany za pomocą przebiegu algorytmu króla na grafie dwudzielnym

  Ustawienia początkowe grafu:
  - Graf dwudzielny z 9 wierzchołkami, rozłączne zbiory liczące 4 i 5 węzłów 
  - 3 wierzchołki ustawione na opinię błędną
  - 2 wierzchołki będące wadliwe, co stanowi 22% całości systemu

  Ustawienia i działanie algorytmu króla:
  - parametry - 3 rundy trwania algorytmu 
  - każdy wierzchołek wysyła swoim sąsiadom opinię i podejmuje decyzję w oparciu o otrzymane od innych

  Analiza przebiegu:
  - czas animacji - 14 sekund
  - liczba kroków animacji - 3
  - liczba wysłanych opinii - 60, w każdym z kroków zostaje wysłane 20 opinii opinii  

  Ocena i wnioski
  - najszybciej trwający algorytm, wynikający z małej ilości kroków, jeden na rundę
  - niższy poziom oferowanej niezawodności systemu, wymagający 4t + 1 wierzchołków w grafie pełnym, gdzie t to liczba 'zdrajców'
  - przy 9 wierzchołkach daje to wartość 22%, w zależności od ich liczby niezawodność wynosi od 20% do 25%
  - liczba rund potrzebna do osiągnięciu konsensusu w grafie pełnym równa liczbie zdrajców, w grafie dwudzielnym potrzebna runda dodatkowa - tutaj trzecia - by informacja mogła wrócić
  - Konsensus scenariusza jest zapewniony

 ### Dziennikarz

 Scenariusz zrealizowany za pomocą przebiegu algorytmu PBFT na grafie pełnym, z wyróżnionym węzłem klienta

  Ustawienia początkowe grafu:
  - Graf pełny z 6 wierzchołkami, 5 stanowiący system serwisów i środkowego klienta
  - 2 wierzchołki serwisów ustawione na opinię błędną
  - 1 wierzchołek będący wadliwy, co stanowi 20% całości systemu

  Ustawienia i działanie algorytmu króla:
  - parametry - 3 rundy trwania algorytmu
  - Każda runda złożona z pięciu faz, request, pre-prepare, prepare, commit, reply, w trakcie której klient wysyła zapytanie i otrzymuje odpowiedź od systemu

  Analiza przebiegu:
  - czas animacji - 48 sekund
  - liczba kroków animacji - 15, po pięć faz na rundę
  - liczba wysłanych opinii - 42

  Ocena i wnioski
  - Algorytm symuluje system zapytania od klienta do rozproszonego systemu serwisów
  - Pod względem złożoności oraz niezawodności, przypomina algorytm króla
  - Konsensus scenariusza jest zapewniony


 ### Porównanie parami

 Scenariusz zrealizowany za pomocą przebiegu algorytmu lamporta na grafie pełnym

  Ustawienia początkowe grafu:
  - Graf pełny z 7 wierzchołkami
  - 3 wierzchołki ustawione na opinię błędną
  - 2 wierzchołki będące wadliwe, co stanowi 28.5% całości systemu

  Ustawienia i działanie algorytmu króla:
  - parametry - głębokość rekurencji algorytmu - 2 
  - lider rekurencyjnie wysyła opinię do swoich podległych sąsiadów

  Analiza przebiegu:
  - czas animacji - 116s sekund
  - liczba kroków animacji - 37, 1 st. zerowego rekurencji, 6 st. pierwszego, 30 st. drugiego 
  - liczba wysłanych opinii - 156  

  Ocena i wnioski
  - najdłuższy czas trwania wynikający z jednej operacji na krok animacji
  - również największa ilość wysłanych opinii, wynikająca z wyższego stopnia złożoności
  - algorytm oferuje w zamian za to najwyższą odporność systemu, przy liczbie wierzchołków 3t + 1 wynoszącą do 28.5% 
  - Konsensus scenariusza jest zapewniony

 ## Algorytmy

 Poniżej przedstawione zostały obliczenia wymaganej liczby kroków i wysłanych opinii żeby zrealizować algorytm konsensusu. Rozpatrzone zostały przypadki dwóch grafów pełnych
 - a) dziesięć wierzchołków, z progiem niezawodności systemu 20% (2 z 10 mogą być wadliwe)
 - b) pięćdziesiąt wierzchołków, z progiem niezawodności systemu 25% (12 z 50 mogą być wadliwe)

Z założeniami, że każdy algorytm wykona minimalną ilość kroków pottrzebnych dla walidacji opinii przy odpowiedniej, z góry założonej wartości t maksymalnych węzłów wadliwych.
Przy obliczaniu rekurencji algorytmu lamporta wykorzystamy wyrażenie reprezentujące iloczyn
\( (n-1)_{k} = (n-1)(n-2) \ldots (n-k) \)
Liczba kroków równa liczbie rund (k); \( K(n, d) = \sum_{k=0}^{d} (n-1)_k \)
  Liczba wysłanych opinii (op); \( Op(n, d) = \sum_{k=1}^{d+1} (n-1)_{k-1} \)
  Liczba podjętych decyzji (dec); \( Dc(n, d) = 2(N-1) + \sum_{k=1}^{d} (N-1)_k \)

 ### Mniejszy graf, K10, t = 2

 - Algorytm króla - dwie rundy podczas których każdy wierzchołek wysyła opinię do wszystkich innych.
  Liczba kroków równa liczbie rund (k) = 2
  Liczba wysłanych opinii (op) = k \* n \* (n-1) = 2\* 10 \* 9 = 180 
  Liczba podjętych decyzji (dec) = k \* n = 2 * 10 = 20 

 - Algorytm lamporta - rekurencyjne wysyłanie opinii do pozostałych wierzchołków aż do osiągnięcia głębokości.
  Głębokość (d) = 2
  Liczba kroków (k);  1 + 9 + 72 = 82
  Liczba wysłanych opinii (op); 9 + 72 + 434 = 585
  Liczba podjętych decyzji (dec); 72 + 2*9 = 90

 - Algorytm PBFT - dwie rundy złożone z pięciu faz
  Liczba kroków(k); k*5 = 10
  Liczba wysłanych opinii (op); k(2*(n-1)) + 1 = 37 
  Liczba podjętych decyzji (dec); k(1+(n-2)+(n-2)*(n-3)+(n-1)*(n-2)+(n-1)) = 292

 ### Większy graf, K50, t = 12
  - Algorytm króla - dwanaście rund podczas których każdy wierzchołek wysyła opinię do wszystkich innych.
  Liczba kroków równa liczbie rund (k) = 12
  Liczba wysłanych opinii = k \* n \* (n-1) = 12\* 50 \* 49 = 29400
  Liczba podjętych decyzji (dec) = k \* n = 12 * 50 = 6000 
  - Algorytm lamporta - rekurencyjne wysyłanie opinii do pozostałych wierzchołków aż do osiągnięcia głębokości.
  Głębokość (d) = 2
  Liczba kroków (k);  1 + 9 + 72 = 2402
  Liczba wysłanych opinii (op); 9 + 72 + 434 = 112945
  Liczba podjętych decyzji (dec); 72 + 2*9 = 2450
  - Algorytm PBFT - dwanaście rund złożonych z pięciu faz
  Liczba kroków(k); k*5 = 60
  Liczba wysłanych opinii (op); k(2*(n-1)) + 1 = 26472
  Liczba podjętych decyzji (dec); k(1+(n-2)+(n-2)*(n-3)+(n-1)*(n-2)+(n-1)) = 1177


  | Algorytm         | Parametry                 | Liczba kroków (k) | Liczba wysłanych opinii (op) | Liczba podjętych decyzji (dec) |
|------------------|---------------------------|-------------------|-------------------------------|--------------------------------|
|10 wierzchołków | max 2 nieprawidłowych|
| Algorytm króla   | k = 2                      | 2                 | 180                           | 20                             |
| Algorytm lamporta| d = 2                      | 82                | 585                           | 90                             |
| Algorytm PBFT    | k = 2                      | 10                | 37                            | 292                            |
|50 wierzchołków | max 12 nieprawidłowych|
| Algorytm króla   | k = 12                     | 12                | 29,400                        | 6,000                          |
| Algorytm lamporta| d = 2                      | 2,402             | 112,945                       | 2,450                          |
| Algorytm PBFT    | k = 12                     | 60                | 26,472                        | 1,177                          |

Jak widać, przy wzroście rozmiaru sytemu rozproszonego, algorytm lamporta, oferujący wyższą niezawodność systemu zdecydowanie zwiększza liczbę potrzebnych obliczeń w stosunku do reszty. 

Dla dowolnego innego systemu można obliczyć liczbę poszczególnych operacji tych trzech algorytmów za pomocą skryptu zawartego w pliku 'calculate_graphs.py' w głównym folderze źródłowym.

Pominięty w rozważaniach model Q-Voter nie oferuje żadnego konsensusu, dlatego nie został uwzględniony w tabelce. Dla algorytmu z czasem 't' oraz parametrem sąsidów 'q' liczba operacji jest następująca:
- 't' kroków
- 't' podjętych decyzji
- 't' \* 'q' wysłanych opinii



