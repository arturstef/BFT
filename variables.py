from tkinter import *
from tkinter import ttk

scale = 2.0 #nie wiem, czy jest gdziekolwiek używana...
width = 1050
height = 900

icon_true = "img/sword.png"
icon_false = "img/shield.png"

V = [] #[[]]
E = [] #[{}]
lines = [] #[{}] #to są linie i one są jak E, gdzie to drugie to współrzędne
G = [] #[None]

drag_index = 0
startX = 0
startY = 0

algorithm_data = []

number_of_tab = 1
canvases = []
loggers = []

descriptions = {
"king": '''ALGORYTM KRÓLA:
Algorytm odporny na problemy bizantyńskie, przy liczbie co najmniej 4t+1 generałów przy
t fałszywych. Można go podzielić na dwie fazy:

1. Wysyłanie opinii
    -Generałowie wymieniają się opiniami.
    -Każdy generał ustawia swoją opinię na podstawie wszystkich zebranych i zapamiętuje zebrane dane.

2. Wybór króla
    -Nowy król jest wybierany dowolną metodą znaną wszystkim generałom. W naszej implementacji jest to po prostu kolejny węzeł po obecnym królu.
    -Nowy król wysyła swoją opinię. Jeżeli opinia w poprzednim kroku została ustalona różnicą mniejszą niż 3 (u każdego generała), to generał poporządkowuje się opinii króla.
''',

"lamport": '''ALGORYTM LAMPORTA:
Algorytm odporny na problemy bizantyńskie, przy liczbie co najmniej 3t+1 generałów przy
t fałszywych. Można go podzielić na dwie fazy:

    1. Wysyłanie opinii - generałowie wysyłają opinie do swoich poddanych, a oni je zliczają
    2. Wybieranie opinii - poddani wybierają swoją opinię na podstawie zliczonych opinii (wygrywa ta, która została przypisana więcej razy)
''',

"q_voter": '''Q-VOTER:
Algorytm Q-Voter to model analizujący interakcje między agentami w systemach złożonych.
W kontekście problemów bizantyńskich, gdzie pewne jednostki mogą działać nieuczciwie,
model Q-Voter może być używany do zrozumienia, jak decyzje podejmowane są w obecności
błędów lub oszustw.

Działanie algorytmu można podzielić na:

    1. Inicjalizację:
        -Każdy agent ma swoją własną początkową decyzję.

    2. Interakcje między agentami:
        -Agenci oddziałują ze sobą, wymieniając informacje o swoich decyzjach.
        -Każdy agent decyduje na podstawie informacji od "q" sąsiadów.

    3. Aktualizacje decyzji:
        -Jeśli przynajmniej "q" sąsiadów danego agenta ma tę samą decyzję, to agent utrzymuje lub przyjmuje tę decyzję.
        -W przypadku braku jednomyślności, agent może pozostać przy swojej obecnej decyzji lub podejmuje nową decyzję na podstawie pewnego kryterium (np. losowego wyboru).
''',

"pbft": '''PBFT:
Algorytm konsensusu o 5 fazach:
    1. Faza prośby (Request Phase):
        -Klient wysyła prośbę do jednego z węzłów, zwanej węzłem lidera.
        -Węzeł lider przekazuje prośbę do innych węzłów.
    2. Faza pre-preparacji (Pre-Prepare Phase):
        -Lider proponuje konkretną wartość i numer sekwencyjny dla prośby klienta.
        -Pozostałe węzły otrzymują pre-preparację i weryfikują jej poprawność.
        -Po weryfikacji węzły przesyłają pre-preparację do innych węzłów.
    3. Faza przygotowania (Prepare Phase):
        -Węzły otrzymują pre-preparację, weryfikują jej poprawność i wysyłają potwierdzenie (prepare) do innych węzłów.
        -Każde węzeł oczekuje na odpowiednią liczbę potwierdzeń od innych węzłów przed przejściem do następnego etapu.
    4. Faza zatwierdzania (Commit Phase):
        -Węzły otrzymują wystarczającą liczbę potwierdzeń i przesyłają zatwierdzenie (commit) do innych węzłów.
        -Po otrzymaniu wystarczającej liczby zatwierdzeń, węzły wykonują operację i informują o tym klienta.
    5. Faza wykonania (Execution Phase):
        -Operacja jest wykonana na każdym węźle.
'''}