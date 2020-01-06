# [Zadanie domowe nr 4](https://szkolachmury.pl/google-cloud-platform-droga-architekta/tydzien-4-cloud-identity-and-access-management/zadanie-domowe-nr-4/)

* [Zadanie 1](#1-zadanie-1)
* [Zadanie 2](#2-zadanie-2)

---

## 1. Zadanie 1

> Klient poprosił cię o przygotowanie maszyny dla swoich pracowników, którzy będą mogli pobierać faktury z przygotowanego repozytorium (w naszym przypadku jest to pojemnik Cloud Storage)

#### 1.1 Przygotowanie `Cloud Storage`
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

#### 1.3 Utworzenie VM
```bash
# Zmienne
vmName="zad4bpvm"
vmType="f1-micro"
vmZone="europe-west3-b"
serviceAccountEmail="" # gcloud iam service-accounts list

# Utworzenie VM
gcloud compute instances create $vmName --zone=$vmZone --machine-type=$vmType --image-project=debian-cloud --image=debian-9-stretch-v20191210 --service-account=$serviceAccountEmail
```

#### 1.4 Sprawdzenie uprawnień
> Połączenie się z VM i sprawdzenie czy ma dostęp Read-only do bucketa

<details>
  <summary><b><i>Pokaż</i></b></summary>

```bash
bartosz@zad4bpvm:~$ gsutil ls gs://zad4bpstorage
gs://zad4bpstorage/test1.txt
gs://zad4bpstorage/test2.txt
bartosz@zad4bpvm:~$ gsutil cat gs://zad4bpstorage/test1.txt
Plik 1 - przykładowy tekst 1
bartosz@zad4bpvm:~$ echo "test1" > testvm.txt
bartosz@zad4bpvm:~$ ls
testvm.txt
bartosz@zad4bpvm:~$ gsutil cp testvm.txt gs://zad4bpstorage
Copying file://testvm.txt [Content-Type=text/plain]...
AccessDeniedException: 403 Insufficient Permission                              
bartosz@zad4bpvm:~$ gsutil rm gs://zad4bpstorage/test1.txt
Removing gs://zad4bpstorage/test1.txt...
AccessDeniedException: 403 Insufficient Permission
bartosz@zad4bpvm:~$ gsutil ls gs://
AccessDeniedException: 403 bucket-viewer-zad4@resonant-idea-261413.iam.gserviceaccount.com does not have storage.buckets.list access to project 162512192576.
```
</details>

#### 1.5 Usunięcie zasobów
```bash
gcloud compute instances delete $vmName --zone=$vmZone 
gcloud iam service-accounts delete $serviceAccountEmail
gsutil -m rm -r gs://${bucketName}/
rm test*.txt
```

## 2. Zadanie 2

> Dany klient przetrzymuje bardzo ważne dokumenty. Zarząd zdecydował, że wprowadzą szyfrowanie krytycznych dokumentów, które będą mogły zostać odszyfrowane po stronie pracownika, który z danego dokumentu chce skorzystać.

#### 2.1 Utworzenie bucketa dla plików
```bash
# Zmienne
bucketName="secretstoragebp"
bucketLocation="europe-west3"

# Utworzenie bucketa
gsutil mb -c STANDARD -l $bucketLocation gs://${bucketName}/
```

#### 2.2 Uruchomieie usługi KMS
```bash
gcloud services enable cloudkms.googleapis.com
```

#### 2.3 [Utworzenie klucza asymetrycznego](https://cloud.google.com/kms/docs/creating-asymmetric-keys)
```bash
keyringsName="vmkeyrings"
keyName="vmKeyAsync"
keyPurpose="asymmetric-encryption"
defaultAlgorithm="rsa-decrypt-oaep-3072-sha256"

# Utworzenie Keyrings
gcloud kms keyrings create $keyringsName --location global

# Utworzenie klucza
gcloud kms keys create $keyName --location global --keyring $keyringsName --purpose $keyPurpose --default-algorithm $defaultAlgorithm 
```

#### 2.4 PoC w Cloud Shell
<details>
  <summary><b><i>PoC w Cloud Shell</i></b></summary>

#### 2.4.1 Utworzenie przykładowego pliku
```bash
echo "Plik 1 - przykładowy tekst 1 ąźćżółęż" > test1.txt
```

#### 2.4.2 [Pobranie klucza publicznego](https://cloud.google.com/kms/docs/retrieve-public-key#kms-howto-retrieve-public-key-cli)
```bash
keyVersion="1"

# Pobranie klucza publicznego
gcloud kms keys versions get-public-key $keyVersion --location global --keyring $keyringsName --key $keyName --output-file public-key.pub
```

#### 2.4.3 [Zaszyfrowanie pliku](https://cloud.google.com/kms/docs/encrypt-decrypt-rsa#encrypt_data)
```bash
openssl pkeyutl -in $HOME/zadanie4/test1.txt -encrypt -pubin -inkey $HOME/zadanie4/public-key.pub -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256 > $HOME/zadanie4/secret/test1.enc
```

#### 2.4.4 [Odszyfrowanie pliku](https://cloud.google.com/kms/docs/encrypt-decrypt-rsa#decrypt_data)
```bash
gcloud kms asymmetric-decrypt --location global --keyring $keyringsName --key $keyName --version $keyVersion --ciphertext-file $HOME/zadanie4/secret/test1.enc --plaintext-file $HOME/zadanie4/test1-odszyfrowany.txt
```

#### 2.4.5 Porównanie pliku po odszyfrowaniu
```bash
bartosz@cloudshell:~/zadanie4 (resonant-idea-261413)$ cat test1.txt
Plik 1 - przykładowy tekst 1 ąźćżółęż
bartosz@cloudshell:~/zadanie4 (resonant-idea-261413)$ cat test1-odszyfrowany.txt
Plik 1 - przykładowy tekst 1 ąźćżółęż
```

</details>
