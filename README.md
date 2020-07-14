# LogService
## Spis treści
- [Wprowadzenie](#wprowadzenie)
  + [Narzędznia i technologie](#narzędzia-i-technologie)
  + [Architektura](#architektura)
- [Przygotowanie środowiska](#przygotowanie-srodowiska)
  + [Instalacja](#instalacja)
  + [Konfiguracja](#konfiguracja)
  + [Uruchomienie](#uruchomienie)
- [Zasada działania](#zasada-działania)
- [Testy](#testy)
- [Podsumowanie & wnioski](#Podsumowanie-wnioski)



# Wprowadzenie
Realizowany projekt składa się z dwóch części. Pierwsza polega na zbudowaniu mechanizmu pozyskiwania i agregacji logów. Zakładamy, że logi dostępne są w formie tekstowej na różnych serwerach (w tym lokalnym). Dostęp do tych logów jest możliwy poprzez ftp, http oraz ssh. Opracowany zostanie mechanizm pobierania logów z każdego serwera, który pozwala na określenie metody dostępu do niego, częstotliwości sprawdzeń oraz autoryzacji. Druga część projektu polega na przygotowaniu mechanizmu raportującego podejrzane zdarzenia (według skonfigurowanych reguł). Mechanizm konfiguracji powinien być elastyczny: tj. pozwalać np. na określenie wzorców pozytywnych i negatywnych, warunków typu if-else oraz ograniczeń czasowych.
## Narzędzia i technologie

Do wykonania projektu zostały wykorzystane następujące technologie:
+ Python
+ SSH
+ FTP
+ HTTP
+ PySpark
+ Paramiko
+ PyYAML

## Architektura

Poniższy diagram przedstawia architekturę aplikacji:
//tutaj nasz obrazek

![01](https://i.imgur.com/mfXwGup.jpg)

Projekt składa się z głównego komponentu, który zarządza pozostałymi komponentami. 
Program zawiera cztery moduły służące do pozyskiwania danych z źródeł HTTP, SSH, FTP oraz serwera lokalnego.
Dodatkowo program posiada parsery umożliwiające analize logów aplikacji takich jak DPKG, PostgreSQL oraz Apache. 
Umożliwiają również zdefiniowanie własnego parsera.

## Przygotowanie środowiska

Oprogramowanie przeznaczone jest na system operacyjny Linux

### Instalacja wymaganych bibliotek
Do prawidłowego funkcjonowania oprogramowania należy zainstalować następujące biblioteki:

```console
apt-get install python3.6
pip install pyspark
pip3 install PyYAML
pip3 install paramiko
```
Należy się upewnić, czy wszystkie biblioteki są zainstalowane poprawnie, w przeciwnym wypadku program się nie uruchomi bądź będzie działał niepoprawnie.


### Konfiguracja
Przed uruchomieniem należy skonfigurować połączenia w pliku `settings.yaml`, który znajduje się w głównym katalogu projektu. 

Przykładowa konfiguracja połączenia SSH dla logów DPKG:
```console
  - host: ssh                       #rodzaj połączenia
    path: localhost                 #adres połączenia
    login: logger                   #login użytkownika
    password: logger_password       #hasło użytkownika
    file: dpkg.log                  #nazwa pliku zawierająca logi
    port: 2222                      #port połączenia ssh
    type: dpkg                      #typ logów
```
Pozostałe przykładowe połączenia znajdują się w pliku `settings.yaml`

Należy także ustawić ścieżkę do Javy potrzebną do PySparka w pliku `HttpParser.py`

### Uruchomienie
Aby uruchomić program należy wykonać poniższe polecenie w głównym folderze aplikacji:
```console
admin@admin:/LogService$ python3 main.py
admin@admin:/LogService$ python3 main.py -v #dla wyświetlania logów aplikacji
admin@admin:/LogService$ python3 main.py -days 10 #analiza logów z ostatnich 10 dni
```
Przykładowy (pusty) wynik działania programu dla logów HTTP, PostgreSQL oraz DPKG:


```console
admin@admin:/LogService$ python3 main.py
Logger v1.0.0
Analyzing log file from HTTP host - http://estelladandyk.kylos.pl/logger/file.txt
------------------HTTP---------------------
Total file lines:

-----------------------
Total distinct HTTP Status Codes:

-----------------------
Status Codes table:
-----------------------
Top 10 404 Response Code Endpoints:

-----------------------
Top 10 404 Response Code Hosts:

--------------END of HTTP-------------------
Analyzing log file from local storage
------------------PostgreSQL----------------------
Errors:
-----------------------
Statement:
-----------------------
Hint:
-----------------------
Log:
-----------------------
Warning:
-----------------------
Users:
--------------END of PostgreSQL-------------------
Analyzing file from SSH host - localhost
------------------DPKG----------------------------
Installed:
-----------------------
Removed:
-----------------------
Upgraded:
-----------------------
Purged:
--------------END of DPKG-------------------------
```



## Zasada działania

Algorytm działania aplikacji do analizy logów i raportowania zdarzeń wygląda następująco:

1. Wczytanie konfiguracji zdefiniowanych połączeń
1. Dla każdego rodzaju połączenia
      1. Połączenie z usługą
      1. Pobranie zdefinowanego pliku logów
      1. Zamknięcie połączenia z usługą
      1. Parsowanie wcześniej pobranego pliku
      1. Analiza logów
      1. Wyświetlanie rezultatów analizy


## Testy

W aplikacji zostały przetestowane następujące elementy:
+ Połączenie SSH
+ Połączenie FTP
+ Połączenie HTTP (WWW)
+ Połączenie lokalne
+ Analiza logów DPKG
+ Analiza logów PostgreSQL
+ Analiza logów DPKG z ostatnich 30 dni
+ Analiza logów PostgreSQL z ostatnich 30 dni
+ Analiza logów HTTP
+ Analiza logów HTTP z ostatnich 30 dni

Wszystkie testy zostały wykonane poprawnie.

```console
admin@admin:/LogService$ python3 LogServiceTestCases.py
..........
----------------------------------------------------------------------
Ran 10 tests in 23.156s

OK
```

## Podsumowanie & wnioski

Podczas tworzenia projektu udało się stworzyć funkcjonalne narzędzie ułatwiające ludziom, w szczególności administratorom systemowym, do wygodnego i szybkiego pobierania danych z różnych skonfigurowanych źródeł oraz ich umożliwienie sprawnego przetwarzania logów w celu wykrycia potencjalnych problemów w działających aplikacjach.
Dodatkowo umożliwiając ustawianie własnych warunków wykrywania zagrożeń. Podczas realizacji projektu przeanalizowaliśmy różne źródła dostępne w sieci internet, które przedstawiły fakt, że istnieje niezliczona liczba typów logów, w tym "customowe" każdego człowieka. Ukazując problem analizy logów pochodzących z różnego typu aplikacji. 
Stworzone narzędzie rozwiązuje ten problem dostarczając kilka predefiniowanych parserów logów, dzięki czemu użytkownik jest w stanie analizować logi według własnych reguł pochodzących z różnych aplikacji.  
Narzędzie dostarcza rozmaite wyniki analizy logów co może okazać się krytyczne w przypadku ukrytych problemów z aplikacją

Aplikacja została zbudowana w sposób umożliwiający jego dalszą rozbudowę. Narzędzie można rozbudować poprzez dodanie nowych parserów, nowych źródeł logów oraz dodanie interfejsu graficznego poprawiając wrażenia wizualne z użytkowania.

## Twórcy
Projekt realizowany przez : jbogunia, psmuga, RSkr
