# [Zadanie domowe nr 8](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-8-app-engine/zadanie-domowe-nr-8/)

## 1. Uruchamiasz aplikację w Google App Engine, która obsługuje ruch produkcyjny. Chcesz wdrożyć ryzykowną, ale konieczną zmianę w aplikacji. Może ona zniszczyć Twoją usługę, jeśli nie będzie prawidłowo zakodowana. Podczas tworzenia aplikacji zdajesz sobie sprawę, że możesz ją prawidłowo przetestować tylko z rzeczywistym ruchem użytkowników.
```bash
# Pobranie przykładowych kodów źródłowych
git clone https://github.com/GoogleCloudPlatform/python-docs-samples

# deploy aplikacji Hello World
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
# Przekirowanie całego ruchu do nowej wersji aplikacji
gcloud app services set-traffic default --splits 20200203t223122=1

# Sprawdzenie
gcloud app versions list
```

