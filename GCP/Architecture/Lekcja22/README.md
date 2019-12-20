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

## Tworzenie VM
```bash
# Stworzenie instancji VM
gcloud compute instances create vm1a --machine-type=f1-micro --zone=us-central1-a

# Stworzenie dysku
gcloud compute disks create vmdisk1a --size=50GB --zone-us=central1-a

# Lista dysków
gcloud compute disks list

# Podpięcie dysku do VM
gcloud compute instances attach-disk vm1a --disk=vmdisk1a --zone=us-central1-a
```
