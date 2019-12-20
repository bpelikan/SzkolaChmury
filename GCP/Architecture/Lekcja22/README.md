# [Snapshot](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-3-compute-engine/snapshots/)

## Profile konfiguracyjne
```bash
# Lista projektów
gcloud projects list

# Sprawdzenie profilu konfiguracyjnego - domyślne wartości
gcloud config list

# Lista konfiguracji
gcloud config configurations list

# Tworzenie nowej konfiguracji
gcloud config configurations create szkolachmury

# Ustawienie projektu
gcloud config set project <Nazwa lub ID projektu>

# Lista dostępnych regionów
gcloud compute regions list

# Ustawienie domyślnego regionu dla compute
gcloud config set compute/region us-central1
```
