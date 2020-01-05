# [Zadanie domowe nr 4](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-4-cloud-identity-and-access-management/zadanie-domowe-nr-4/)

## 1. Zadanie 1

### 1.1 Przygotowanie `Cloud Storage`
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

#### 1.2 Utworzenie `Service Account`
> Utworzenie konta serwisowego z dostępnem Read-only do wcześniej utworzonego bucketa

<details>
  <summary><b><i>Pokaż</i></b></summary>

![Screen](./img/20200105215929.jpg "Screen")
Dodanie roli **Storage Object Viewer**

![Screen](./img/20200105220454.jpg "Screen")
Oraz warunku dostępu tylko do danego bucketa:
* Name is `projects/_/buckets/zad4bpstorage`
* or Name Starts with `projects/_/buckets/zad4bpstorage/objects/`

![Screen](./img/20200105220527.jpg "Screen")

</details>

