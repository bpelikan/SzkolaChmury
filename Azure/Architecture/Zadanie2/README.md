# Praca domowa - tydzień 2

##

#### Valet Key
* SAS dla faktur

#### CQRS
* rozdzielenie zapisu oraz odczytu danych

#### Throttling pattern
* ograniczenie użytkownikowi ilości zapytań na sekundę - dostarczenie usługi do większej ilości klinetów


#### Asynchronous Messaging/Queue-Based Load Leveling

#### Competing Consumer Pattern
* wysyłanie wiadomości
* dokonywanie płatności ?


#### Cached Data Consistency

#### Cache Aside Pattern
* pobieranie informacji o produktach


#### Load Balancing
* rozkładanie ruchu pomiędzy instancjami aplikacji



## Usługi


#### Storage
* przechowywanie zdjęć (public/container)
* przechowywanie faktur 
  * dostęp przez Sas - Valet Key Pattern
  * przepisy prawa, czy należy przechowywać przez X lt faktury -> immutable storage
  * logowanie/monitorowanie wykorzystania (konieczność użycia innych metod niż SAS?)
  * wykorzystanie API z AAD z celu lepszego monitorowania (audytu) dostępu do faktur + az storage w sieci prywatnej (jeśli jest to mozliwe?)


#### CDN/cache
* dla zdjęć oraz treści opisu produktów

#### CosmosDb
* replikacja danych o produktach na różnych regionach (wykorzystanie systemu monitoringu do wyznaczenia ... regionów)
* ? ograniczanie ilości zapytań w jednostce czasu na klienta (jak w APi management)?

#### Functions
* przetwarzanie płatnści ([case study ze sprzedaży kursu DDD](https://blog.scooletz.com/2019/09/02/how-i-built-and-run-my-e-shop-for-0-07-month-using-azure-functions-and-a-few-more/))


#### Cognitive Services
* zdjęcie/tekst - analiza pod kątem treści zabronionych
* tworzenie thumbnaili zdjęć


#### Search
* wyszukiwanie produktów

#### API management
* ograniczenie ilości zapytań użytkownika w jednostce czasu
* uwierzytelnianie urzytkowników/token


#### Trafic manager
* przekierowanie na podstawie lokalizacji geograficznej czy też najkrótszej trasy

#### Load balancer / Application gateway
* za trafic managerem, rozrzucanie ruchu pomiędzy instancjami w zależności od usługi jaką świadczą (oraz obciążenia jeśli wspiera - trafiic manager/load balancer)


#### Wysyłanie maili
* SendGrid, inne ...