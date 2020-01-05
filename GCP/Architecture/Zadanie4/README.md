# [Zadanie domowe nr 4](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-4-cloud-identity-and-access-management/zadanie-domowe-nr-4/)

## 1. Zadanie 1

### 1.1 Przygotowanie Cloud Storage
```bash
# Zmienne
bucketName="zad4bpstorage"
bucketLocation="europe-west3"

# Utworzenie bucketa
gsutil mb -c STANDARD -l $bucketLocation gs://${bucketName}/

# Utworzenie plików
echo "Plik 1 - przykładowy tekst 1" > test1.txt
echo "Plik 2 - przykładowy tekst 2" > test2.txt

# Wysłanie plików
gsutil cp test*.txt gs://${bucketName}/
```

