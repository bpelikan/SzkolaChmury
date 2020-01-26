# [Zadanie domowe nr 7](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-7-databases-on-google-cloud/zadanie-domowe-nr-7/)

---


## 1. Firma posiada jedną głowną bazę danych MySQL - jeden serwer dla danych użytkowników, inwentaryzacji, danych statycznych. Serwis ten jest głównym elementem, który ma zostać przeniesiony do środowiska w Google Cloud.
> 
    MySQL. One server for user data, inventory, static data,
        MySQL 5.7
        8 core CPUs
        128 GB of RAM
        2x 5 TB HDD (RAID 1)

Patrząc na powyższe wymagania potrzebować będziemy bazę MySQL o pojemności 5TB z włączoną opcją HA (jako, że storage bazy on-prem jest w RAID 1). 
Wymagania te spełni baza `Cloud SQL`, problemem tutaj może być wybór odpowiedniego typu maszyny:
* db-n1-standard-32 (32vCPU, 120 GB)
* db-n1-standard-64 (64vCPU, 240 GB)
* db-n1-highmem-16 (16vCPU, 104 GB)
* db-n1-highmem-32 (32vCPU, 208 GB)

Dodatkowo można wykorzystać tutaj opcję replikacji bazy [`Replication from an external server`](https://cloud.google.com/sql/docs/mysql/replication/) w celu synchronizacji danych z on-prem do GCP. 
Możliwe wykorzystanie przy:
* chęci posiadanie failover replica w GCP
* przy migracji do GCP