# [Zadanie domowe nr 7](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-7-databases-on-google-cloud/zadanie-domowe-nr-7/)

## 1. Firma posiada jedną głowną bazę danych MySQL - jeden serwer dla danych użytkowników, inwentaryzacji, danych statycznych. Serwis ten jest głównym elementem, który ma zostać przeniesiony do środowiska w Google Cloud.
> 
    MySQL. One server for user data, inventory, static data,
        MySQL 5.7
        8 core CPUs
        128 GB of RAM
        2x 5 TB HDD (RAID 1)

Patrząc na powyższe wymagania potrzebować będziemy bazy MySQL o pojemności 5TB z włączoną opcją HA (jako, że storage bazy on-prem jest w RAID 1). 
Wymagania te spełni baza `Cloud SQL`, problemem tutaj może być wybór odpowiedniego typu maszyny:
* db-n1-standard-32 (32vCPU, 120 GB)
* db-n1-standard-64 (64vCPU, 240 GB)
* db-n1-highmem-16 (16vCPU, 104 GB)
* db-n1-highmem-32 (32vCPU, 208 GB)

Dodatkowo można wykorzystać tutaj opcję replikacji bazy [`Replication from an external server`](https://cloud.google.com/sql/docs/mysql/replication/) w celu synchronizacji danych z on-prem do GCP. 
Możliwe wykorzystanie przy:
* chęci posiadanie failover replica w GCP
* przy migracji do GCP

## 2. Dział bezpieczeństwa posiada serwery, które nie są związane bezpośrednio z samą architekturą aplikacji. Serwery te również mają zostać przeniesione do środowiska w Google Cloud
> 
    Miscellaneous servers:
        Jenkins, monitoring, bastion hosts, security scanners
        Eight core CPUs
        32GB of RAM
* Compute Engine ([c2-standard-8 8vCPU	32GB](https://cloud.google.com/compute/docs/machine-types#c2_machine_types))

## 3. Firma lokalnie posiada serwery NAS, które odpowiadają za przechowywanie obrazów, logów oraz kopii zapasowych. Serwery muszą posiadać możliwość wersjonowania obiektów oraz kontrolowania dostępu na poziomie pojedyńczego obiektu.
>
    NAS - image storage, logs, backups
        100 TB total storage; 35 TB available
* Cloud Storage - umożliwia włączenie wersjonowania obiektów oraz kontrolowanie dostępu na poziomie pojedyńczego obiektu.
* Filestore - możę być wykorzystana jako NAS jednak nie znalazłem informacji aby usługa ta wspierała wersjonowanie oraz kontrolowanie dostępu na poziomie pojedyńczego obiektu

## 4. Dress4Win planuje zbudować miejsce odzyskiwania danych w przypadku awarii, ponieważ ich obecna infrastruktura znajduje się w jednym miejscu. 
> Zaproponuj plan działania w przypadku awarii na poziomie samej bazy danych, ponieważ jest to krytyczny element działania aplikacji oraz środowisk w całej firmie, dlatego ten element wymaga dość dużej precyzji.
Wykorzystanie możliwości jakie oferuje Cloud SQL:
* [High availability configuration](https://cloud.google.com/sql/docs/mysql/high-availability) na wypadek niedostępności bazy - w takiej sytuacji GCP automatycznie przełączy się na drugą instancję z innej strefie po ok 60s.
* [Automatyczne backupy + binary logging](https://cloud.google.com/sql/docs/mysql/backup-recovery/backups) na wypadek utraty/uszkodzenia danych - mamy tutaj możliwość przywrócenia bazy z backupów które są tworzone co 24h, oraz przywrócenie bazy do określonego czasu na 7 dni wstecz dzięki włączonej opcji binary logging ([point-in-time recovery](https://cloud.google.com/sql/docs/mysql/backup-recovery/restore)). Należy tutaj pamiętać, że przywrócenia bazy do określonego czasu nie możemy wykonać na obecnej instancji - tworzona jest nowa instancja ([źródło](https://cloud.google.com/sql/docs/mysql/backup-recovery/restore#tips-pitr)). Backupy możemy dodatkowo zabezpieczyć/zarchiwizować w usłudze Cloud Storage.

> Zaproponuj plan, który będzie brał pod uwagę odzyskiwanie danych z rozwiązania dla serwerów NAS w Google Cloud tak, aby firma nie musiała się przejmować, że ich obrazy czy też np. logi z danego dnia nagle znikną
* Wykorzystanie Cloud Storage z włączoną opcją wersjonowania obiektów

## 5. Dodatkowe wytyczne
> Zarząd planuje ekspansje globalną jeśli chodzi o aplikacje, wiec również jej dane będą udostępniane globalnie w pewnych regionach. Zarząd zauważył, że baza MySQL pod względem architektury staje się wąskim gardłem, kiedy mówimy o skalowalności. Firma jest gotowa zainwestować czas na migrację do pełni zarządzalnego, skalowalnego, relacyjnego serwisu baz danych dla regionalnych i globalnych danych aplikacyjnych, aby ekspansja na rynek zagraniczny nie była przeszkodą. Jakie rozwiązanie zaproponowałbyś firmie gdyby nie chciała rezygnować z MySQL, ale chciała by zyskać na skalowalności swojego środowiska bazodanowego?
* [Cloud Spanner](https://cloud.google.com/spanner/) będzie odpowiednim wyborem:
    * zapewnia wszystkie wymagane cechy
    * konieczne będzie poświęcenie czasu na dostosowanie oprogramowania - na co firma jest gotowa.

## 6. Przedstaw również proces migracji z klasycznej bazy MySQL do takiego zaproponowanego środowiska.
Utworzenie backupu bazy danych i odtworzenie jej w GCP, problemem tutaj może być czas wykonania takiej migracji w czasie której w środowisku on-prem baza nadal działa. 

Tutaj lepszym wyborem będzie wykorzystanie opcji replikacji bazy, którą oferuje Cloud SQL - [`Replication from an external server`](https://cloud.google.com/sql/docs/mysql/replication/). 
Dzięki temu w czasie rzeczywistym możemy wykonać migrację bazy z on-prem do GCP, a następnie tylko przełączyć połączenie na bazę znajdującąsięw GCP. 
Pamiętać tutaj należy o tym, że środowisko on-prem musi spełniać pewne wymagania, aby taka migracja była możliwa ([Requirements for the source database server](https://cloud.google.com/sql/docs/mysql/replication/replication-from-external#server-requirements)).
* [Kroki do wykonania replikacji](https://cloud.google.com/sql/docs/mysql/replication/replication-from-external#process)

## 7. MountKirk Games
Kiedy przejrzymy treść case study - MountKirk Games natrafimy na taki oto wpis w wymaganiach dotyczących platformy backendowej gry:

> "Connect to a transactional database service to manage user profiles and game state"

#### Jakie rozwiązania zaproponowałbyś dla tego przypadku jeśli chodzi o bazę danych?

* Najlepszym wyborem dla danych użytkowników lub też stanu gry będzie baza dokumentowa (chcąc pobrać dane użytkownika lub stanu gry baza jest odpytywana tylko o jeden dokument zamiast wykonywać zapytanie z dodatkowymi relacjami pobierające dane z różnych tabel), czyli w przypadku GCP będzie to Cloud Firestore, który zapewni:
    * tranzakcyjność
    * `Realtime sync to clients`
    * globalną replikację bazy
* Cloud Spanner odpada głównie ze względu na wysoki koszt + chęć korzystania z nierelacyjnej baz danych:
> and integrate with a managed NoSQL database. 