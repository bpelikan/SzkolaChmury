# [Zadanie domowe nr 6](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-6-cloud-storage/zadanie-domowe-nr-6/)

1. Pobierz dane ze wskazanego linku na swój komputer/maszynę wirtualną w chmurze.
https://storage.googleapis.com/testdatachm/sampledata/imagedata.tar.gz
2. Rozpakuj zdjęcia.
3. Stwórz odpowiednie konto storage.
4. Skopiuj dane z zachowaniem struktury katalogów (najlepiej w trybie równoległym).
5. Stwórz odpowiednią metodę dostępu do plików dla zewnętrznej firmy, tak aby mogli dostać się do plików bez konieczności zakładania dedykowanych kont.
6. Wprowadź odpowiednie zasady zarządzania cyklem życia plików, tak aby spełniały wymagania zawarte powyżej.

---

### Utworzenie bucketa
```bash
bucketName="szkchmzad6bp"
bucketLocation="EUR4" # https://cloud.google.com/storage/docs/locations#location-dr
gsutil mb -c STANDARD -l $bucketLocation gs://${bucketName}/
```

## Przygotowanie dostępu dla środowiska on-prem
```bash
serviceAccountOnPrem="onpremserviceaccount"
serviceAccountOnPremDescription="Service account umożliwiający dostęp do storage ze środowiska on-prem"
serviceAccountOnPremDisplayName="Onprem service account"

# Utworzenie konta service account dla on-prem
gcloud iam service-accounts create $serviceAccountOnPrem --description "$serviceAccountOnPremDescription" --display-name "$serviceAccountOnPremDisplayName"

# Pobranie nazwy
gcloud iam service-accounts list
serviceAccountOnPremEmail="onpremserviceaccount@resonant-idea-261413.iam.gserviceaccount.com"

# Nadanie uprawnień do danego bucketa
# https://cloud.google.com/storage/docs/gsutil/commands/iam
gsutil iam ch serviceAccount:$serviceAccountOnPremEmail:objectAdmin gs://${bucketName}/

# Wygenerowanie klucza
gcloud iam service-accounts keys create onpremkey.json --iam-account $serviceAccountOnPremEmail
```

## Przygotowanie dostępu dla klienta
```bash
serviceAccountClient="clientserviceaccount"
serviceAccountClientDescription="Service account umożliwiający dostęp do storage ze środowiska klienta"
serviceAccountClinetDisplayName="Client Service Account"

# Utworzenie konta service account dla klienta
gcloud iam service-accounts create $serviceAccountClient --description "$serviceAccountClientDescription" --display-name "$serviceAccountClinetDisplayName"

# Pobranie nazwy
gcloud iam service-accounts list
serviceAccountClientEmail="clientserviceaccount@resonant-idea-261413.iam.gserviceaccount.com"

# Nadanie uprawnień 
gsutil iam ch serviceAccount:$serviceAccountClientEmail:objectViewer gs://${bucketName}/

# Wygenerowanie klucza
gcloud iam service-accounts keys create clientkey.json --iam-account $serviceAccountClientEmail
```