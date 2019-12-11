# Praca domowa - tydzień 2

## Patterns

#### Valet Key
* odciążenie serwera aplikacyjnego niepotrzebnymi operacjami pobierania/wysyłania plików
* zmniejszenie wykorzystania transferu danych
* skalowanie tylko usługi dostarczającej pliki w przypadku większego zapotrzebowania
* dostęp do plików w określonym zakresie uprawnień (odczyt/zapis) oraz w określonym czasie
* możliwość unieważnienia klucza przez serwer (np. po zakończonym procesie wysyłania pliku)

* klucz dostępu może zostać upubliczniony

* SAS dla faktur
* trudność w logowaniu/autytowaniu dostępu

<details>
    <summary><b><i>Wady/zalety</i></b></summary>

| Zalety                                                                                    | Wady                                                                                        |
|-------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| odciążenie serwera aplikacyjnego niepotrzebnymi operacjami pobierania/wysyłania plików    | klucz dostępu może zostać upubliczniony                                                     |
| zmniejszenie wykorzystania transferu danych                                               | zbyt krótki okres ważności klucza może spowodować, że użytkownik nie zdąży wykonać operacji |
| skalowanie tylko usługi dostarczającej pliki w przypadku większego zapotrzebowania        | brak możliwości zdefiniowania rozmiaru wysyłanego plików / ilości pobrań pliku              |
| dostęp do plików w określonym zakresie uprawnień (odczyt/zapis) oraz w określonym czasie  | konieczność zarządzania kluczami dostępu                                                    |
| możliwość unieważnienia klucza przez serwer (np. po zakończonym procesie wysyłania pliku) | przeglądarka może nie wspierać CORS                                                         |
|                                                                                           |                                                                                             |
|                                                                                           |                                                                                             |
</details>


#### CQRS
* rozdzielenie zapisu oraz odczytu danych
* oddzielne skalowanie odczytu oraz zapisu / niezależne skalowanie
* wykorzystanie kolejki dla asynchronicznego zapisu
* zoptymalizowana baza do odczytu
* możliwość wykorzystania różnego typu baz relacyjna/nierelacyjna
* wykorzystanie repliki bazy do odczytu jako read-only

#### Throttling pattern
* ograniczenie użytkownikowi ilości zapytań na sekundę - dostarczenie usługi do większej ilości klinetów (np w szczególnym okresie większej aktywności - kampania reklamowa/black friday) ()
* spełnienie wymagań SLA
* wyłączanie usług mało istotnych na rzecz usług wrażliwych (przynoszących wartość biznesową), jak np. dokonywanie zakupów, płatności (pomocne może być Priority Queue pattern  z ustawionymi hight-value tenant)
* ograniczenie dostępu na czas autoskalowania



#### Asynchronous Messaging/Queue-Based Load Leveling

#### Competing Consumer Pattern - Azure Service Bus Queues
* wysyłanie wiadomości
* dokonywanie płatności ?
* generowanie faktur


#### Cached Data Consistency

#### Cache Aside Pattern
* przechowywanie informacji o produktach jak cena czy opis


#### Load Balancing
* rozkładanie ruchu pomiędzy instancjami aplikacji


#### Redis Cache
* cache dla danych pobieranych przez użytkowników/klientów

#### Data Partitioning (Lookup Strategy / Range Strategy / Hash Strategy)
* według kategorii produktów , klienta? przy płatnościach-historii zakupów, daty miesiąca/godziny

#### Materialized View Pattern


#### Transient Error / Transient Fault Handling
* ponawianie zapytań do serwisu - chwilowa niedostępność kolejki, konta storage

#### Circuit Breaker
* blokowanie kolejnych połączeń w przypadku niedostępności usługi

#### Retry Pattern

#### Queue Based Load Leveling
* nierównomierny ruch, monitorowanie wielkości kolejki -> skalowanie
* przechowywanie wiadomości w przypadku niedostępności serwisu konsumującego wiadomości
* wysyłanie maili (np z potwierdzeniem zakupu)


## Usługi


#### Storage
* przechowywanie zdjęć (public/container)
* przechowywanie faktur 
  * dostęp przez Sas - Valet Key Pattern
  * przepisy prawa, czy należy przechowywać przez X lt faktury -> immutable storage
  * logowanie/monitorowanie wykorzystania (konieczność użycia innych metod niż SAS?)
  * wykorzystanie API z AAD z celu lepszego monitorowania (audytu) dostępu do faktur + az storage w sieci prywatnej (jeśli jest to mozliwe?)


#### CDN/cache / Azure Cache for Redis
* dla zdjęć oraz treści opisu produktów

#### CosmosDb
* replikacja danych o produktach na różnych regionach (wykorzystanie systemu monitoringu do wyznaczenia ... regionów)
* ? ograniczanie ilości zapytań w jednostce czasu na klienta (jak w APi management)?

#### Functions
* przetwarzanie płatnści ([case study ze sprzedaży kursu DDD](https://blog.scooletz.com/2019/09/02/how-i-built-and-run-my-e-shop-for-0-07-month-using-azure-functions-and-a-few-more/))


#### Cognitive Services
* zdjęcie/tekst - analiza pod kątem treści zabronionych
* tworzenie thumbnaili zdjęć

#### Service Bus Queues
* system kolejkowy

#### Search
* wyszukiwanie produktów

#### API management
* ograniczenie ilości zapytań użytkownika w jednostce czasu
* uwierzytelnianie urzytkowników/token


#### Trafic manager
* przekierowanie na podstawie lokalizacji geograficznej czy też najkrótszej trasy

#### Load balancer / Application gateway
* za trafic managerem, rozrzucanie ruchu pomiędzy instancjami w zależności od usługi jaką świadczą (oraz obciążenia jeśli wspiera - trafiic manager/load balancer)

#### Data ...
* tworzenie raportów, analiza danych

#### Wysyłanie maili
* SendGrid, inne ...


----

Użycie zebranych logów do wyboru regionów w których będzie istniała aplikacja, rodzaju cachowanych danych według regionu oraz popularności danej kategorii