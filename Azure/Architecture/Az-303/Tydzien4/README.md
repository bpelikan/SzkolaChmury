# [Zadanie domowe z tygodnia 4](https://szkolachmury.pl/az-303-microsoft-azure-architect-technologies/tydzien-4-implement-cloud-infrastructure-monitoring/praca-domowa/)

* #TYDZIEŃ4.1 „Dla każdego typu Storage, którego się nauczyłeś w czasie kursu (min. 4 typy) dobierz dwa dobre i jedno złe zastosowanie. Chciałbym byś zweryfikował różne możliwości składowania danych w Azure i opowiedział, kiedy i do czego te możliwości możesz wykorzystać”.
* #TYDZIEŃ4.2 „Wymień jeden dobry i jeden zły przykład wykorzystania StorSimple w swojej organizacji. Napisz, kiedy i w jakich scenariuszach się sprawdzi, a kiedy nie.”
* TYDZIEŃ4.3 „Liczymy Koszty :). Umówmy się. Twój system backupu (nie ma znaczenia jaki) składuje 1TB nowych danych każdego dnia. Wykorzystujesz oczywiście Azure do tej operacji i chcesz dane składować jak najtaniej. Przez dwa lata nie kasujesz zebranych danych. Po dwóch latach na próbę odtwarzasz dane z ostatniego dnia każdego roku. Po 3 roku kasujesz dane, zebrane w roku pierwszym.

    Ile łącznie wygenerujesz kosztów w ramach tej usługi, jeśli rozważymy pełny, 6 letni okres jej działania.
Rozważ różne aspekty i różne możliwości usług i pokaż jako algorytm liczenia przyjąłeś.

## 1. Zadanie 4.1

> Dla każdego typu Storage, którego się nauczyłeś w czasie kursu (min. 4 typy) dobierz dwa dobre i jedno złe zastosowanie. Chciałbym byś zweryfikował różne możliwości składowania danych w Azure i opowiedział, kiedy i do czego te możliwości możesz wykorzystać

* Azure Storage
    * Blobs
        * Plusy: 
            * Przechowywanie plików archiwalnych/backupów np. faktury z dostępem dla klientów poprzez SAS, dokumenty firmowe, regulaminy
            * Przechowywanie logów aplikacyjnych (aktualizowanych w przedziałach czasowych, nie w czasie rzeczywistym)
        * Minusy: 
            * Trzymanie plików z dużą ilością zapisu/odczytu np. pliki konfiguracyjne z których bezpośrednio korzystają aplikacje,
            * Backup prywatnych plików (nieoptymalne kosztowo)
    * Files
        * Plusy:
            * Współdzielenie plików pomiędzy VM
            * Zastąpienie lokalnego urządzenia NAS
        * Minusy:
            * Przechowywanie plików statycznych jak np. grafiki na stronę www
    * Queues
        * Plusy:
            * Komunikacja asynchroniczna dla serwisów niewymagających określonej kolejności wiadomości, np. wysyłka wiadomości email, żądanie wygenerowania dokumentu
        * Minusy:
            * Brak `publish-subscribe messaging pattern` z wieloma subskrybentami
    * Tables
        * Plusy:
            * Tania baza NoSQL - przechowywanie nierelacyjnych danych
            * Storage dla logów
        * Minusy:
            * Chęć wykorzystanie relacyjności
    * Disks
        * Plusy:
            * Wysoka przepustowość IOPS
            * Duży transfer danych (przetwarzanie,obróbka plików)
        * Minusy:
            * Chęć współdzielenia danych
* Azure Files & FileSync
* StorSimple
* Azure Site Recovery, Azure Backup, Azure Data Box