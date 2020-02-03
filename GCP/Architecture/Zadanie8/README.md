# [Zadanie domowe nr 8](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-8-app-engine/zadanie-domowe-nr-8/)

## 1. Uruchamiasz aplikację w Google App Engine, która obsługuje ruch produkcyjny. Chcesz wdrożyć ryzykowną, ale konieczną zmianę w aplikacji. Może ona zniszczyć Twoją usługę, jeśli nie będzie prawidłowo zakodowana. Podczas tworzenia aplikacji zdajesz sobie sprawę, że możesz ją prawidłowo przetestować tylko z rzeczywistym ruchem użytkowników.
```bash
# Pobranie przykładowych kodów źródłowych
git clone https://github.com/GoogleCloudPlatform/python-docs-samples

# Wdrożenie aplikacji Hello World
cd ./python-docs-samples/appengine/standard/hello_world
gcloud app deploy

# Pobranie adresu aplikacji i sprawdzenie działania
gcloud app browse
gcloud app services list

# Dokonanie zmian w pliku main.py i wdrożenie nowej wersji aplikacji
gcloud app deploy --no-promote

# Pobranie listy wersji
gcloud app versions list

# Wysłanie do nowej wersji aplikacji 30% użytkowników
gcloud app services set-traffic default --splits 20200203t221803=0.7,20200203t223122=0.3 --split-by=random
# Przekierowanie całego ruchu do nowej wersji aplikacji
gcloud app services set-traffic default --splits 20200203t223122=1

# Sprawdzenie
gcloud app versions list
```

## 2. Zarząd pewnej firmy zdecydował się na przeniesienie swojej aplikacji do środowiska w Google Cloud. Zdecydowali się umieścić swoją aplikacje na środowisku w App Engine. Środowisko wymaga integracji z bazą danych MySQL z których aplikacja pobiera dane.

#### 2.1 Utworzenie Cloud SQL
```bash
sqlInstanceName="zadanie8sqlinst2"
secretRootPassword="tajnehaslo12345566"
gcloud sql instances create $sqlInstanceName --root-password $secretRootPassword --activation-policy=ALWAYS --tier=db-n1-standard-1 --region=europe-west1
```

#### 2.2 Utworzenie proxy
> https://cloud.google.com/sql/docs/mysql/connect-admin-proxy

#### 2.3 Utworznie bazy
```bash
mysql -h 127.0.0.1 -u root -p -e "CREATE DATABASE mydbname;"
```

