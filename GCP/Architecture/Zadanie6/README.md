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

### Przygotowanie dostępu dla środowiska on-prem
```bash
serviceAccountOnPrem="onpremserviceaccount"
serviceAccountOnPremDescription="Service account umożliwiający dostęp do storage ze środowiska on-prem"
serviceAccountOnPremDisplayName="Onprem Service Account"

# Utworzenie konta serwisowego dla on-prem
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

### Przygotowanie dostępu dla klienta
```bash
serviceAccountClient="clientserviceaccount"
serviceAccountClientDescription="Service account umożliwiający dostęp do storage ze środowiska klienta"
serviceAccountClinetDisplayName="Client Service Account"

# Utworzenie konta serwisowego dla klienta
gcloud iam service-accounts create $serviceAccountClient --description "$serviceAccountClientDescription" --display-name "$serviceAccountClinetDisplayName"

# Pobranie nazwy
gcloud iam service-accounts list
serviceAccountClientEmail="clientserviceaccount@resonant-idea-261413.iam.gserviceaccount.com"

# Nadanie uprawnień 
gsutil iam ch serviceAccount:$serviceAccountClientEmail:objectViewer gs://${bucketName}/

# Wygenerowanie klucza
gcloud iam service-accounts keys create clientkey.json --iam-account $serviceAccountClientEmail
```

### Weryfikacja uprawnień
```bash
gsutil iam get gs://${bucketName}/ > bucket_iam.json
```
<details>
  <summary><b><i>bucket_iam.txt</i></b></summary>

```json
{
  "bindings": [
    {
      "members": [
        "projectEditor:resonant-idea-261413", 
        "projectOwner:resonant-idea-261413"
      ], 
      "role": "roles/storage.legacyBucketOwner"
    }, 
    {
      "members": [
        "projectViewer:resonant-idea-261413"
      ], 
      "role": "roles/storage.legacyBucketReader"
    }, 
    {
      "members": [
        "serviceAccount:onpremserviceaccount@resonant-idea-261413.iam.gserviceaccount.com"
      ], 
      "role": "roles/storage.objectAdmin"
    }, 
    {
      "members": [
        "serviceAccount:clientserviceaccount@resonant-idea-261413.iam.gserviceaccount.com"
      ], 
      "role": "roles/storage.objectViewer"
    }
  ], 
  "etag": "CAM="
}
```
</details>

### Zalogowanie się do VM on-prem
```bash
bucketName="szkchmzad6bp"

# Sprawdzenie dostępu
gsutil ls gs://$bucketName

# Wykorzystanie klucza w celu uzyskania dostępu do bucketa
gcloud auth activate-service-account --key-file onpremkey.json

# Sprawdzenie dostępu
gsutil ls gs://$bucketName

# Pobranie plików
curl https://storage.googleapis.com/testdatachm/sampledata/imagedata.tar.gz > imagedata.tar.gz

# Rozpakowaie plików
tar -zxvf imagedata.tar.gz > null

# Sprawdzenie czy pliki zostały rozpakowane prawidłowo
ls ./testdatachm/**

# Wysłanie plików do bucketa
gsutil -m cp -r testdatachm gs://$bucketName

# Sprawdzenie rozmiaru bucketa
gsutil du -chs gs://${bucketName}/

```

<details>
  <summary><b><i>Output</i></b></summary>

```bash
bartosz@zad6onprem:~$ bucketName="szkchmzad6bp"
bartosz@zad6onprem:~$ gsutil ls gs://$bucketName
ServiceException: 401 Anonymous caller does not have storage.objects.list access to szkchmzad6bp.
bartosz@zad6onprem:~$ ls
onpremkey.json
bartosz@zad6onprem:~$ gcloud auth activate-service-account --key-file onpremkey.json
Activated service account credentials for: [onpremserviceaccount@resonant-idea-261413.iam.gserviceaccount.com]
bartosz@zad6onprem:~$ gsutil ls gs://$bucketName
bartosz@zad6onprem:~$ curl https://storage.googleapis.com/testdatachm/sampledata/imagedata.tar.gz > image
data.tar.gz
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 72.8M  100 72.8M    0     0  59.1M      0  0:00:01  0:00:01 --:--:-- 59.1M
bartosz@zad6onprem:~$ tar -zxvf imagedata.tar.gz > null
bartosz@zad6onprem:~$ ls ./testdatachm/**
./testdatachm/fungs:
fung100.jpg  fung155.jpg  fung209.jpg  fung253.jpg  fung302.jpg  fung356.jpg  fung415.jpg  fung57.jpg
{...}
bartosz@zad6onprem:~$ gsutil -m cp -r testdatachm gs://$bucketName
{...}
/ [964/964 files][ 73.6 MiB/ 73.6 MiB] 100% Done 512.4 KiB/s ETA 00:00:00       
Operation completed over 964 objects/73.6 MiB.
bartosz@zad6onprem:~$ gsutil du -chs gs://${bucketName}/
73.61 MiB    gs://szkchmzad6bp
73.61 MiB    total
```
</details>

### Zalogowanie się do VM klienta
```bash
bucketName="szkchmzad6bp"

# Sprawdzenie dostępu
gsutil ls gs://$bucketName

# Wykorzystanie klucza w celu uzyskania dostępu do bucketa
gcloud auth activate-service-account --key-file clientkey.json

# Sprawdzenie dostępu
gsutil ls gs://$bucketName

# Pobranie przykładowego pliku
gsutil cp gs://$bucketName/testdatachm/fungs/fung209.jpg .
```

<details>
  <summary><b><i>Output</i></b></summary>

```bash
bartosz@zad6client:~$ bucketName="szkchmzad6bp"
bartosz@zad6client:~$ gsutil ls gs://$bucketName
ServiceException: 401 Anonymous caller does not have storage.objects.list access to szkchmzad6bp.
bartosz@zad6client:~$ ls
clientkey.json
bartosz@zad6client:~$ gcloud auth activate-service-account --key-file clientkey.json
Activated service account credentials for: [clientserviceaccount@resonant-idea-261413.iam.gserviceaccount.com]
bartosz@zad6client:~$ gsutil ls gs://$bucketName
gs://szkchmzad6bp/testdatachm/
bartosz@zad6client:~$ gsutil cp gs://$bucketName/testdatachm/fungs/fung209.jpg .
Copying gs://szkchmzad6bp/testdatachm/fungs/fung209.jpg...
- [1 files][ 63.5 KiB/ 63.5 KiB]                                                
Operation completed over 1 objects/63.5 KiB.                                     
bartosz@zad6client:~$ ls
clientkey.json  fung209.jpg
```
</details>